# encoding: UTF-8
import re
import pickle
import socket
import requests
from multiprocessing import Pool
from time import sleep
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wenzhou.settings")
from cohost.models import Ips
from cohost.models import Data
    
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
        return json_data.get(keyword)
    return get_host

def f(ip):
    url = "http://dns.aizhan.com/index.php?r=index/domains"
    aizhan_get_host = gen_ip2host(url, "domains", **{"headers": AIZHAN_HEADERS})
    return ip, aizhan_get_host(ip)


def main():
    with Pool(4) as pool:
        c = pool.map(f, ['42.120.194.11', "220.181.181.222", "123.125.114.144"])
        # query = {ip: aizhan_get_host(ip,) for ip in ['42.120.194.11', "220.181.181.222", "123.125.114.144"]}
        print (c)

def getIp(domain):
    import socket
    myaddr = socket.getaddrinfo(domain,'http')[0][4][0]
    print(myaddr)


if __name__ == '__main__':
    main()


