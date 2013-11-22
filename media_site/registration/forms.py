import re, logging
from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(label='Username', max_length=64)
    password=forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username=forms.CharField(label='Username', max_length=64)
    email=forms.EmailField(label='Email')
    password1=forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)
    password2=forms.CharField(label='Password (confirm)', max_length=64, widget=forms.PasswordInput)
    lab=forms.CharField(label='Lab', max_length=255)
    lab_url=forms.URLField(label='Lab Url', max_length=255)

    @classmethod
    def from_user(self, user):
        return self(username=user.username,
                    password1=user.password,
                    password2=user.password,
                    email=user.email,
                    lab=user.lab,
                    lab_url=user.lab_url)
