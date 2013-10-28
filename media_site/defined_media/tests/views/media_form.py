from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class TestMediaForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_media_form_get_empty(self):
        response=self.client.get(reverse('new_media_form'))
#        print content
        self.assertEqual(response.status_code, 200)
        content=response.content
        self.assertIn('<h2>Enter Media Information:</h2>', content)
        self.assertIn("<input type='hidden' name='csrfmiddlewaretoken'", content)
        self.assertIn("<table id='newmedia_table'>", content)

    def test_media_form_post(self):
        url=reverse('new_media_form')
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'pmid': '10238329',
              'comp1': 'h2o', 'amount': '1.23', 
              }
        response=self.client.post(url, args)
        print 'post: status: %s' % response.status_code
