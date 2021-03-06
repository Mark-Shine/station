#encoding=utf-8
import sys
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
    if res.status_code==200:
        soup = BeautifulSoup(page)
        info['title'] = soup.title.text
        # print type(soup.title.text)
        # print str(soup.title.text)
        descript = soup.find(attrs={"name":"description"})
        info['descript'] = descript and descript.get('content', "") or ""
    return info

# def put_host():
#     das = Data.objects.all()
#     for d in das:
#         try:
#             info = get_host_infos("http://%s" % d.uri)        
#         except Exception, e:
#             continue
#             print e
#         finally:
#             pass
#         d.__dict__.update(**info)
#         d.save()


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
        if ping_ip != obj.ips_id.ip:
            print ("ping_ip :%s not equal curIP %s" %(ping_ip, obj.ips_id.ip))
            obj.state = "-1"
        else:
            host = obj.uri
            beian = get_beian(host)
            ip_info = get_ip_info(obj.ips_id.ip)
            if ip_info:
                obj.IPS_net = ip_info.get("detailed", '')
            if beian:
                obj.__dict__.update(**beian)
            for k in kwords:
                if k.kword in obj.descript or k.kword in obj.title:
                    obj.cate = k.cate
                    break
                else:
                    #如果没有匹配的，就分入其他  
                    cate, created = Cate.objects.get_or_create(name=u"其他")
                    obj.cate = cate
        obj.save()
        sys.stdout.flush()
        return 
    return wrapped

def put_cate():
    das =  Data.objects.all()
    kwords = Keywords.objects.all()
    for obj in das:
        for k in kwords:
            print k.kword
            print k.kword in obj.descript 
            if (k.kword in obj.descript) or (k.kword in obj.title):
                obj.cate = k.cate
                break
            else:
                #如果没有匹配的，就分入其他  
                cate, created = Cate.objects.get_or_create(name=u"其他")
                obj.cate = cate
        obj.save()


def makeup_info_bulk(datas=None):
    p = Pool(processes=4)
    if datas is None:
        print "please put datas in "
        return
    kwords = Keywords.objects.all()
    for d in datas:
        try:
            r = p.apply_async(getIp, (d.uri, ), callback=handle_obj(d, kwords))
            r.get(5)
        except Exception, e:
            print e
        finally:
            pass
        try:
            host_info = get_host_infos(d.uri)
        except Exception, e:
            print e
        finally:
            pass
        if host_info:
            d.title = host_info['title']
            d.descript = host_info['descript']
            d.save()
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
    return [realStartIP,realEndIP]

def build_area_ip(area_name=u'其他'):
    def put_ip(x,):
        curip = socket.inet_ntoa(struct.pack('I',socket.htonl(x)))
        area, created = Area.objects.get_or_create(name=area_name)
        obj, cred = Ips.objects.get_or_create(ip=curip, defaults=dict(area=area))
        # print "created ip %s ? %s" % (obj.ip, cred)
    return put_ip

def put_into_ippool(ips, area_name=u'其他'):
    for strHost in ips:
        IpRange = BuildHostRange(strHost)
        map(build_area_ip(area_name), range(IpRange[0], IpRange[1]+1))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def fff():
#     datas = Data.objects.all()
#     for d in datas:
#         try:
#             ip = getIp(d.uri)        
#         except Exception, e:
#             print e
#         else:
#             d.state="-1"
#             ip = ''
#         finally:
#             q=Ips.objects.filter(ip=ip)
#             if q :
#                 d.ip_s = q[0]
#             d.save()


if __name__ == '__main__':
    # put_into_ippool(result, u"龙湾")
    datas = Data.objects.filter(cate=None).exclude(state="-1")
    makeup_info_bulk(datas)
    # p = Pool(processes=4)utls
    # apply_async = p.apply_async

