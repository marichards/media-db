from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

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
)
