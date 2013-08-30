#URLs file for defined media database
from django.conf.urls import patterns, url
#Include the views I've written
from defined_media import views

#URL Format:
#url(regex,view,*name,*kwargs)
#Regex defines the pattern for the url
#View defines which view to call for that page
#Kwargs is a keyword argument...not sure what to do with this
#Name lets you refer to it somewhere else, like a template 
#-->Powerful, lets you make global changes to url patterns

#Define ALL the urls!
urlpatterns = patterns('',
	#Simple Response url (Main Page)
	url(r'^$', views.main, name='main'),
	
	#Main Indices
	url(r'^compounds/$', views.compounds, name='compounds'),
	url(r'^organisms/$', views.organisms, name='organisms'),
	url(r'^media/$', views.media, name='media'),
	url(r'^biomass/$', views.biomass, name='biomass'),
	url(r'^sources/$', views.sources, name='sources'),

	#Record-Specific Views
	url(r'^compounds/(?P<compid>\d+)/$', views.compound_record, name='compound_record'),
	url(r'^organisms/(?P<strainid>\d+)/$', views.organism_record, name='organism_record'),
	url(r'^media/(?P<medid>\d+)/$', views.media_record, name='media_record'),
	url(r'^biomass/(?P<biomassid>\d+)/$', views.biomass_record, name='biomass_record'),
	url(r'^sources/(?P<sourceid>\d+)/$', views.source_record, name='source_record'),
)

#Define the Admin URL too, but in the main media_site directory

