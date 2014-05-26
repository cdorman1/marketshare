from django.conf.urls import patterns, include, url
from django.contrib import admin
from marketshare.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'appsuite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^index/',index,name="index"),
    url(r'^listpage/',listpage,name="listpage"),
    url(r'^dashboard/',dashboard,name="dashboard"),
    url(r'^logout/',dologout,name="logout")
)
