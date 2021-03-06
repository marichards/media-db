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

    def test_compound_list(self):
        url=reverse('compounds')
        print url
        response=self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print response.content
