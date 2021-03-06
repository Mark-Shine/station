# encoding: UTF-8
import sys
import re
import os
import struct
import socket
import pickle
import socket
import requests
import datetime
from logging import getLogger, FileHandler
from multiprocessing import Pool
from time import sleep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wenzhou.settings")
from cohost.models import Ips
from cohost.models import Data
from cohost.models import Area
from multiprocessing import Pool
from cohost.models import Ips
from cohost.utils import makeup_info_bulk, BuildHostRange, get_host_infos, put_into_ippool

logger = getLogger("trace")
file_handler = FileHandler("bing_ip.log")
logger.addHandler(file_handler)  



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

# with open("ips.txt") as text

AIZHAN_HEADERS = {
        "Connection":"keep-alive",
        "Host":"dns.aizhan.com",
        "Referer": "http://dns.aizhan.com/", 
        "User-Agent":'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Chrome/17.0.963.56 Fedora/3.0.1-1.fc9 Firefox/3.0.1',
        "Accept-Encoding":"gzip,deflate,sdch",
        "X-Requested-With":"XMLHttpRequest"}

def gen_ip2host(query_url, keyword, **kwards):
    headers = kwards.get("headers", "")
    def get_host(ip, **kwards):
        params = {"ip": ip}
        params.update(kwards)
        res = requests.get(query_url, params=params, headers=headers)
        json_data = res.json()
        sleep(5)
        return json_data and  json_data.get(keyword) or ""
    return get_host

def f(ip):
    url = "http://dns.aizhan.com/index.php?r=index/domains"
    aizhan_get_host = gen_ip2host(url, "domains", **{"headers": AIZHAN_HEADERS})
    return ip, aizhan_get_host(ip)


def put_host(ip, domains):
    now = datetime.datetime.now()
    ip_q = Ips.objects.filter(ip=ip)
    ip = ip_q and ip_q[0]
    if not ip:
        print u"ip not in pool"
        return 
    for domain in domains:
        data, created = Data.objects.get_or_create(ips_id=ip, uri=domain, defaults={"time": now, })
        if created:
	    print u"insert new domain"
            sys.stdout.flush()

def main():
    ips = Ips.objects.all()
    print ips.count()
    for obj in iter(ips):
        curip = obj.ip
        print u"get ip :%s " %(curip)        
        try:
            ip, res = f(curip)
        except Exception, e:
            print e
        finally:
            pass
        obj.active = '1'
        if res:
            put_host(ip, res)
	    print "get domains : %s" %res
        else:
            print "error no data"
        obj.save()
        sys.stdout.flush()

def getIp(domain):
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    print(myaddr)


if __name__ == '__main__':
    Ips.objects.filter(active='1').update(active='0')
    main()
    datas = Data.objects.filter(cate=None).exclude(state="-1")
    makeup_info_bulk(datas)    
    # makeup_info_bulk()




