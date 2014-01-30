from django.test import TestCase
from defined_media.models import *

#from django.test.client import Client
#from django.core.urlresolvers import reverse

class TestKeywords(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
#        self.client=Client()
        pass
    def tearDown(self):
        pass

    def test_keywords(self):
        c58s=Compounds.objects.exclude(formula__isnull=True)
        self.assertTrue(c58s.count()>=58, '%d objects with formula != null' % c58s.count())
        
        water=Compounds.objects.get(formula='H2O')
        self.assertEqual(water.name, 'H2O')

        ATP=Compounds.objects.get(formula='C10H16N5O13P3')
        self.assertEqual(ATP.formula, 'C10H16N5O13P3')
        self.assertEqual(ATP.name, 'ATP')
        expected_keywords="ATP,Adenosine 5'-triphosphate,C10H16N5O13P3,C00002".split(',')
        print ATP.keywords()
        self.assertEqual(ATP.keywords(), expected_keywords, ','.join(ATP.keywords()))

