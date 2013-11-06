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
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()

        url=reverse('new_media_form')
        args=newmedia_inputs['minimal_valid']['args']
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(GrowthData.objects.count(), n_gd+1)
        self.assertEqual(Sources.objects.count(), n_src+1)
        self.assertEqual(MediaNames.objects.count(), n_mn+1)
        
    def test_media_form_post_three_compounds_two_uptakes(self):
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        url=reverse('new_media_form')

        args=newmedia_inputs['full_valid']['args']
        args['comp2']='atp'
        args['amount2']='0.48'
        args['comp3']='1,3-Di-(octadec-9Z-enoyl)-1-cyano-2-methylene-propane-1,3-diol'
        args['amount3']='0.148'
        args['comp4']='1,2-Dichloroethane'
        args['amount4']='0.348'
        
        args['uptake_comp1']='Angiotensin (1-5)SEQUENCE Asp Arg Val Tyr IleORGANISM Human [HSA:183]'
        args['uptake_rate1']='-0.2'
        args['uptake_comp2']='Angoline'
        args['uptake_rate2']='0.2'
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)

        log.debug('after: %d growth data objects' % GrowthData.objects.count())
        log.debug('after: %d sources objects' % Sources.objects.count())
        log.debug('after: %d media names objects' % MediaNames.objects.count())
        self.assertEqual(GrowthData.objects.count(), n_gd+1)
        self.assertEqual(Sources.objects.count(), n_src+1)
        self.assertEqual(MediaNames.objects.count(), n_mn+1)
        
