#encoding=utf-8
from __future__ import absolute_import

import os
import sys
from celery.utils.log import get_logger
from celery import task
from celery import Celery
from django.conf import settings

from cohost.new_bing import *
from cohost.utils import makeup_info_bulk

logger = get_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wenzhou.settings')


app = Celery('wenzhou',)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@task()
def add(x, y):
    sys.stdout.write('hello'+'\n')
    return x + y

@task()
def ip_bing():
    """异步获取信息bing的信息， 任务在setting中设置"""
    keyInfo=GetAccountKey()
    AccountKey =keyInfo[1]
    useCounts=keyInfo[2]
    bSave = True
    nType = 1
    p = Pool(processes=4)
    now = time.time()
    for strHost in result:
        IpRange=BuildHostRange(strHost)
        r = p.map_async(f, range(IpRange[0],IpRange[1]+1), callback=ViewResult)
        r.wait()
    end = time.time()
    print (end-now)
    makeup_info_bulk()
    