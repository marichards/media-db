from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from defined_media.models import *

class CompoundsListView(ListView):
    model=Compounds
    paginate_by=50
    template_name='defined_media/compounds_list.html'
    def get_queryset(self, *args, **kwargs):
        ''' Trying to sort compounds by their first name '''
        #comps=list(Compounds.objects.all())
#        comps=list(Compounds.objects.all()[:50])

	#All compound IDs in media
	in_media = MediaCompounds.objects.values('compid').distinct()
	#Make a list of them
	id_list = []
	for item in in_media:
		id_list.append(item['compid'])
	#Filter for only those compounds
	comps = Compounds.objects.filter(pk__in=id_list)

        return sorted(comps, key=lambda c: c.name)


class MediaList(ListView):
    model=MediaNames
    paginate_by=100

    def get_queryset(self, *args, **kwargs):
        return MediaNames.objects.all().order_by('media_name')


class SourcesList(ListView):
    model=Sources
    paginate_by=100

    def get_queryset(self, *args, **kwargs):
        return Sources.objects.all().order_by('first_author')

class CompoundsDetail(DetailView):
    model=Compounds


class OrganismsListView(ListView):
    model=Organisms
    paginate_by=100

    def get_queryset(self, *args, **kwargs):
        return Organisms.objects.all().order_by('genus', 'species', 'strain')

class OrganismDetail(DetailView):
    model=Organisms

class MediaDetail(DetailView):
    model=MediaNames

    def get_context_data(self, **kwargs):
        context=super(MediaDetail,self).get_context_data(**kwargs)
        try:
            context['can_edit']=self.request.user.contributor.can_edit_mn(context['medianames'])
        except:
            context['can_edit']=False
        return context


class MediaText(View):
    template_name='defined_media/media_text.html'
    def get(self, request, *args, **kwargs):
        mn=get_object_or_404(MediaNames, **kwargs)
        return render(request, 
                      self.template_name, 
                      {'mn': mn, 'mcs': mn.media_compounds_dicts()},
                      content_type='text/plain',
                      )

class BiomassDetail(DetailView):
    model=Biomass

class BiomassList(ListView):
    model=Biomass

class BiomassText(View):
    template_name='defined_media/biomass_text.html'
    def get(self,request, *args, **kwargs):
	bn=get_object_or_404(Biomass, **kwargs)
	return render(request,
		      self.template_name,
		      {'bn': bn, 'bcs': bn.biomass_compounds_dicts()},
		      content_type='text/plain',
		      )    

class SourceDetail(DetailView):
    model=Sources


class GrowthDataListView(ListView):
    model=GrowthData
    paginate_by=100

    def get_queryset(self, *args, **kwargs):
        return GrowthData.objects.all().order_by('strainid__genus', 'medid__media_name')


class GrowthDataDetail(DetailView):
    model=GrowthData

    def get_context_data(self, **kwargs):
        context=super(GrowthDataDetail,self).get_context_data(**kwargs)
        try:
            context['can_edit']=self.request.user.contributor.can_edit_gd(context['growthdata'])
        except:
            context['can_edit']=False
        return context

