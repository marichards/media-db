import json, logging
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse, NoReverseMatch

log=logging.getLogger(__name__)

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
        log.debug(response.content)

        self.assertEqual(int(data['pmid']), pmid)
        self.assertEqual(data['author'], 'Hager B')
        self.assertEqual(data['title'], 'Long-term culture of murine epidermal keratinocytes.')
        self.assertEqual(data['journal'], 'The Journal of investigative dermatology')
        self.assertEqual(data['year'], '1999')
        self.assertEqual(data['link'], 'http://www.ncbi.nlm.nih.gov/pubmed/?term=10383747')

    def test_bad_pmid(self):
        self.assertRaises(NoReverseMatch, reverse, 'efetch_pmid', args=('fred',))

    def test_missing_pmid(self):
        url=reverse('efetch_pmid', args=())
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 404)


    def test_pmid_not_found(self):
        pmid=100000000
        url=reverse('efetch_pmid', args=(pmid,))
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 404)
        expected_error='<h1>Not Found</h1><p>The requested URL /defined_media/api/pmid/100000000 was not found on this server.</p>'
        self.assertIn(expected_error, response.content)
        
