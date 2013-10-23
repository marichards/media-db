from django.shortcuts import render
from django.http import HttpResponse
from defined_media.models import *
 
#Define the main page of the site
def main(request):
		
	#Put into basic template
	context = {
	}
	return render(request, 'defined_media/main.html', context)

	#Basic Return; Placeholder
	#return HttpResponse('This will be the main page someday!')

#Define the growth index
def growth(request):

	#List all the growth conditions, limit to 50 for now
	growth_list = GrowthData.objects.order_by('growthid')[:50]

	#Put into template
	context = {
		'growth_list': growth_list,
	}
	return render(request, 'defined_media/growth.html', context)

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

#Define the growth record page
def growth_record(request, growthid):

	#Grab the growth object
	growth = get_object_or_404(GrowthData, growthid=growthid)
	#Grab the name of the strain
	#First grab strainid...right now this is the name, so leave it
	organism = growth.strainid
	#Grab the name of the media...this is also the name, so leave it
	media = growth.medid
	#Put into template
	context = {
		'media': media,
		'organism': organism,
		'growth': growth,
	}

	return render(request, 'defined_media/growth_record.html', context)

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
