import logging
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.models import *
from defined_media.tests.snapshot import snapshot, compare_snapshots

log=logging.getLogger(__name__)
SUCCESS=302
FAILURE=200

class TestCreate(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_success_no_uptakes(self):
        ss1=snapshot(self, 'start')

        url=reverse('create_growth_data')
        log.debug('%d Organisms' % Organisms.objects.count())
        args={'strainid': Organisms.objects.first().strainid,
              'sourceid':Sources.objects.first().sourceid,
              'medid':MediaNames.objects.first().medid,
              'ph':7,
              'temperature_c':38.8,
              'growth_rate':1.2,
              }
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, SUCCESS)
        
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {GrowthData: +1})
