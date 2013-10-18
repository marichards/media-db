from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from defined_media.views import df_login, df_logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from defined_media.views import main

import defined_media.views


urlpatterns = patterns('',
                       # Examples:

                       url(r'^$', defined_media.views.main, name='home'),
                       
                       # url(r'^media_site/', include('media_site.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       # I added this to point to the defined_media app
                       url(r'^defined_media/', include('defined_media.urls')), 

                       # login and logout
                       url(r'^login/$',  df_login, name='login'),
                       url(r'^logout/$', df_logout, name='logout'),
                       )
