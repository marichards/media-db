import logging
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

log=logging.getLogger(__name__)

'''
usage:
> py manage.py test registration.tests.register_new_user
'''

class TestRegister(TestCase):
    fixtures=['one_user.json']
    def setUp(self):
        self.client=Client()
        pass

    def tearDown(self):
        pass

    def test_new_user_success(self):
        try:
            wilma=User.objects.get(username='wilma')
            self.fail('user "wilma" already in db')
        except User.DoesNotExist:
            self.assertTrue(True)

        args={'username':'wilma',
              'first_name': 'wilma',
              'last_name': 'flintstone',
              'email':'wilma@wilma.com',
              'password1':'WilmaFlintstone1',
              'password2':'WilmaFlintstone1',
              'lab':'Price',
              'lab_url': 'http://systemsbiology.org/pricelab'}
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
        
              
    def test_new_user_bad_password(self):
        response=self._test_bad_args(
            {'username':'wilma',
             'first_name': 'wilma',
             'last_name': 'flintstone',
             'email':'wilma@wilma.com',
             'password1':'WilmaFlintstone',
             'password2':'WilmaFlintstone',
             'lab':'Price',
             'lab_url': 'http://systemsbiology.org/pricelab'})

        self.assertIn('Password must be at least 8 characters, contain upper and lower case letters, and at least one digit', response.content)
              
    def test_new_user_mismatched_password(self):
        response=self._test_bad_args(
            {'username':'wilma',
             'first_name': 'wilma',
             'last_name': 'flintstone',
             'email':'wilma@wilma.com',
             'password1':'WilmaFlintstone1',
             'password2':'WilmaFlintstone2',
             'lab':'Price',
             'lab_url': 'http://systemsbiology.org/pricelab'})

        self.assertIn("Passwords don&#39;t match", response.content)

    def _test_bad_args(self, args):
        try:
            wilma=User.objects.get(username='wilma')
            self.fail('user "wilma" already in db')
        except User.DoesNotExist:
            self.assertTrue(True)


        url=reverse('register_new_user')
        response1=self.client.post(url, args)
        
        # make sure we didn't get a redirect:
        self.assertEqual(response1.status_code, 200)

        # make sure user is not in database:
        username=args['username']
        try:
            wilma=User.objects.get(username=args['username'])
            self.fail('user "%s" found' % username)
        except User.DoesNotExist:
            self.assertTrue(True)
            log.debug('did not get user %s' % username)

        # 
        url=reverse('user_profile', args=(username,))
        log.debug('now hitting %s' % url)
        response=self.client.get(url)
        self.assertEqual(response.status_code, 302)
        log.debug('response: %s' % response.content)
        self.assertIn('Location: http://testserver/login/?next=/profile/%s' % username, str(response), str(response))
        
        return response1

