# -*- coding: utf-8 -*-
#https://datamarket.azure.com/account/datasets
#Code by Anle
import sys
import os
import redis
import urllib  
import urllib2
import urllib3  
import base64
import socket
import struct
import time
import requests
import MySQLdb
import logging
from multiprocessing import Pool

logger = logging.getLogger('tasks.log')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wenzhou.settings")
from cohost.models import Data
from cohost.models import Ips
from datetime import datetime,timedelta
try:  
    import json  
except ImportError:  
    import simplejson as json


AccountKey=''  
top=100  
skip=0
formats='json'
useCounts = 0
useID = 0
ConfigFile = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "db": "bing",
}

def _usage():
    print 'Bing Domain dig Usage:'
    print '\t%s <options> [Host]' % sys.argv[0]
    print 'Options:\t'
    print '-url\t\tOnly view url.\t'
    print '-uri\t\tView url of full path.\t'
    print '-desc\t\tView description info.\t'
    print '-key\t\tView all account key.\t'
    print '-add <key>\tAdd a key to database.\t'
    print '-set <id> [num]\tSet a key to current use.\t'
    print '-del <id>\tDelete a key from database.\t'
    print '-view\t\tView the last saved record.\t'
    print '-save\t\tSave to databse.\t'
    print '-export <path>\tExport data to file.\n'

def CheckDatabaseExist():

    szSQL="SELECT name FROM sqlite_master WHERE type='table' order by name;"
    try:
        conn=MySQLdb.connect(**ConfigFile)
        cursor=conn.execute(szSQL)
    except Exception, e:
        print e
        return 0
    nTable=0
    for row in cursor:
        if row[0]=='AllKey' or row[0]=='Data':
            nTable += 1
    if nTable!=2:
        conn.execute("Create table AllKey(id integer PRIMARY KEY autoincrement,bActive INT NOT NULL,KeyName TEXT UNIQUE NOT NULL,VisitMonth INT default 0,UseCount INT default 0);")
        conn.execute("Create table Data(ID integer PRIMARY KEY autoincrement,IP TEXT NOT NULL,URI TEXT NOT NULL,Title TEXT,Descript TEXT);")
    cursor.close()
    conn.close()
    return nTable==2

def GetAccountKey():
    conn = MySQLdb.connect(**ConfigFile)
    cf=conn.cursor()
    cursor = cf.execute("Select id,KeyName,UseCount from AllKey where bActive=1")
    keys=cf.fetchone()
    if keys==None:
        keys=[0,'',0]
    cf.close()
    conn.close()
    return keys

def BuildHostRange(strHost):
    slash=[]                                      
    startIpStr=""
    endIpStr=""
    ranges=0
    submask=0

    realStartIP=0
    realEndIP=0

    if strHost.find('-')>0:
        slash = strHost.split('-')
        startIpStr=slash[0]
        endIpStr=slash[1]
    else:
        startIpStr=strHost
    try:
        startIpStr=socket.gethostbyname(startIpStr)
        if strHost.find('-')>0:
            realStartIP = socket.ntohl(struct.unpack('I',socket.inet_aton(startIpStr))[0])
            realEndIP = socket.ntohl(struct.unpack('I',socket.inet_aton(endIpStr))[0])
        else:
            realStartIP=realEndIP=socket.ntohl(struct.unpack('I',socket.inet_aton(startIpStr))[0])
    except:
        return [0,0]

    return [realStartIP,realEndIP]


def getIp(domain):
    myaddr = socket.getaddrinfo(domain,'http')[0][4][0]
    return myaddr

def ViewResult(data):
    JsonData={}

    for r in data:
        ResData = r.get("ResData", "")
        curIP = r.get("curIP", "")
        updated = r.get("updated", "")
        data_query = Data.objects.filter(ip=curIP)

        if not updated:
            #如果快照的内容没有更新则更新数据
            print ("nothing changed compared with cached page")
            logger.info("nothing changed compared with cached page")
            continue
        try:
            JsonData=json.loads(ResData)
        except:
            pass
        print ("[%s]" % curIP)
        logger.info("[%s]" % curIP)
        url=[]
        for key,value in JsonData.items():
            for key1,value1 in value.items():
                for lv in value1:
                    try:
                        print (lv['Url'])
                        logger.info(lv['Url'])
                        host = urllib3.get_host(lv['Url'])[1]
                        d_query_set = data_query.filter(uri=host)
                        if d_query_set.exists():
                            print ("update 2 ip-host : %s->%s" %(curIP, host))
                            #同个ip 如果更新域名则同步更新内容
                            d_query = d_query_set[0]
                            d_query.uri = host
                            d_query.title = lv['Title']
                            d_query.descript = lv['Description']
                            d_query.state = '6' #域名更新
                            d_query.save()
                        else:
                            print "save to database %s" % host
                            now = datetime.datetime.now()
                            Data.objects.create(ip=curIP,uri=host,title=lv['Title'],descript=lv['Description'], time=now)
                    except Exception, e:
                        print e

                    finally:
                        pass
        print '\r\n'


