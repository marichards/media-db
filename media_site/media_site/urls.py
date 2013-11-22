from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

#from defined_media.views import df_login, df_logout, CreateContributor

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from defined_media.views.legacy import main
from views import user_profile



urlpatterns = patterns('',
                       url(r'^$', main, name='home'),
                       # Uncomment the admin/doc line below to enable admin documentation:
                           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       # defined_media/urls.py
                       url(r'^defined_media/', include('defined_media.urls')), 
                       url(r'', include('registration.urls')), 
                       )

