from django.conf.urls import patterns, url
from registration.views import *


view_prefix=''                  # Define ALL the urls!

urlpatterns = patterns(view_prefix,
                       # login and logout
                       url(r'^login/$',  login, name='login'),
                       url(r'^accounts/profile/$', user_profile, name='user_profile'),
                       url(r'^accounts/profile/(?P<username>\w+)', user_profile, name='user_profile'),
                       url(r'^logout/$', logout,  name='logout'),
                       url(r'^register/$', register_new_user, name='register_new_user'),
                       )
