from django.conf.urls import patterns, url
from registration.views import *

#URL Format:
#url(regex,view,*name,*kwargs)
#Regex defines the pattern for the url
#View defines which view to call for that page
#Kwargs is a keyword argument...not sure what to do with this
#Name lets you refer to it somewhere else, like a template 
#-->Powerful, lets you make global changes to url patterns

#Define ALL the urls!
view_prefix=''

urlpatterns = patterns(view_prefix,
                       # login and logout
                       url(r'^login/$',  login2, name='login'),
                       url(r'^accounts/profile/$', user_profile, name='user_profile'),
                       url(r'^accounts/profile/(?P<username>\w+)', user_profile, name='user_profile'),
                       url(r'^logout/$', logout,  name='logout'),
                       url(r'^register/$', register_new_user, name='register_new_user'),
                       )
