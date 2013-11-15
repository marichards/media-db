from rest_framework import generics
from defined_media.models import Organisms, GrowthData
from defined_media.serializers import OrganismSerializer, GrowthDataSerializer
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.core import serializers

import json, requests, re, logging

log=logging.getLogger(__name__)

def urlmap(request):
    ''' make certain url mappings available as json, so jQuery can use them '''
    urlmap={}
    for viewname in ['organism_api', 'efetch_pmid']:
        urlmap[viewname]=reverse(viewname)
    return HttpResponse(json.dumps(urlmap), mimetype='application/json')


class OrganismsView(generics.ListAPIView):
    model=Organisms
    serializer_class=OrganismSerializer
    
    def get_queryset(self):
        args={}
        for arg in ['genus', 'species', 'strain']:
            if arg in self.kwargs:
                args[arg]=self.kwargs[arg]
        return Organisms.objects.filter(**args)


def growth_data_view(request, *args, **kwargs):
    gd=GrowthData.objects.get(pk=kwargs['pk'])
    strain=gd.strainid
    gd_json=serializers.serialize('json', [gd, strain], indent=4)
#        med_comp=gd.medid
#        source=gd.sourceid
#        return (gd, strain, med_comp, source)
    return HttpResponse(gd_json, mimetype='application/json')


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
          'author':'',
          'title':'',
          'journal':'',
          'year':'',
          'link':'http://www.ncbi.nlm.nih.gov/pubmed/?term=%d' % pmid}
    url='http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%d&rettype=medline' % pmid
    r=requests.get(url)
    log.debug('pmid=%s: status_code from pubmed is %d' % (pmid, r.status_code))
    if r.status_code != 200:
        raise Http404('nothing found for pmid=%d' % pmid)
    
    c2f={'TI':'title',
         'JT':'journal'}
    
    if 'Error occurred: The following PMID is not available:' in r.content:
        log.debug('pmid %s not available, 404-ing' % pmid)
        raise Http404('nothing found for pmid=%d' % pmid)
#        data['error']='nothing found for pmid=%d' % pmid
    else:
        last_code=None
        for line in r.content.split('\n'):
#            print line
            try: (code,value)=line.split(' - ')
            except ValueError: 
                if last_code==None:
                    continue
                code=last_code
                value=' '+line.strip()
            
            code=code.strip()
            if code=='TI' or code == 'JT':
                key=c2f[code]
                data[key]+=value
            elif code=='DP':
                mg=re.search(r'19\d\d|20\d\d', value) # this seems error-prone
                if mg:
                    year=mg.group(0)
                    print 'year is ' + year
                    data['year']=year
            elif code=='AU':
                if not data['author']:
                    data['author']=value
            last_code=code
    
    print 'efetch: data is %s' % data
    return HttpResponse(json.dumps(data), mimetype='application/json')

