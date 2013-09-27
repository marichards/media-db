from django.test import TestCase
from defined_media.models import *

class CompoundsTest(TestCase):
    def setUp(self):
        print 'setUp'

    def test_media_names(self):
        comps=Compounds.objects.all()
        print 'got %d comps' % len(comps)
        comp144=comps[143]
        print 'comp144: %s' % comp144

        self.fail()
