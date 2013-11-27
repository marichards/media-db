import re, logging
from django import forms
from form_helpers import ReformatsErrors
from django.contrib.auth.models import User
log=logging.getLogger(__name__)

class LoginForm(forms.Form, ReformatsErrors):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.errors.msgs=[]

    username=forms.CharField(label='Username', max_length=64)
    password=forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)

class RegistrationForm(forms.Form, ReformatsErrors):
    username=forms.CharField(label='Username', max_length=64)
    email=forms.EmailField(label='Email')
    password1=forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)
    password2=forms.CharField(label='Password (confirm)', max_length=64, widget=forms.PasswordInput)
    lab=forms.CharField(label='Lab', max_length=255)
    lab_url=forms.URLField(label='Lab Url', max_length=255)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.msgs=[]

    def __repr__(self):
        return repr(self.cleaned_data)

    @classmethod
    def from_user(self, user):
        try: lab=user.lab
        except AttributeError: lab='FAKE user.lab'
        try: lab_url=user.lab_url
        except AttributeError: lab_url='http://FAKE.user.lab'
            
        return RegistrationForm({'username': user.username,
                                 'password1': user.password,
                                 'password2': user.password,
                                 'email': user.email,
                                 'lab': lab,
                                 'lab_url': lab_url})

    def is_valid(self):
        valid=super(RegistrationForm, self).is_valid()
        log.debug('form is %r' % self)
        log.debug('valid is %s' % valid)
        if not valid:
            log.debug('initial errors: %s' % self.errors)
        
        # I don't think this should be here; will fail for update_user_profile,
        # when this user *should* exist

        try:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                log.debug('password mismatch')
                self.errors['password2']="Passwords don't match"
                valid=False
        except KeyError:
            valid=False

        log.debug('RegistrationForm.is_valid returning %s' % valid)
        return valid
