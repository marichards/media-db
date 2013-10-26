from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from defined_media.models import *

class CompoundsListView(ListView):
    model=Compounds
    paginate_by=100
    
    def get_queryset_broken(self, *args, **kwargs):
        ''' Trying to sort compounds by their first name '''
        comps=list(Compounds.objects.all()[:50])
        return sorted(comps, key=lambda c: c.keywords()[0])



class MediaList(ListView):
    model=MediaNames
    paginate_by=100

    def get_queryset(self, *args, **kwargs):
        return MediaNames.objects.all().order_by('media_name')


class SourcesList(ListView):
    model=Sources
    paginate_by=100


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

class BiomassDetail(DetailView):
    model=Biomass

class SourceDetail(DetailView):
    model=Sources


class GrowthDataListView(ListView):
    model=GrowthData
    paginate_by=100

    def get_queryset(self, *args, **kwargs):
        return GrowthData.objects.all().order_by('strainid__genus', 'medid__media_name')


class GrowthDataDetail(DetailView):
    model=GrowthData

