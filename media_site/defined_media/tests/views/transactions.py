import logging, copy
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from defined_media.tests.forms.test_cases import newmedia_inputs
from defined_media.models import *

class TestMediaForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_break_media_comps(self):
        # can't break it with a bad compound; that'll be caught by form.is_valid
        # can't break it with missing/bad amount; ditto
        pass                    # ...
