import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse, NoReverseMatch


class TestPmidAPI(TestCase):
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_efetch_pmid_GET(self):
        pmid=10383747
        url=reverse('efetch_pmid', args=(pmid,))
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.content)
        
        self.assertEqual(int(data['pmid']), pmid)
        self.assertEqual(data['authors'], ['Hager B', 'Bickenbach JR', 'Fleckman P'])
        self.assertEqual(data['title'], 'Long-term culture of murine epidermal keratinocytes.')
        self.assertEqual(data['journal'], 'The Journal of investigative dermatology')
        self.assertEqual(data['date'], '1999 Jun')
        self.assertEqual(data['link'], 'http://www.ncbi.nlm.nih.gov/pubmed/?term=10383747')

    def test_bad_pmid(self):
        self.assertRaises(NoReverseMatch, reverse, 'efetch_pmid', args=())
        self.assertRaises(NoReverseMatch, reverse, 'efetch_pmid', args=('fred',))

    def test_pmid_not_found(self):
        pmid=100000000
        url=reverse('efetch_pmid', args=(pmid,))
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.content)
        self.assertEqual(data['error'], 'nothing found for pmid=%d' % pmid)
