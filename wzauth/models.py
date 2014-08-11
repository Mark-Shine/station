#encoding=utf-8
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save

from cohost.models import Area

# Create your models here.


class WzUser(models.Model):
    user = models.OneToOneField(User)
    is_admin = models.BooleanField('admin status', default=False,)
    #一个员工可以管理多个区域
    area = models.ManyToManyField(Area, null=True, blank=True)

    def __unicode__(self,):
        return u"用户：%s-%s" %(self.user.id, self.user.username)



    class Meta:
        db_table = 'wzuser'
        verbose_name = u"区域管理员信息"
        verbose_name_plural = u"区域管理员信息"
        permissions = (
            ("can_see_log", u"查看日志"),
            ("can_manage_area", u"管理区域"),
        )

# class ActionRecord(models.Model):
#     # rd_name = models.CharField()
#     pass