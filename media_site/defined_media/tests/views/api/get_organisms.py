import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class TestOrganismAPI(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        pass

    def tearDown(self):
        pass

    def test_organisms_list_GET(self):
        url=reverse('organism_api')
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.content)
        print 'got %d organisms' % len(data)
        self.assertEqual(len(data), 25)



        
