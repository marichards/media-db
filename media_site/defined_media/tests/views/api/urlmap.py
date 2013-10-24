import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from defined_media.models import Organisms

class TestOrganismAPI(TestCase):
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_urlmap_GET(self):
        url=reverse('urlmap')
        print url
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.content)
        for name,url in data.items():
            print '%s -> %s' % (name, url)
        self.assertEqual(data['organism_api'], reverse('organism_api'))
