from rest_framework import generics
from defined_media.models import Organisms
from defined_media.serializers import OrganismSerializer
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json

def urlmap(request):
    ''' make certain url mappings available as json, so jQuery can use them '''
    urlmap={}
    for viewname in ['organism_api']:
        urlmap[viewname]=reverse(viewname)
    print json.dumps(urlmap)
    return HttpResponse(json.dumps(urlmap), mimetype='application/json')


class OrganismsView(generics.ListAPIView):
    model=Organisms
    serializer_class=OrganismSerializer
    
    def get_queryset(self):
        args={}
        for arg in ['genus', 'species', 'strain']:
            if arg in self.kwargs:
                args[arg]=self.kwargs[arg]
        orgs=Organisms.objects.filter(**args)

        return orgs
