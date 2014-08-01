# -*- coding: utf-8 -*-
#https://datamarket.azure.com/account/datasets
#Code by Anle
import sys
import urllib  
import urllib2
import urllib3  
import base64
import socket
import struct
import time
import requests
import MySQLdb
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

def ViewResult(Keyword,curIP,nType,bSave):
    conn = MySQLdb.connect(**ConfigFile)
    #conn.text_factory=str
    ResData=BingSearch(Keyword)
    JsonData={}
    try:
        JsonData=json.loads(ResData)
    except:
        pass
    url=[]
    for key,value in JsonData.items():
        for key1,value1 in value.items():
            for lv in value1:
                try:
                    if nType==0:
                        uu=lv['Url']
                        i=uu.find('/',8)
                        url.append(uu[0:i])
                    elif nType==1:
                        print lv['Url']
                    elif nType==2:
                        print '%s -> %s' % (lv['Url'],lv['Title'])
                    if bSave:
                        host = urllib3.get_host(lv['Url'])[1]
                        szSQL="Insert into Data(IP,URI,Title,Descript) values ('%s','%s','%s','%s');" % (curIP,host,lv['Title'],lv['Description'])
                        cur = conn.cursor()
                        cur.execute(szSQL)

                        conn.commit()
                except Exception, e:
                    raise e
    if nType==0:
        for l in list(set(url)):
            print l
    print '\r\n'
    conn.close()

def ViewSaveData(nType):
    conn = MySQLdb.connect(**ConfigFile)
    conn.text_factory=str
    cf=conn.cursor()
    cf.execute("Select IP From DATA group by IP;")
    ipList=cf.fetchall()

    for IP in ipList:
        cf.execute("Select URI,Title,Descript from Data where IP='%s';" % (IP))
        dataList=cf.fetchall()
        i=0
        url=[]
        print '[%s]' % (IP)
        for row in dataList:
            i += 1
            if nType==0:
                uu=row[0]
                i=uu.find('/',8)
                url.append(uu[0:i])
            elif nType==1:
                print row[0]
            elif nType==2:
                print '%s -> %s' % (row[0],row[1])
        if i<=0:
            print '[-] No records.'
        elif nType==0:
            for l in list(set(url)):
                print l
    cf.close()
    conn.close()

def UpdateUseCount():
    global useCounts
    try:
        NowMonth=time.gmtime().tm_mon
        OldMonth=1
        conn = MySQLdb.connect(**ConfigFile)
        cf=conn.cursor()
        cursor = cf.execute("Select VisitMonth from AllKey where id=%d" % useID)
        keys=cf.fetchone()
        if keys!=None:
            OldMonth=keys[0]
        cf.close()
        if NowMonth - OldMonth >= 1:
            useCounts = 1
        szSQL="Update AllKey set useCount=%d,VisitMonth=%d where id=%d" % (useCounts,NowMonth,useID)
        cur = conn.cursor()
        cur.execute(szSQL)
        conn.commit()
    except Exception, e:
        print '[-] ',e
    conn.close()
    
def BingSearch(query):
    global useCounts
    payload={}  
    payload['$top']=top  
    payload['$skip']=skip  
    payload['$format']=formats  
    payload['Query']="'"+query+"'"
    url='https://api.datamarket.azure.com/Bing/Search/Web?' + urllib.urlencode(payload)       
    sAuth='Basic '+base64.b64encode(':'+AccountKey)  
    
    headers = { }  
    headers['Authorization']= sAuth  
    try:  
        req = urllib2.Request(url,headers=headers)          
        response = urllib2.urlopen(req)
        the_page=response.read()
        useCounts += 1
        return the_page 
    except:
        print '[-] Connect failed.'


# def BingSearch(query):
#     global useCounts
#     payload={}  
#     payload['$top']=top  
#     payload['$skip']=skip  
#     payload['$format']=formats  
#     payload['Query']="'"+query+"'"
#     url='https://api.datamarket.azure.com/Bing/Search/Web?'      
#     sAuth='Basic '+base64.b64encode(':'+AccountKey)  
#     headers = {}  
#     headers['Authorization']= sAuth  
#     try:  
#         res = requests.get(url, params=payload, headers=headers)
#         print res.__dict__
#         print type(res)
#         print res.text
#         print "!!!!!!!!!!!!!!!"
#         print res.content
#         the_page = res.content
#         useCounts += 1
#         return the_page 
#     except Exception, e:
#         print e
#         print '[-] Connect failed.'    
      
