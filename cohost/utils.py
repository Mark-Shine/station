#encoding=utf-8

import urllib3
import socket
from cohost.models import Data, Allkey, Cate, Keywords
import requests
import struct
import time
from cohost.models import Area
from multiprocessing import Pool
from cohost.models import Ips
from BeautifulSoup import BeautifulSoup

def urldecode_to_utf8(dict_data):
    for k, v in dict_data.items():
        urldecode_data = urllib.unquote(str(v))
        try:
            unicode_data = unicode(urldecode_data, 'utf-8')
        except Exception, e:
            print "error in urldecode_data encode utf8"
            try:
                unicode_data = unicode(urldecode_data, 'gbk')
            except Exception, e:
                print "error in urldecode_data encode GB2312"
                raise e
        dict_data[k] = unicode_data
    return dict_data



def url2host():
    datas = Data.objects.all()
    for d in datas:
        host = urllib3.get_host(d.uri)[1]
        d.uri = host
        d.save()

def getIp(domain):
    print "ping domain :%s" % domain
    myaddr = socket.getaddrinfo(domain,'http')[0][4][0]
    return myaddr

def validate_host_ip():
    ds = Data.objects.all()
    for d in ds:
        ip = getIp(d.uri)
        if ip != d.ip:
            d.state = '-1'
            print "%s, %s" %(ip, d.ip)
            d.save()


def get_cate():
    """根据关键字 判断站点类型"""
    datas = Data.objects.filter(cate=None)
    kwords = Keywords.objects.all()
    for d in datas:
        for k in kwords:
            if k.kword in d.descript:
                d.cate = k.cate
                d.save()

def get_host_infos(host):
    """获取host站点信息"""
    res = requests.get("http://%s" % host, timeout=1)
    page = res.content
    info = {}
    if page:
        soup = BeautifulSoup(page)
        info['title'] = soup.title.text
        descript = soup.find(attrs={"name":"description"})
        info['descript'] = descript and descript.get('content', "") or ""
        print info
    return info

def build_api_get(querykey, queryurl, format="json"):
    
    def api_get(querystr):
        url = queryurl
        params = {}
        params[querykey] = querystr
        params['appkey'] = "11438"
        params['sign'] = "3393c4e359d09cd601093dfbcc8cad9b"
        params['format'] = format
        r = requests.get(url, params=params)
        rsp = r.json()
        if rsp['success'] == "1":
            return rsp['result']
        else:
            print rsp['msg']
            return
    return api_get

get_beian = build_api_get(querykey="domain", queryurl="http://api.k780.com:88/?app=domain.beian")
get_ip_info = build_api_get(querykey="ip", queryurl="http://api.k780.com:88/?app=ip.get")

def handle_obj(obj, kwords):
    """查询ip及域名的备案信息"""
    def wrapped(ping_ip):
        if ping_ip != obj.ip:
            print ("ping_ip :%s not equal curIP %s" %(ping_ip, obj.ip))
            obj.state = "-1"
        else:
            host = obj.uri
            beian = get_beian(host)
            ip_info = get_ip_info(obj.ip)
            if ip_info:
                obj.IPS = ip_info.get("detailed", '')
            if beian:
                obj.__dict__.update(**beian)
            for k in kwords:
                if k.kword in obj.descript:
                    obj.cate = k.cate
        obj.save()
        return 
    return wrapped


def makeup_info_bulk(datas=None):
    p = Pool(processes=4)
    if datas is None:
        print "please put datas in "
        return
    kwords = Keywords.objects.all()
    for d in datas:
        r = p.apply_async(getIp, (d.uri, ), callback=handle_obj(d, kwords))
        r.wait(5)
    print ("GOOd bye")



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
    except Exception, e:
        print e
        return [0,0]
    print realStartIP, realEndIP
    return [realStartIP,realEndIP]


def put_ip(x):
    area, created = Area.objects.get_or_create(name=u"龙湾")
    obj, cred = Ips.objects.get_or_create(ip=x, area=area)
    if not cred:
        print "insert ip"


def put_into_ippool(ips):
    # ips = read_from_ipbook()
    for strHost in ips:
        IpRange = BuildHostRange(strHost)
        map(f, range(IpRange[0], IpRange[1]+1))



if __name__ == '__main__':
    put_into_ippool(result)
    datas = Data.objects.filter(cate=None).exclude(state="-1")
    makeup_info_bulk(datas)
    # p = Pool(processes=4)utls
    # apply_async = p.apply_async

