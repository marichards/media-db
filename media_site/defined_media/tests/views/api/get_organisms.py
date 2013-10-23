from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class TestSomething(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        pass

    def tearDown(self):
        pass

    def test_organisms_list_GET(self):
        url=reverse('organisms_api')
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.content)
        self.assertTrue(len(data), 4)
        
        for org in data:
            print org


        
