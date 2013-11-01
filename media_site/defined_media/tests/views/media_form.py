import logging
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from defined_media.tests.forms.test_cases import newmedia_inputs
from defined_media.models import *

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
        self.assertIn("<table id='id_medianames_table'>", content, "'id='id_medianames_table' not found'")


    def test_media_form_is_valid(self):
        url=reverse('new_media_form')
        for name, data in newmedia_inputs.items():
            log.debug('name is %s' % name)
            args=data['args']
            expected_valid=data['valid']
            response=self.client.post(url, args)
            expected_code=302 if expected_valid else 200
            log.debug('code (%s, ev=%s): expected %s, got %s' % (name,
                                                                 expected_valid, 
                                                                 expected_code, 
                                                                 response.status_code))
            self.assertEqual(response.status_code, expected_code)


    def test_media_form_post(self):
        n_gd=GrowthData.objects.count()
        log.debug('to start: %d growth data objects' % n_gd)

        url=reverse('new_media_form')
        args=newmedia_inputs['minimal_valid']['args']
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(GrowthData.objects.count(), n_gd+1)
        
