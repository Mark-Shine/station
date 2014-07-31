#encoding=utf-8
from django.db import models

# Create your models here.
class Keywords(models.Model):
    #关键字
    kword = models.CharField(max_length=32, null=True, blank=True)
    #分类
    cate = models.ForeignKey("Cate", null=True, blank=True)


class Cate(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)


# class Iptable(models.Model):
#     """IP段"""
#     ip_zone = models.CharField(max_length=32, null=True, blank=True)


class Allkey(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True) # Field name made lowercase.
    bactive = models.IntegerField(db_column='bActive') # Field name made lowercase.
    keyname = models.TextField(db_column='KeyName', unique=True) # Field name made lowercase.
    visitmonth = models.IntegerField(db_column='VisitMonth', blank=True, null=True) # Field name made lowercase.
    usecount = models.IntegerField(db_column='UseCount', blank=True, null=True) # Field name made lowercase.
    
    class Meta:
        db_table = 'AllKey'


class Data(models.Model):
    def __unicode__(self,):
        return "ip: %s - uri: %s" %(self.ip, self.uri)

    STATE_CHOICES = (
    ('0', '未处理'),
    ('1', '无违规'),
    ('2', '涉嫌违规'),
    ('3', '重点监管'),
    ('4', '处理'),
    ('5', '非管辖'),)

    id = models.IntegerField(db_column='ID', primary_key=True, blank=True) # Field name made lowercase.
    ip = models.TextField(db_column='IP') # Field name made lowercase.
    uri = models.TextField(db_column='URI') # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True) # Field name made lowercase.
    descript = models.TextField(db_column='Descript', blank=True) # Field name made lowercase.
    
    cate = models.ForeignKey("Cate", null=True, blank=True)
    IPS = models.CharField(max_length=16, null=True, blank=True)
    #备案号
    reg_number = models.IntegerField(blank=True, default=0)
    #备案类型
    reg_type = models.CharField(max_length=16, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True, choices=STATE_CHOICES, default='0')
    contact_name = models.CharField(max_length=32, null=True, blank=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Data'
