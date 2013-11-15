import logging
from django.test import TestCase
from defined_media.models import *

log=logging.getLogger(__name__)

class TestGetObj(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_obj(self):
        gd265=get_obj('GrowthData', 265)
        log.debug('gd265: %s' % gd265)
        self.assertEqual(gd265.growthid, 265, str(gd265.growthid))
