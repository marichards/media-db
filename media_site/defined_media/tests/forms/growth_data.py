import logging
from django.test import TestCase
from defined_media.models import *
from defined_media.forms import NewCompoundMediaForm

log=logging.getLogger(__name__)

class TestForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_form(self):
        for gd in GrowthData.objects.all():
            try:
                form=NewCompoundMediaForm.from_growth_data(gd)
            except:
                self.fail()

            # check for growthid...
            

