import json, logging
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from defined_media.models import *

log=logging.getLogger(__name__)

class TestGrowthDataAPI(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_growthdata_list_GET(self):
        gds_db=GrowthData.objects.all()
        for gd_db in gds_db:
            url=reverse('growth_data_api', args=(gd_db.growthid,))
            response=self.client.get(url, ACCEPT='application/json')
            self.assertEqual(response.status_code,200, str(response.status_code))
            data=json.loads(response.content)
            log.debug('got back data: %s' % response.content)
            break



        
