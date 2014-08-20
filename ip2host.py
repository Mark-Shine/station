# encoding: UTF-8
import re
import os
import struct
import socket
import pickle
import socket
import requests
import datetime
from multiprocessing import Pool
from time import sleep
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wenzhou.settings")
from cohost.models import Ips
from cohost.models import Data
from cohost.models import Area
from multiprocessing import Pool
from cohost.models import Ips
from cohost.utils import makeup_info_bulk, BuildHostRange

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
    for domain in domains:
        data, created = Data.objects.get_or_create(ip=ip, uri=domain, defaults={"time": now, })
        if created:
            makeup_info_bulk([data, ])
            print u"生成新的domain记录"
        else:
            print data.uri

def main():

    ips = Ips.objects.all()
    for obj in iter(ips):
        curip = obj.ip
        ip, res = f(curip)
        obj.active = '1'
        obj.save()
        if res:
            put_host(ip, res)
        else:
            print "error no data"


    # with Pool(4) as p:
    #     c = pool.map(f, ['42.120.194.11', "220.181.181.222", "123.125.114.144"])
    #     # query = {ip: aizhan_get_host(ip,) for ip in ['42.120.194.11', "220.181.181.222", "123.125.114.144"]}
    #     print (c)

def getIp(domain):
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    print(myaddr)

def put_ip(x):
    ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(x))))
    area, created = Area.objects.get_or_create(name=u"龙湾")
    Ips.objects.create(ip=ip, area=area)

#将ip放入数据库
def put_into_ippool(ips):
    # ips = read_from_ipbook()
    for strHost in ips:
        IpRange = BuildHostRange(strHost)
        map(put_ip, range(IpRange[0], IpRange[1]+1))


if __name__ == '__main__':
    put_into_ippool(result)
    main()
    # makeup_info_bulk()


