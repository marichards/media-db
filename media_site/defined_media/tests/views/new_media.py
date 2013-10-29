from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test import TestCase

class TestNewMedia(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        
    def test_new_contributor_form(self):
        reg_url=reverse('newmedia')
        print 'reg_url is %s' % reg_url
