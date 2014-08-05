#encoding=utf-8
import urllib3
import socket
from cohost.models import Data, Allkey, Cate, Keywords
import requests

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
    print domain
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

# def get_beian(domain):
#     url = "http://api.k780.com:88/?app=domain.beian"
#     params = {}
#     params['domain'] = domain
#     params['appkey'] = "11438"
#     params['sign'] = "3393c4e359d09cd601093dfbcc8cad9b"
#     params['format'] = "json"
#     r = requests.get(url, params=params)
#     rsp = r.json()
#     if rsp['success'] == "1":
#         return rsp['result']
#     else:
#         print rsp['msg']
#         return 


def makeup_info():
    datas = Data.objects.filter(cate=None).exclude(state="-1")
    print datas
    kwords = Keywords.objects.all()
    for d in datas:
        print d.uri
        beian = get_beian(d.uri)
        ip_info = get_ip_info(d.ip)
        if ip_info:
            d.IPS = ip_info.get("detailed", '')
        if beian:
            d.__dict__.update(**beian)
        for k in kwords:
            if k.kword in d.descript:
                d.cate = k.cate
        d.save()




