#encoding=utf-8
from django.db import models

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
    kword = models.CharField(max_length=32, null=True, blank=True)
    #分类
    cate = models.ForeignKey("Cate", null=True, blank=True)


class Cate(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)

    def __unicode__(self, ):
        return self.name

# class Iptable(models.Model):
#     """IP段"""
#     ip_zone = models.CharField(max_length=32, null=True, blank=True)


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
    uri = models.TextField(db_column='URI') # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True) # Field name made lowercase.
    descript = models.TextField(db_column='Descript', blank=True) # Field name made lowercase.
    
    cate = models.ForeignKey("Cate", null=True, blank=True)
    IPS = models.CharField(max_length=16, null=True, blank=True)
    #备案号
    # reg_number = models.IntegerField(blank=True, default=0, null=True)
    #备案类型
    # reg_type = models.CharField(max_length=16, null=True, blank=True)
    state = models.CharField(max_length=32, blank=True, choices=STATE_CHOICES, default='0')
    contact_name = models.CharField(max_length=32, null=True, blank=True)
    time = models.DateTimeField(blank=True, null=True)

    #备案信息
    icpno = models.CharField(max_length=32, blank=True, null=True)
    organizers_type = models.CharField(null=True, blank=True, max_length=64)
    exadate = models.DateTimeField(null=True, blank=True)
    #主办单位
    organizers = models.CharField(null=True, blank=True, max_length=64)

    class Meta:
        db_table = 'Data'
