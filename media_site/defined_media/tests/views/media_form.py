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
        response=self.client.get(reverse('new_media_form')).content 
#        print response
        self.assertIn('id_random_tf', response, 'fart')

