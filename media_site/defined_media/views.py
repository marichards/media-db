# Views of Pages!
from django.http import HttpResponse
#Template Loader
from django.template import RequestContext, loader
#Shortcut to render templates and raise error if not there
from django.shortcuts import render,get_object_or_404

#Bring in models I might need
from defined_media.models import Compounds,MediaNames,MediaCompounds,Organisms,Sources,Biomass,BiomassCompounds,GrowthData
 
#Define the main page of the site
def main(request):
		
	#Put into basic template
	context = RequestContext(request, {

	})
	return render(request, 'defined_media/main.html', context)

	#Basic Return; Placeholder
	#return HttpResponse('This will be the main page someday!')

#Define the compounds index
def compounds(request):

	#List all the compounds, limit to 50 for now!
	compound_list = Compounds.objects.order_by('compid')[:50]

	#Put it into the template
	context = RequestContext(request, {
		'compound_list': compound_list,
	})
	return render(request, 'defined_media/compounds.html', context)

#Define the media index
def media(request):
	
	#List all the media, limit to 10 records for now!
	media_list = MediaNames.objects.order_by('media_name')[:10]
	
	#Put it into the template
	context = RequestContext(request, {
		'media_list': media_list,
	})
	return render(request, 'defined_media/media.html', context)

#Define the organisms index
def organisms(request):
	
	#List all the organisms, limit to 10 for now!
	organism_list = Organisms.objects.order_by('genus')[:10]

	#Put it into a template
	context = RequestContext(request, {
		'organism_list': organism_list,
	})
	return render(request, 'defined_media/organisms.html', context)

#Define the biomass index
def biomass(request):

	#List all the biomasses (there are only 4)
	biomass_list = Biomass.objects.order_by('genus')

	#Put it into a template
	context = RequestContext(request, {
		'biomass_list': biomass_list,
	})
	return render(request, 'defined_media/biomass.html', context)

#Define the sources index
def sources(request):
	
	#List all the sources, limit to 10 for now
	source_list = Sources.objects.order_by('first_author')[:10]

	#Put it into a template
	context = RequestContext(request, {
		'source_list': source_list,
	})
	return render(request, 'defined_media/sources.html', context)

#Define Record-Specific Compound View
def compound_record(request,compid):
	return HttpResponse('This is the page for compound %s.' %compid)

#Define Record-Specific Organisms View
def organism_record(request, strainid):
	return HttpResponse('This is the page for organism %s' %strainid)

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
	return HttpResponse('This is the page for source %s' %sourceid)
