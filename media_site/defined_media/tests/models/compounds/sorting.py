from django.test import TestCase
from defined_media.models import Compounds

class MediaNamesTestCase(TestCase):
    fixtures=['fixture.json']

    def test_sorting(self):
        compounds=Compounds.objects.all()[:50]
        print '%d compounds' % len(compounds)
        for c in sorted(list(compounds), key=lambda c: c.keywords()[0]):
            print str(c)
