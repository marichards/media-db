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
	#Basic Return; Placeholder
	return HttpResponse('This will be the main page someday!')

#Define the compounds index
def compounds(request):
	return HttpResponse('This is the main compounds index')

#Define the media index
def media(request):
	
	#List all the media, limit to 10 records for now!
	media_list = MediaNames.objects.order_by('media_name')[:10]
	
	#Put it into the template
	template = loader.get_template('defined_media/media.html')
	context = RequestContext(request, {
		'media_list': media_list,
	})
	return HttpResponse(template.render(context))

#Define the organisms index
def organisms(request):
	return HttpResponse('This is the main organisms index')

#Define the biomass index
def biomass(request):
	return HttpResponse('This is the main biomass index')

#Define the sources index
def sources(request):
	return HttpResponse('This is the main sources index')

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
	media_name = MediaNames.objects.get(medid=medid).media_name.capitalize()
	#Find the list of compounds for a medium
	compound_list = MediaCompounds.objects.filter(medid=medid)
	#Create context for template
	context = {
		'compound_list': compound_list,
		'media_name': media_name
	}
	#Shortcut method puts context into template
	return render(request, 'defined_media/media_record.html',context)

#Define Record-Specific Biomass View
def biomass_record(request, biomassid):
	return HttpResponse('This is the page for biomass %s' %biomassid)

#Define Record-Specific Source View
def source_record(request, sourceid):
	return HttpResponse('This is the page for source %s' %sourceid)
