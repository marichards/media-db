import logging
from django.test import TestCase
from defined_media.models import *
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.views.media import NewMediaView
from defined_media.forms import MediaNamesForm
from defined_media.tests.snapshot import snapshot, compare_snapshots

log=logging.getLogger(__name__)

SUCCESS=302
FAILURE=200

class TestPost(TestCase):
    fixtures=['fixture.json']

    def setUp(self):
        self.client=Client()
        if not self.client.login(username='vcassen', password='Bsa441_md'):
            raise RuntimeError("Can't login")

    def tearDown(self):
        pass

    def test_create(self):
        args={'media_name': 'Some media name',
              'is_defined': True,
              'is_minimal': True, 
              'comp1': 'water',
              'amount1': '3.32',
              'comp2': 'NADH',
              'amount2': '4.23',
              }
        ss1=snapshot(self, 'start')
        url=reverse('new_media')
        response=self.client.post(url, args)
        self.assertTrue(response.status_code, SUCCESS)
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {MediaNames: +1, MediaCompounds: +2})

    def test_missing_amount_create(self):
        '''
        A compound named, but with a missing amount, should cause an error.
        '''
        args={'media_name': 'Some media name',
              'is_defined': True,
              'is_minimal': True, 
              'comp1': 'water',
              'amount1': '3.32',
              'comp2': 'NADH',
              }
        ss1=snapshot(self, 'start')
        url=reverse('new_media')
        response=self.client.post(url, args)
        self.assertTrue(response.status_code, FAILURE)
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {MediaNames: +0, MediaCompounds: +0})

    def test_missing_amount_edit(self):
        '''
        A compound named, but with a missing amount, should cause an error.
        '''
        args={'media_name': 'Some media name',
              'is_defined': True,
              'is_minimal': True, 
              'comp1': 'water',
              'amount1': '3.32',
              'comp2': 'NADH',
              }
        ss1=snapshot(self, 'start')

        mn=MediaNames.objects.first()
        url=reverse('new_media', args=(mn.medid,))
        response=self.client.post(url, args)
        self.assertTrue(response.status_code, FAILURE)
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {MediaNames: +0, MediaCompounds: +0})

