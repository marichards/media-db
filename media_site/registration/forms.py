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
    first_name=forms.CharField(label='First Name', max_length=64)
    last_name=forms.CharField(label='Last Name', max_length=64)
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
        lab=user.contributor.lab.name
        lab_url=user.contributor.lab.url
            
        return RegistrationForm({'username': user.username,
                                 'password1': user.password,
                                 'password2': user.password,
                                 'email': user.email,
                                 'lab': lab,
                                 'lab_url': lab_url})

    def is_valid(self, user=None):
        valid=super(RegistrationForm, self).is_valid()

        # I don't think this should be here; will fail for update_user_profile,
        # when this user *should* exist

        # check passwords match, safe
        try:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                self.errors['password2']="Passwords don't match"
                valid=False
            msg=self.password_unsafe(self.cleaned_data['password1'])
            if msg:
                self.errors['password1']=msg
                valid=False
            msg=self.password_unsafe(self.cleaned_data['password2'])
            if msg:
                self.errors['password2']=msg
                valid=False
        except KeyError:
            valid=False

        if user:
            if user.username != self.cleaned_data['username']:
                self.errors['username']='You cannot change your username'
                valid=False


        return valid

    def password_unsafe(self, password):
        '''
        passwords must: 
        - be between 8 and 64 chars
        - contain at least 1 digit
        - at least one upper, lower case char
        '''

        err_msg='Password must be at least 8 characters, contain upper and lower case letters, and at least one digit'
        if not re.search(r'\d', password):
            return err_msg
        if not re.search(r'[a-z]', password):
            return err_msg
        if not re.search(r'[A-Z]', password):
            return err_msg
        if len(password) < 8:
            return err_msg
        if len(password) > 64:
            return err_msg
        return False
