from django.test import TestCase
from defined_media.models import *

class TestGrowthData(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gd_media_compounds(self):
        ''' '''
        for gd in GrowthData.objects.all():
            for d in gd.media_compounds_dicts():
                try:
                    print 'medcomp dicts: %s' % str(d)
                    comp=Compounds.objects.with_name(d['comp'])
                    amount=float(d['amount'])
                except:
                    self.fail()
                

    def test_gd_uptakes(self):
        for gd in GrowthData.objects.all():
            for d in gd.uptake_dicts():
                try:
                    print 'uptake dicts: %s' % str(d)
                    comp=Compounds.objects.with_name(d['comp'])
                    rate=float(d['rate'])
                    units=d['units']
                    typ=int(d['type'])
                except Exception as e:
                    self.fail(str(e))
