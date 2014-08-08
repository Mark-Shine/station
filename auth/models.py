#encoding=utf-8
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save

# Create your models here.


class WzUser(models.Model):
    user = models.OneToOneField(User)
    is_admin = models.BooleanField('admin status', default=False,)


    def __unicode__(self,):
        return u"用户：%s-%s" %(self.user.id, self.user.username)

    class Meta:
        verbose_name = "WzUser"
        verbose_name_plural = "WzUser"

        permissions = (
            ("can_see_log", u"查看日志"),
            ("can_do_stuff", u"处理相应的IP"),
            ("can_add_keyword", u"添加关键字"),
        )


class ActionRecord(models.Model):
    # rd_name = models.CharField()
    pass