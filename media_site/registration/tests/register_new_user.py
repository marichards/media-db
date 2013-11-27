import logging
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

log=logging.getLogger(__name__)

class TestRegister(TestCase):
    fixtures=['one_user.json']
    def setUp(self):
        self.client=Client()
        pass

    def tearDown(self):
        pass

    def test_new_user(self):
        try:
            wilma=User.objects.get(username='wilma')
            self.fail('user "wilma" already in db')
        except User.DoesNotExist:
            self.assertTrue(True)

        args={'username':'wilma',
              'email':'wilma@wilma.com',
              'password1':'wilma',
              'password2':'wilma',
              'lab':'lab wilma',
              'lab_url': 'http://wilma.com'}
        url=reverse('register_new_user')
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)

        try:
            wilma=User.objects.get(username='wilma')
            self.assertTrue(True)
            log.debug('got user %s' % wilma)
        except User.DoesNotExist:
            self.fail('user "wilma" not found')

        url=reverse('user_profile', args=('wilma',))
        log.debug('now hitting %s' % url)
        response=self.client.get(url)
        self.assertEqual(response.status_code, 200)
        log.debug('response: %s' % response)
        
              
