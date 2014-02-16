import logging, time
from django.test import TestCase
from defined_media.models import *
from defined_media.tests import snapshot, compare_snapshots

log=logging.getLogger(__name__)

class TestDBTS(TestCase):
    # fixtures=['fixture.json']
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_save(self):
        snap1=snapshot(self, 'start')
        ss1=DatabaseSnapshot()
        ss1.save()
        snap2=snapshot(self, 'after 1')
        compare_snapshots(self, 'start', 'after 1', {DatabaseSnapshot: +1})

        ss2=DatabaseSnapshot()
        ss2.save()
        snap2=snapshot(self, 'after 2')
        compare_snapshots(self, 'start', 'after 2', {DatabaseSnapshot: +2})

    def test_ordering(self):
        ss1=DatabaseSnapshot()
        time.sleep(1)
        ss2=DatabaseSnapshot()
        self.assertTrue(ss2>ss1)
        self.assertTrue(ss2>=ss1)
        self.assertFalse(ss1>ss2)
        self.assertFalse(ss1>=ss2)
        self.assertTrue(ss1==ss2)
        self.assertFalse(ss1!=ss2)
        print 'weird'

    def test_str(self):
        ss1=DatabaseSnapshot()
        ss1.save()
        log.debug(str(ss1))
        print str(ss1)

    def test_static(self):
        ss1=DatabaseSnapshot()
        ss1.save()
        print ss1.get_absolute_url()
