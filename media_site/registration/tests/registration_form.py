import logging
from django.test import TestCase
from registration.forms import RegistrationForm
from django.contrib.auth.models import User

log=logging.getLogger(__name__)

class TestRegistrationForm(TestCase):
    fixtures=['one_user.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_from_dict(self):
        try:
            form=RegistrationForm({'username':'fred',
                                  'password1':'fred1',
                                  'password2':'fred2',
                                  'email':'fred@fred.com',
                                  'lab':'LabFred',
                                  'lab_url':'lab_fred@fred.com'})
            self.assertTrue(True)
        except Exception as e:
            self.fail('caught %s: %s' % (type(e).__name__, e))
            
        for d in [d for d in dir(form) if not callable(getattr(form, d))]:
            print 'non-callable form.%s' % d

    def test_from_user(self):
        user=self.get_mock_user()
        form=RegistrationForm.from_user(user)
        try:
            self.assertTrue(True)
        except Exception as e:
            self.fail('caught %s: %s' % (type(e).__name__, e))
            

    def get_mock_user(self):
        existing_user=User.objects.all()[0]
        existing_user.lab='FAKE price lab'
        existing_user.lab_url='http://fake.price.lab'
        return existing_user

    def test_username_in_use(self):
        existing_user=self.get_mock_user()
        form=RegistrationForm.from_user(existing_user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], 'username "%s" already taken' % existing_user.username)
        print 'form.errors: %s' % form.errors
        print 'form.my_errors: %s' % form.reformat_errors().my_errors
        print 'form.cleaned_data: %s' % form.cleaned_data

    def test_passwords_mismatch(self): # note: this is different from wrong password
        pass
