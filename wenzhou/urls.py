from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from cohost import views
from wzauth.views import LoginView, logoff
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wenzhou.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^error/permissions$', TemplateView.as_view() , {'template': 'error_perms.html'}, name="error_perms"),
    url(r'^login$', LoginView.as_view() , name="login"),
    url(r'^logoff$', logoff , name="logoff"),
    url(r'^keywords$', views.show_kwords, name="keywords"),
    url(r'^ips$', views.show_ips, name="ips"),
    url(r'^logs$', views.show_logs, name="logs"),
    url(r'^result$', views.show_result, name="result"),
    url(r'^areas$', views.show_areas, name="areas"),
    url(r'^areas/manage$', views.manage_area, name="manage_area"),
    url(r'^ip/search$', views.search_ip, name="search_ip"),
    url(r'^data/$', views.show_data, name="data"),
    url(r'^$', views.show_data, name="home"),
    url(r'^data/detail/(?P<pk>\d+)$', views.show_data_detail, name="detail"),
    url(r'^host/edit/(?P<pk>\d+)$', views.change_detail, name="change_detail"),

    url(r'^admin/', include(admin.site.urls)),
)
