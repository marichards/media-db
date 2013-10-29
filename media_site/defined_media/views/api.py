from rest_framework import generics
from defined_media.models import Organisms
from defined_media.serializers import OrganismSerializer
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
import json, requests

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

def efetch_pmid(request, *args, **kwargs):
    ''' return JSON fetched from pubmed for the given pubmed id '''
    try:
        pmid=int(kwargs['pmid'])
    except KeyError:
        try:
            if request.method.lower()=='get':
                pmid=request.GET['pmid']
            elif request.method.lower()=='post':
                pmid=request.POST['pmid']
        except KeyError:
            raise Http404('pubmed id not supplied')
    except ValueError:
        raise Http404('%s does not appear to be a valid pubmed id' % pmid)

    data={'pmid':pmid,
          'authors':[],
          'title':None,
          'journal':None,
          'date':None,
          'link':'http://www.ncbi.nlm.nih.gov/pubmed/?term=%d' % pmid}
    url='http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%d&rettype=medline' % pmid
    r=requests.get(url)
    if r.status_code != 200:
        raise Http404('nothing found for pmid=%d' % pmid)
    
    c2f={'TI':'title',
         'JT':'journal',
         'DP':'date'}
    
    if 'Error occurred: The following PMID is not available:' in r.content:
        data['error']='nothing found for pmid=%d' % pmid
    else:
        for line in r.content.split('\n'):
            try: (code,value)=line.split(' - ')
            except ValueError: continue
            
            code=code.strip()
            try:
                key=c2f[code]
                data[key]=value
            except KeyError:
                if code=='AU':
                    data['authors'].append(value)
    
    return HttpResponse(json.dumps(data), mimetype='application/json')

