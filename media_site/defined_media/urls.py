from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
import defined_media.views as views

view_prefix=''

urlpatterns = patterns(view_prefix,
                       #Simple Response url (Main Page)
                       url(r'^$', views.legacy.main, name='main'),
                       
                       #Main Indices

                       #url(r'^compounds/$', views.compounds, name='compounds'),
                       url(r'^compounds/$', views.core.CompoundsListView.as_view(), name='compounds'),
                       url(r'^compounds/page/(?P<page>\d+)', views.core.CompoundsListView.as_view(), name='compounds_paged'),
                       url(r'^organisms/$', views.core.OrganismsListView.as_view(), name='organisms'),
                       url(r'^organisms/page/(?P<page>\d+)', views.core.OrganismsListView.as_view(), name='organisms_paged'),
                       url(r'^media/$', views.core.MediaList.as_view(), name='media'),
                       url(r'^media/page/(?P<page>\d+)', views.core.MediaList.as_view(), name='media_paged'),

                       url(r'^biomass/$', views.legacy.biomass, name='biomass'),
                       url(r'^sources/$', views.core.SourcesList.as_view(), name='sources'),
                       url(r'^sources/page/(?P<page>\d+)', views.core.SourcesList.as_view(), name='sources_paged'),
                       url(r'^downloads/$', views.legacy.downloads, name='downloads'),

                       url(r'^growthdata/$', views.core.GrowthDataListView.as_view(), name='growthdata'),
                       url(r'^growthdata/page/(?P<page>\d+)', views.core.GrowthDataListView.as_view(), name='growthdata_paged'),


                       #Record-Specific Views
                       url(r'^compounds/(?P<pk>\d+)/$', views.core.CompoundsDetail.as_view(), name='compound_record'),
                       url(r'^organisms/(?P<pk>\d+)/$', views.core.OrganismDetail.as_view(), name='organism_record'),
                       url(r'^media/(?P<pk>\d+)/$', views.core.MediaDetail.as_view(), name='media_record'),
                       url(r'^biomass/(?P<pk>\d+)/$', views.core.BiomassDetail.as_view(), name='biomass_record'),
                       url(r'^sources/(?P<pk>\d+)/$', views.core.SourceDetail.as_view(), name='source_record'),

                       url(r'^growthdata/(?P<pk>\d+)/$', views.core.GrowthDataDetail.as_view(), name='growth_record'),

                       # Search views:
                       url(r'^search/$', views.search.SearchResultsView.as_view(), name='search'),
                       url(r'^search_results/$', views.search.SearchResultsView.as_view(), name='search_results'),

                       # New Media Contribution:
                       url(r'^newmedia/$', login_required(views.contributors.NewMediaView.as_view()), name='new_media_form'),
                       url(r'^newmedia/(?P<pk>\d+)/$', login_required(views.contributors.NewMediaView.as_view()), name='new_media_form'),
                       url(r'^clone_newmedia/(?P<pk>\d+)/$', login_required(views.clone.CloneGrowthDataView.as_view()), name='clone_growth_data'),

                       # REST api
                       url(r'^api/urlmap$', views.api.urlmap, name='urlmap'),
                       url(r'^api/organism$', views.api.OrganismsView.as_view(), name='organism_api'),
                       url(r'^api/organism/(?P<genus>\w+)$', views.api.OrganismsView.as_view(), name='organism_api'),
                       url(r'^api/organism/(?P<genus>\w+)/(?P<species>\w+)/$', views.api.OrganismsView.as_view(), name='organism_api'),
                       url(r'^api/organism/(?P<genus>\w+)/(?P<species>\w+)/(?P<strain>\w+)/$', views.api.OrganismsView.as_view(), name='organism_api'),

                       url(r'^api/pmid/$', views.api.efetch_pmid, name='efetch_pmid'),
                       url(r'^api/pmid/(?P<pmid>\d+)$', views.api.efetch_pmid, name='efetch_pmid'),

                       url(r'^api/growthdata/(?P<pk>\d+)/$', views.api.growth_data_view, name='growth_data_api'),

# old function-based views:
#                       url(r'^organisms/$', views.organisms, name='organisms'),
#                       url(r'^media/$', views.media, name='media'),
#                       url(r'^sources/$', views.sources, name='sources'),
#                       url(r'^compounds/(?P<compid>\d+)/$', views.compound_record, name='compound_record'),
#                       url(r'^organisms/(?P<strainid>\d+)/$', views.organism_record, name='organism_record'),
#                       url(r'^media/(?P<medid>\d+)/$', views.media_record, name='media_record'),
#                       url(r'^biomass/(?P<biomassid>\d+)/$', views.biomass_record, name='biomass_record'),
#                       url(r'^sources/(?P<sourceid>\d+)/$', views.source_record, name='source_record'),

                       )

#Define the Admin URL too, but in the main media_site directory

