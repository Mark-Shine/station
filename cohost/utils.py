#encoding=utf-8

import urllib3
import socket
from cohost.models import Data, Allkey, Cate, Keywords
import requests
import time
from multiprocessing import Pool


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
    print "##########\n"
    socket.settimeout(3)
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

# from queue import Queue 
# from functools import wraps

# class Async:
#     def __init__(self, func, args):
#         self.func = func 
#         self.args = args

# def inlined_async(func): 

#     @wraps(func)
#     def wrapper(*args): 
#         f = func(*args)
#         result_queue = Queue() 
#         result_queue.put(None) 
#         while True:
#             result = result_queue.get() 
#             try:
#                 a = f.send(result)
#                 apply_async(a.func, a.args, callback=result_queue.put) 
#             except StopIteration:
#                 break 
#     return wrapper
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


def makeup_info():
    p = Pool(processes=4)

    datas = Data.objects.filter(cate=None).exclude(state="-1")
    kwords = Keywords.objects.all()
    for d in datas:
        r = p.apply_async(getIp, (d.uri, ), callback=handle_obj(d, kwords))
    print ("GOOd bye")

if __name__ == '__main__':
    makeup_info()
    # p = Pool(processes=4)
    # apply_async = p.apply_async

