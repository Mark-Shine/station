#encoding=utf-8
from __future__ import absolute_import

import os
import sys
from celery.utils.log import get_logger
from celery import task
from celery import Celery
from django.conf import settings

from cohost.new_bing import do_bing
from cohost.utils import makeup_info_bulk

logger = get_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wenzhou.settings')


app = Celery('wenzhou',)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@task()
def ip_bing():
    """异步获取信息bing的信息， 任务在setting中设置"""
    do_bing()
    #bing获取的信息过滤，丰富
    makeup_info_bulk()
    