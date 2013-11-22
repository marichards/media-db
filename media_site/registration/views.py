import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from registration.forms import LoginForm, RegistrationForm

log=logging.getLogger(__name__)

def login2(request):
    added_context={
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        }

    # if just a get, return the blank template
    if request.method.lower()=='get':
        return render(request, 'registration/login.html', added_context)

    # if a post, figure out which of the forms was filled out
    if request.method.lower()=='post':
        if request.POST['form_name']=='login':
            return login2_login(request, added_context=added_context)
        else:
            return register_new_user(request)

def login2_login(request, **kwargs):
    form=LoginForm(request.POST)
    if not form.is_valid():
        log.debug('login2_loing: form invalid')
        return render(request, 'registration/login.html', kwargs['added_context'])

    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username, password=password)
    if user is None:
        log.debug('incorrect user/password')
        login_form=kwargs['added_context']['login_form']
        log.debug('login_form.errors: %s' % login_form.errors)
        login_form.errors['msg']='incorrect user/password'
        return render(request, 'registration/login.html', kwargs['added_context'])
        
    log.info('user logged in: %s' % username)
    try: next=request.session['redirect_to']
    except KeyError: next=reverse('user_profile', args=(username,))
    log.debug('redirecting to %s' % next)
    return redirect(next)
        


def user_profile(request, **kwargs):
    user=request.user
    reg_args={'username': user.username, # fixme: need to update this with Contributor fields
              'password1': 'blah',
              'password2': 'blah',
              'email': 'joe@blow.com',
              'lab': 'Price Lab',
              'lab_url': 'http://systemsbiology.org/PriceLab'}
    reg_form=RegistrationForm(reg_args)

    # fixme: user_profile.html doesn't have a Submit button...

#    added_context={'registration_form': RegistrationForm.from_user(user)}
    added_context={'registration_form': reg_form}
    return render(request, 'registration/user_profile.html', added_context)


def register_new_user(request):
    pass

def logout(request):
    logout(request.user)
    return redirect(reverse('login'))

'''
# fixme: implement the following:
def forgotten_password_request_email():
    pass

def forgotten_password_email_sent():
    pass

def forgotten_password_enter_new_password():
    pass

'''
