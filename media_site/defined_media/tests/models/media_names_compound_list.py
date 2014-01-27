from django.test import TestCase
from defined_media.models import *

class TestMediaNamesCompoundList(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compound_list_equal(self):
        gd0=MediaNames.objects.all()[0]
        self.assertTrue(gd0._compound_list_equal(gd0))

    def test_compound_list_not_equals(self):
        gd0=MediaNames.objects.all()[0]
        gd1=MediaNames.objects.all()[1]
        
        self.assertFalse(gd0._compound_list_equal(gd1))
        self.assertFalse(gd1._compound_list_equal(gd0))