def NewViewResult(data):
    JsonData={}
    ResData = data.get("ResData", "")
    curIP = data.get("curIP", "")
    updated = data.get("updated", "")
    data_query = Data.objects.filter(ip=curIP)
    if not updated:
        #如果快照的内容没有更新则更新数据
        print ("nothing changed compared with cached page")
        return 
    try:
        JsonData=json.loads(ResData)
    except Exception, e:
        print e;
        pass
    print "[%s]" % curIP
    url=[]
    for key,value in JsonData.items():
        for key1,value1 in value.items():
            for lv in value1:
                try:
                    print lv['Url']
                    host = urllib3.get_host(lv['Url'])[1]
                    # newip = getIp(host)
                    # if newip == curIP:
                    d_query_set = data_query.filter(uri=host)
                    if d_query_set.exists():
                        print ("update 2 ip-host : %s->%s" %(curIP, host))
                        #同个ip 如果更新域名则同步更新内容
                        d_query = d_query_set[0]
                        d_query.uri = host
                        d_query.title = lv['Title']
                        d_query.descript = lv['Description']
                        d_query.state = '6' #域名更新
                        d_query.save()
                    else:
                        print "save to database %s" % host
                        Data.objects.create(ip=curIP,uri=host,title=lv['Title'],descript=lv['Description'])
                # else:
                    #     print ("fake curip")
                except Exception, e:
                    print e

                finally:
                    pass
        print '\r\n'
    
def BingSearch(index, _AccountKey=None):
    r_server = redis.Redis("localhost",)
    
    global useCounts
    curIP=socket.inet_ntoa(struct.pack('I',socket.htonl(index)))
    query='IP:' + curIP
    payload={}  
    payload['$top']=top  
    payload['$skip']=skip  
    payload['$format']=formats  
    payload['Query']="'"+query+"'"
    url='https://api.datamarket.azure.com/Bing/Search/Web?' + urllib.urlencode(payload)       
    sAuth='Basic '+base64.b64encode(':'+_AccountKey)  
    headers = { }  
    headers['Authorization']= sAuth  
    try:  
        req = urllib2.Request(url,headers=headers)          
        response = urllib2.urlopen(req)
        the_page=response.read()
        useCounts += 1
        result = {'ResData': the_page, "curIP": curIP,}
        cached = r_server.get("cachedIP/%s" % curIP)
        if cached != the_page:
            print ("create or update infos")
            r_server.set("cachedIP/%s" % curIP, the_page)
            result['updated'] = True
        return  result
    except Exception, e:
        print e
        logger.error('%s ' % e)
        print ('[-] Connect failed.')
        raise e
  
def y(x):
    print (x)

def f(r):
    print r
    keyInfo=GetAccountKey()
    AccountKey = keyInfo[1]
    res = BingSearch(r, AccountKey)
    print res
    return "res"
    # return "y"


#测试用Ip集合
test_result = [ '36.22.64.0-36.22.127.255', '39.180.128.0-39.180.136.255']

#完整ip集合
result = [
 "122.228.192.0-122.228.192.255",
 '122.228.193.0-122.228.193.255',
 '122.228.194.0-122.228.194.255',
 '122.228.195.0-122.228.195.255',
 '122.228.195.193-122.228.195.255',# 后续
 '122.228.196.0-122.228.196.255',
 '122.228.197.0-122.228.197.255',
 '122.228.198.0-122.228.198.255',
 '122.228.199.0-122.228.199.255',
 '122.228.228.16-122.228.228.23',
 '122.228.228.64-122.228.228.127',
 '122.228.230.0-122.228.230.127',
 '122.228.231.64-122.228.231.127',
 '122.228.252.64-122.228.252.95',
 '122.228.254.128-122.228.254.143',
 '122.228.255.16-122.228.255.31',
 '122.228.255.48-122.228.255.63',
 '122.228.68.64-122.228.68.79',
 '122.228.71.0-122.228.71.31',
 '122.228.71.64-122.228.71.79',
 '122.228.72.80-122.228.72.95',
 '122.228.73.0-122.228.73.15',
 '60.190.101.192-60.190.101.255',
 '60.190.114.240-60.190.114.255',
 '60.190.118.160-60.190.118.175',
 '61.164.120.240-61.164.120.255',
 '61.164.122.128-61.164.122.143',
 '61.164.124.0-61.164.124.127',
 '61.164.125.0-61.164.125.255',
 '61.164.155.144-61.164.155.159',
 '61.164.159.192-61.164.159.223',]


def do_bing():
    """异步执行bing查询动作"""
    keyInfo=GetAccountKey()
    AccountKey =keyInfo[1]
    useCounts=keyInfo[2]
    bSave = True
    nType = 1
    p = Pool(processes=4)
    
    now = time.time()
    ips = Ips.objects.all().values_list("ip", flat=True)
    futures = []
    #单线程版本用于测试线路
    # for ip in iter(ips):
    #     res = f(int(ip))
    #     NewViewResult(res)
    #多线程版本   
    for ip in iter(ips):    
        r = p.apply_async(f, [int(ip), ], callback=NewViewResult)
        r.get()
    # for fu in futures:
        # r = fu.get()
    # r = p.map_async(f, iter(ips), callback=ViewResult)
    # for strHost in test_result:
    #     IpRange=BuildHostRange(strHost)
    end = time.time()
    print (end-now)


def read_from_ipbook():
    with open('ip.txt',"r") as data:
        c = data.read()
        d = c.split(",")
        print d

if __name__ == '__main__':
    do_bing()



