from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class TestCompoundDetail(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_compound_detail(self):
        response=self.client.get(reverse('compound_record', args=[1])).content # water
        self.assertIn('Compound ID: 1', response)
        self.assertIn('KEGG ID: C00001', response)
        self.assertIn('BiGG ID: h2o', response)
