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
    url(r'^api/ip_info$', views.new_api_get_ip_info , name="get_ip_info"),
    url(r'^logs/$', views.show_logs, name="logs"),

    # url(r'^error/permissions$', TemplateView.as_view() , {'template': 'error_perms.html'}, name="error_perms"),
    url(r'^login$', LoginView.as_view() , name="login"),
    url(r'^logoff$', logoff , name="logoff"),
    
    url(r'^keywords$', views.show_kwords, name="keywords"),
    url(r'^ips$', views.show_ips, name="ips"),
    url(r'^result$', views.show_result, name="result"),
    url(r'^areas$', views.show_areas, name="areas"),
    url(r'^areas/manage$', views.manage_area, name="manage_area"),

    url(r'^ip/search$', views.search_ip, name="search_ip"),
    url(r'^ip/config$', views.ips_config, name="ips_config"),
    url(r'^ip/add$', views.add_ips, name="add_ips"),

    url(r'^data/$', views.show_data, name="data"),
    url(r'^$', views.show_home, name="home"),
    url(r'^data/detail/(?P<pk>\d+)$', views.show_data_detail, name="detail"),
    url(r'^data/detail/(?P<pk>\d+)/editform$', views.edit_data, name="edit_data"),
    url(r'^data/(?P<pk>\d+)/edit$', views.change_detail, name="change_detail"),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls), ),
)