if __name__ == '__main__':
    argLen = len(sys.argv)
    if argLen < 2:
        _usage()
        sys.exit(0)
    arg=sys.argv
    # if not CheckDatabaseExist():
    #     print '[-] Database is not exist, but would auto create.'
    
    nType=0
    strHost=""
    bSave=False
    bView=False
    bManualStr=False
    
    keyInfo=GetAccountKey()
    useID=keyInfo[0]
    AccountKey=keyInfo[1]
    useCounts=keyInfo[2]
    
    for x in range(1,argLen):
        if arg[x]=='-url' and argLen>2:
            nType=0
            if (x+1)<argLen:
                strHost=arg[x+1]
        if arg[x]=='-uri' and argLen>2:
            nType=1
            if (x+1)<argLen:
                strHost=arg[x+1]
        if arg[x]=='-desc' and argLen>2:
            nType=2
            if (x+1)<argLen:
                strHost=arg[x+1]
        if arg[x]=='-view':
            bView=True
        if arg[x]=='-key':
            conn = MySQLdb.connect(**ConfigFile)
            cf=conn.cursor()
            cf.execute("SELECT id,bActive,KeyName,UseCount from AllKey;")
            keylist=[]
            keylist=cf.fetchall()
            i=0
            for row in keylist:
                xx=' '
                if row[1]==1:
                    xx='>'
                print '%s%-5d %s %5d' % (xx,row[0],row[2],row[3])
                i += 1
            if i<=0:
                print '[-] No records.'
            cf.close()
            conn.close()
            sys.exit(0)
        if arg[x]=='-add' and argLen>2:
            keystr=arg[x+1]
            if not keystr:
                print '[-] Please input a key value.\n'
                sys.exit(0)
            NowMonth=time.gmtime().tm_mon
            szSQL = "INSERT INTO AllKey(bActive,KeyName,VisitMonth,UseCount)  VALUES (%d,'%s',%d,%d)"  % (0,keystr,NowMonth,1)
            conn = MySQLdb.connect(**ConfigFile)
            try:
                cursor = conn.cursor()
                cursor.execute(szSQL)
                conn.commit()
                cursor.close()
                conn.close()
                print '[+] Add a key records successfully.\r\n'
            except Exception, e:
                print e
                print '[-] This record has exsits.'
            sys.exit(0)
        if arg[x]=='-set' and argLen>2:
            ID=int(arg[x+1])
            if argLen>3:
                useCounts=int(arg[x+2])
            if not ID:
                print '[-] ID value incorrect.'
                sys.exit()
            try:
                szSQL="Update AllKey set bActive=0;"
                conn = MySQLdb.connect(**ConfigFile)
                cursor = conn.cursor()
                cursor.execute(szSQL)
                conn.commit()
                szSQL="Update AllKey set bActive=1 where id=%d" % (ID)
                cursor.execute(szSQL)
                conn.commit()
                print '[+] Set success.'
            except:
                print '[-] Set failed.'
            if useCounts>0:
                UpdateUseCount()
            sys.exit(0)
        if arg[x]=='-del' and argLen>2:
            ID=int(arg[x+1])
            if not ID:
                print '[-] ID value incorrect.'
                sys.exit()
            try:
                szSQL = 'Delete from AllKey where id=%d;' % (ID)
                conn = MySQLdb.connect(**ConfigFile)
                cur = conn.cursor()
                cur.execute(szSQL)
                conn.commit()
                print '[+] Delete success.'
            except:
                print '[-] Delete failed.'
            sys.exit(0)
        if arg[x]=='-save':
            bSave=True
        if arg[x]=='-api':
            bManualStr=True
        if arg[x]=='-export':
            pass

    if not strHost and bView==False:
        _usage()
        sys.exit()

    if useID==0:
        print '[-] Please set a active ID.'
        sys.exit()

    # if bSave:
    #     conn = MySQLdb.connect(**ConfigFile)
    #     conn.execute("Delete from Data where ID>0;")
    #     conn.commit()
    #     conn.close()

    if bManualStr:
        ViewResult(strHost,strHost,nType,bSave)
        UpdateUseCount()
        sys.exit()

    if bView:
        ViewSaveData(nType)
        sys.exit()
        
    """uri, type, ID, Title, Description, DisplayUrl, Url"""
    IpRange=BuildHostRange(strHost)
    for index in range(IpRange[0],IpRange[1]+1):
        curIP=socket.inet_ntoa(struct.pack('I',socket.htonl(index)))
        SearchKeyWord='IP:' + curIP
        print '[%s]' % (curIP)
        ViewResult(SearchKeyWord,curIP,nType,bSave)
    UpdateUseCount()
