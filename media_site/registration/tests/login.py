from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import logging
log=logging.getLogger(__name__)

class TestLogin(TestCase):
    fixtures=['one_user.json']

    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def fetch(self, view_name, args, expected_status):
        url=reverse(view_name)
        if args:
            response=self.client.post(url, args)
        else:
            response=self.client.get(url)
        self.assertEqual(response.status_code, expected_status, 
                         '%s: expected %s, got %s' % (url, expected_status, response.status_code))
        return response

    def test_login_get(self):
        self.fetch('login', None, 200)

    def test_valid_login(self):
        response=self.fetch('login', {'username':'vcassen', 'password':'Bsa441'}, 302)
        self.assertIn('Location: http://testserver/accounts/profile/vcassen', str(response))

    def test_missing_username(self):
        response=self.fetch('login', {'password':'Bsa441'}, 200)
        self.assertIn('This field is required', response.content, 'This field is required')

    def test_bad_username(self):
        response=self.fetch('login', {'username':'sir not appearing in this picture', 'password':'Bsa441'}, 200)
        self.assertIn('This field is required', response.content, 'This field is required')


    def test_missing_password(self):
        response=self.fetch('login', {'username':'vcassen', }, 200)
        self.assertIn('This field is required', response.content, 'This field is required')


    def test_bad_password(self):
        response=self.fetch('login', {'username':'vcassen', 'password': 'wrong'}, 200)
        self.assertIn('This field is required', response.content, 'This field is required')


