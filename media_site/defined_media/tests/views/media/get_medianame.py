import logging
from django.test import TestCase
from defined_media.models import *
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.views.media import NewMediaView
from defined_media.forms.media_names_form import MediaNamesForm

log=logging.getLogger(__name__)

class TestGetMedianame(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        pass
    def tearDown(self):
        pass

    def test_get_medianame(self):
        view=NewMediaView()
        args={'media_name': 'Some media name',
              'is_defined': True,
              'is_minimal': True, 
              'comp1': 'water',
              'amount1': '3.32',
              'comp2': 'NADH',
              'amount2': '4.23',
              }

        form=MediaNamesForm(args)
        self.assertTrue(form.is_valid()) # to get cleaned_data, also; but doesn't work if form init'd from mn0
        mn=view.get_medianames(form)
        self.assertEqual(mn.media_name, args['media_name'])
        self.assertEqual(mn.is_defined, 'Y')
        self.assertEqual(mn.is_minimal, 'Y')
        self.assertEqual(mn.mediacompounds_set.count(), 2)
