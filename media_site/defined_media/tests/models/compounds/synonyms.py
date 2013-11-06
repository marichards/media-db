from django.test import TestCase
from defined_media.models import *

#from django.test.client import Client
#from django.core.urlresolvers import reverse

class TestSynonyms(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
#        self.client=Client()
        pass
    def tearDown(self):
        pass

    def test_real_name(self):
        h2o=Compounds.objects.with_name('H2O')
        self.assertEqual(h2o.compid, 1)

    def test_synonyms(self):
        h2o=Compounds.objects.with_name('water')
        self.assertEqual(h2o.compid, 1)

        comp8=Compounds.objects.with_name('Glyoxalate')
        self.assertEqual(comp8.compid, 48)

        coa=Compounds.objects.with_name('coenzyme a')
        self.assertEqual(coa.compid, 10)
        coa=Compounds.objects.with_name('CoA-SH')
        self.assertEqual(coa.compid, 10)

    def test_unknown(self):
        self.assertRaises(Compounds.DoesNotExist,
                          Compounds.objects.with_name, 
                          ('unknown does not exist null nope non nyet'))

    def test_regular_methods(self):
        comps=Compounds.objects.filter(compid__lt=20)
        self.assertTrue(len(comps)<=20)

        
