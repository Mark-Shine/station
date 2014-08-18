#encoding=utf-8
import datetime
import time
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from cohost.signals import action_message

STATE_CHOICES = (
    ('0',u'未处理'),
    ('1', u'无违规'),
    ('2', u'涉嫌违规'),
    ('3', u'重点监管'),
    ('4', u'处理'),
    ('6', u'域名更新'),
    ('5', u'非管辖'),)

# Create your models here.
class Keywords(models.Model):
    #关键字
    kword = models.CharField(u"关键字", max_length=32, null=True, blank=True)
    #分类
    cate = models.ForeignKey("Cate", null=True, blank=True, verbose_name=u"相关分类")

    class Meta:
        verbose_name_plural = u"匹配关键字"

    def __unicode__(self, ):
        return self.kword

class Cate(models.Model):
    name = models.CharField(u"分类", max_length=64, null=True, blank=True)

    def __unicode__(self, ):
        return self.name

    class Meta:
        verbose_name_plural = u"分类"


class Allkey(models.Model):
    # id = models.IntegerField(db_column='ID', primary_key=True, blank=True) # Field name made lowercase.
    bactive = models.IntegerField(db_column='bActive') # Field name made lowercase.
    keyname = models.CharField(db_column='KeyName', unique=True, max_length=128) # Field name made lowercase.
    visitmonth = models.IntegerField(db_column='VisitMonth', blank=True, null=True) # Field name made lowercase.
    usecount = models.IntegerField(db_column='UseCount', blank=True, null=True) # Field name made lowercase.
    
    class Meta:
        db_table = 'AllKey'


class Data(models.Model):
    def __unicode__(self,):
        return "ip: %s - uri: %s" %(self.ip, self.uri)

    # id = models.IntegerField(db_column='ID', primary_key=True, blank=True) # Field name made lowercase.
    ip = models.TextField(db_column='IP') # Field name made lowercase.
    uri = models.TextField(u"域名", db_column='URI') # Field name made lowercase.
    title = models.TextField(u"标题", db_column='Title', blank=True) # Field name made lowercase.
    descript = models.TextField(db_column='Descript', blank=True) # Field name made lowercase.
    
    IPS = models.CharField(u"运营商", max_length=16, null=True, blank=True)
    #备案号
    # reg_number = models.IntegerField(blank=True, default=0, null=True)
    #备案类型
    # reg_type = models.CharField(max_length=16, null=True, blank=True)
    state = models.CharField(u"状态", max_length=32, blank=True, choices=STATE_CHOICES, default='0')
    contact_name = models.CharField(max_length=32, null=True, blank=True)
    time = models.DateTimeField(blank=True, null=True)

    #备案信息
    icpno = models.CharField(u"备案号", max_length=32, blank=True, null=True)
    organizers_type = models.CharField(u"组织机构类型", null=True, blank=True, max_length=64)
    exadate = models.DateTimeField(u"过期时间", null=True, blank=True)
    #主办单位
    organizers = models.CharField(u"组织机构", null=True, blank=True, max_length=64)
    cate = models.ForeignKey("Cate", null=True, blank=True,  verbose_name=u"分类")
    area = models.ForeignKey("Area", null=True, blank=True,  verbose_name=u"区域")
    #备注
    beizhu = models.TextField(blank=True, null=True,)
    #适应法律条文
    related_law = models.ForeignKey("LawRecord", null=True, blank=True,  verbose_name=u"相关条文")
    class Meta:
        verbose_name_plural = u"IP域名信息"
        db_table = 'Data'

class Area(models.Model):
    #区域名称
    def __unicode__(self,):
        return "%s" %(self.name)

    name = models.CharField(u"区域", max_length=64, blank=True, null=True)
    class Meta:
        verbose_name_plural = u"区域"


class Ippiece(models.Model):
    """IP片段"""
    piece = models.CharField(u"IP段", max_length=64, blank=True, null=True)
    area = models.ForeignKey("Area", null=True, blank=True, verbose_name=u"区域")


class DataActionRecord(models.Model):
    """用户处理data记录表"""
    data = models.ForeignKey("Data", null=True, blank=True)
    action = models.CharField(max_length=24, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)


    @receiver([action_message],)
    def record_handel(sender=None, user=None, instance=None, action=None, **kwargs): 
        form = {}
        form['user'] = user
        form['data'] = instance
        form['time'] =  timezone.localtime(timezone.now())
        form['action'] = action
        acrecord, created = DataActionRecord.objects.get_or_create(**form)


class Ips(models.Model):
    """IP库"""
    ip = models.IPAddressField(null=True, blank=True)
    


class LawRecord(models.Model):
    class Meta:
        verbose_name_plural = u"相关条文"

    def __unicode__(self):
        return self.law

    #todo 添加详细说明 lanmu 
    law = models.TextField(u"条文", null=True, blank=True, )
    #详细
    detail = models.TextField(u"详细", null=True, blank=True, )
    time = models.DateTimeField(null=True, blank=True)



