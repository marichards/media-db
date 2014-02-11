import logging, copy, json
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.models import *
from defined_media.forms.media_names_form import MediaNamesForm
#from defined_media.tests.snapshot import *
from defined_media.tests.models.media_names.mock_post_dict import MockPostDict

class TestMediaNamesForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        self.logged_in=self.client.login(username='vcassen', password='Bsa441_md')

    def tearDown(self):
        pass


    def test_is_valid_bad_comp(self):
        '''
        need to check that all compounds are findable and that amounts exist where needed
        '''
        mn0=MediaNames.objects.first()
        comps=MockPostDict(mn0)
        comps['comp2']='imaginary compound'
        form=MediaNamesForm(comps)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comp2'], 'Unknown compound "imaginary compound"', form.errors['comp2'])
        self.assertEqual(len(form.errors), 1, form.errors)


    def test_is_valid_bad_amount(self):
        mn0=MediaNames.objects.first()
        comps=MockPostDict(mn0)
        comps['comp2']='imaginary compound'
        form=MediaNamesForm(comps)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comp2'], 'Unknown compound "imaginary compound"', form.errors['comp2'])
        self.assertEqual(len(form.errors), 1, form.errors)
