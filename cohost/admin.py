from django.contrib import admin
from cohost.models import Data, Keywords, Cate, Area, LawRecord,Ips,Area


# admin.site.register(Ips)
admin.site.register(Area)
admin.site.register(LawRecord)
admin.site.register(Cate)
admin.site.register(Keywords)

# Register your models here.
