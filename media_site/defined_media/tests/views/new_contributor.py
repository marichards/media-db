from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test import TestCase

class TestNewContributor(TestCase):
    def setUp(self):
        self.client=Client()
        
    def test_new_contributor_form(self):
        reg_url=reverse('register')
        print 'reg_url is %s' % reg_url
