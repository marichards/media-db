from django.conf.urls import patterns, url
from registration.views import *
from django.contrib.auth.decorators import login_required, permission_required


view_prefix=''                  # Define ALL the urls!

urlpatterns = patterns(view_prefix,
                       # login and logout
                       url(r'^login/$',  login, name='login'),
                       url(r'^profile/$', login_required(user_profile), name='user_profile'),
                       url(r'^profile/(?P<username>\w+)', login_required(user_profile), name='user_profile'),
                       url(r'^logout/$', logout,  name='logout'),
                       url(r'^register/$', register_new_user, name='register_new_user'),
                       url(r'^forbidden/$', forbidden, name='forbidden'),
                       )
