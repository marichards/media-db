import logging
from django.test import TestCase

from defined_media.models import *
from defined_media.tests.snapshot import snapshot, compare_snapshots
#from .mock_post_dict import MockPostDict

log=logging.getLogger(__name__)

class TestMediaNames(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clone(self):
        ss1=snapshot(self, 'start')
        mn=MediaNames.objects.first()
        c=mn.clone()
        self.assertEqual(mn.mediacompounds_set.count(), c.mediacompounds_set.count())
        self.assertNotEqual(mn.medid, c.medid)
        self.assertEqual(mn.media_name+' (clone)', c.media_name)
        # could also test media compounds one by one...

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {MediaNames: +1, MediaCompounds: +c.mediacompounds_set.count()})
