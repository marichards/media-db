# Create your views here.

from django.http import HttpResponse

#Define the main page of the site
def main(request):
	return HttpResponse('This will be the main page someday!')

#Define the compounds index
def compounds(request):
	return HttpResponse('This is the main compounds index')

#Define the media index
def media(request):
	return HttpResponse('This is the main media index')

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
	return HttpResponse('This is the page for media %s' %medid)

#Define Record-Specific Biomass View
def biomass_record(request, biomassid):
	return HttpResponse('This is the page for biomass %s' %biomassid)

#Define Record-Specific Source View
def source_record(request, sourceid):
	return HttpResponse('This is the page for source %s' %sourceid)
