import logging
from django.test import TestCase
from defined_media.models import *
#from django.test.client import Client
#from django.core.urlresolvers import reverse

log=logging.getLogger(__name__)

class TestSomething(TestCase):
    # fixtures=['fixture.json']
    def setUp(self):
#        self.client=Client()
        pass
    def tearDown(self):
        pass

    def test_something(self):
        pass
