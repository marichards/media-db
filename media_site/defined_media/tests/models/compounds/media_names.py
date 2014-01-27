from django.test import TestCase
from defined_media.models import Compounds

class MediaNamesTestCase(TestCase):
    def setUp(self):
        pass

    def test_media_names(self):
        comp144=Compounds(compid=144)
        print comp144
