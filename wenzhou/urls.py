from django.conf.urls import patterns, include, url

from django.contrib import admin
from cohost import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wenzhou.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^keywords$', views.show_kwords, name="keywords"),
    url(r'^data$', views.show_data, name="data"),
    url(r'^host/statechange$', views.show_data, name="change_host_state"),

    url(r'^admin/', include(admin.site.urls)),
)
