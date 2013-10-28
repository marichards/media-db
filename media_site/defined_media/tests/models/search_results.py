from django.test import TestCase
from defined_media.models import SearchResult, Organisms

class SearchResultTestCase(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def test_search_result_unicode(self):
        '''
        for sr in SearchResult.objects.all():
            print repr(sr)

        for o in Organisms.objects.all():
            print 'id=%d: %s' % (o.strainid, repr(o))
        '''

        sr=SearchResult(keyword='Acinetobacter', classname='Organisms', obj_id=9)
        print str(sr)

