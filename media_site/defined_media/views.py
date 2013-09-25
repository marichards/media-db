# Views of Pages!
from django.http import HttpResponse
#Template Loader
from django.template import RequestContext, loader
#Shortcut to render templates and raise error if not there
from django.shortcuts import render,get_object_or_404

#Bring in models I might need
from defined_media.models import Compounds,MediaNames,MediaCompounds,Organisms,Sources,Biomass,BiomassCompounds,GrowthData, SearchResult

from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse


 
#Define the main page of the site
def main(request):
		
	#Put into basic template
	context = {
	}
	return render(request, 'defined_media/main.html', context)

	#Basic Return; Placeholder
	#return HttpResponse('This will be the main page someday!')

#Define the compounds index
def compounds(request):
	print 'compounds() called'
	#List all the compounds, limit to 50 for now!
	compound_list = Compounds.objects.order_by('compid')[:50]

	#Put it into the template
	context = {
		'compound_list': compound_list,
	}
	return render(request, 'defined_media/compounds.html', context)


class CompoundsListView(ListView):
	model=Compounds
	paginate_by=100


#Define the media index
def media(request):
	
	#List all the media, limit to 10 records for now!
	media_list = MediaNames.objects.order_by('media_name')[:10]
	
	#Put it into the template
	context = {
		'media_list': media_list,
	}
	return render(request, 'defined_media/media.html', context)

#Define the organisms index
def organisms(request):
	
	#List all the organisms, limit to 10 for now!
	organism_list = Organisms.objects.order_by('genus')[:10]

	#Put it into a template
	context ={
		'organism_list': organism_list,
	}
	return render(request, 'defined_media/organisms.html', context)

#Define the biomass index
def biomass(request):

	#List all the biomasses (there are only 4)
	biomass_list = Biomass.objects.order_by('genus')

	#Put it into a template
	context = {
		'biomass_list': biomass_list,
	}
	return render(request, 'defined_media/biomass.html', context)

#Define the sources index
def sources(request):
	
	#List all the sources, limit to 10 for now
	source_list = Sources.objects.order_by('first_author')[:10]

	#Put it into a template
	context = {
		'source_list': source_list,
	}
	return render(request, 'defined_media/sources.html', context)

#Define the downloads page
def downloads(request):
	
	#Return something dumb for now
	return HttpResponse('This page houses the downloads')

#Define Record-Specific Compound View
def compound_record(request,compid):

	#Pick out the compound object here
	compound = get_object_or_404(Compounds, compid=compid)
	#Grab the names of the compound
	names_list = compound.namesofcompounds_set.all() 	

	context ={
		'compound': compound,
		'names_list': names_list,
	}
        
	return render(request, 'defined_media/compound_record.html', context)

#Define Record-Specific Organisms View
def organism_record(request, strainid):

	#Pick out the organism object
	organism = get_object_or_404(Organisms, strainid=strainid)
	#Put in context
	context = {
		'organism': organism,
	}

	return render(request, 'defined_media/organism_record.html', context)

#Define Record-Specific Media View
def media_record(request, medid):
	#Simple Response...let's do something more fun!
#	return HttpResponse('This is the page for media %s' %medid)
	
	#Grab that media record like in the model file
	#Specify the media name
	#Use shortcut for Raise404
	media_name = get_object_or_404(MediaNames,medid=medid).media_name.capitalize()
	#Find the list of compounds for a medium
	compound_list = MediaCompounds.objects.filter(medid=medid)
	#Create context for template
	context = {
		'compound_list': compound_list,
		'media_name': media_name
	}
	#Shortcut method puts context into template
	return render(request, 'defined_media/media_record.html', context)

#Define Record-Specific Biomass View
def biomass_record(request, biomassid):
	#Copy the media record one

	biomass_name = get_object_or_404(Biomass,biomassid=biomassid).genus.capitalize()
	#Find the list of compounds for a biomass composition
	compound_list = BiomassCompounds.objects.filter(biomassid=biomassid)
	#Create context for template
	context = {
		'compound_list': compound_list,
		'biomass_name': biomass_name
	}
	return render(request, 'defined_media/biomass_record.html', context)

#Define Record-Specific Source View
def source_record(request, sourceid):
	#Fish out the source object
	source = get_object_or_404(Sources, sourceid=sourceid)
	#Create context
	context = {
		'source': source,
	}
	return render(request, 'defined_media/source_record.html', context)

from defined_media.forms import SearchForm
class SearchView(FormView):
	form_class=SearchForm
	template_name='defined_media/searchresult_list.html'

class SearchResultsView(ListView, FormView):
	template_name='defined_media/searchresult_list.html'

	def get(self, request, *args, **kwargs):

		form_class=SearchForm
		form=self.get_form(form_class)

		self.object_list=[]
		c={'form':form, 'object_list':self.object_list}
		st=self._get_search_term()
		if st:
			self.object_list=self.get_queryset()
			c.update({'object_list' : self.object_list,
				  'search_term' : st})
				  
		context=self.get_context_data(**c)
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)

	def get_queryset(self):
		st=self._get_search_term()
		return SearchResult.objects.filter(keyword__contains=st).order_by('keyword')
						   

	def _get_search_term(self):
		try:
			return self.request.POST['search_term'].lower()
		except KeyError:
			try: return self.request.GET['search_term'].lower()
			except KeyError:
				return None
		
