import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib.auth import authenticate
import django.contrib.auth as auth
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

def login(request, *args, **kwargs):
    # we'll need these forms (in one form or another)
    added_context={
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        }
    
    # get request?
    if request.method.lower()=='get':
        return render(request, 'registration/login.html', added_context)
        
    # login attempt:
    log.debug('request.POST: %s' % request.POST)
    login_form=LoginForm(request.POST)
    added_context['login_form']=login_form
    if not login_form.is_valid():
        log.debug('login: form invalid')
        added_context['login_form']=LoginForm(request.POST).reformat_errors()
        return render(request, 'registration/login.html', added_context)

    username=request.POST['username']
    password=request.POST['password']
    log.debug('attempting login attempt: username=%s' % username)
    user=auth.authenticate(username=username, password=password)
    log.debug('user is %s' % user)
    if user is None:
        log.debug('incorrect user/password')
        login_form.errors.msgs.append('incorrect user/password')
        return render(request, 'registration/login.html', added_context)
    else:
        auth.login(request, user)
        log.info('user logged in: %s' % username)

    try: next=request.POST['next']
    except KeyError: next=reverse('user_profile', args=(username,))
    log.debug('redirecting to %s' % next)
    return redirect(next)
        


def user_profile(request, **kwargs):
    if request.method.lower()=='get':
        return user_profile_get(request, **kwargs)
    else:
        return user_profile_post(request, **kwargs)

def user_profile_get(request, **kwargs):
    user=request.user
    
    # get a form based on the user
    # make sure they didn't change their name (need to disallow this in profile
    # make sure other fields valid
    # update user object based on form values, save
    # if all good, re-display the profile page with a 'profile updated' message

    
def user_profile_get(request, **kwargs):
    user=request.user
    log.debug('user_profile(user=%s) entered' % user)
    reg_args={'username': user.username, # fixme: need to update this with Contributor fields
              'password1': '',
              'password2': '',
              'email': user.email,
              'lab': 'FAKE Price Lab',
              'lab_url': 'http://systemsbiology.org/PriceLab'}
    reg_form=RegistrationForm(reg_args)
    added_context={'registration_form': reg_form}
    return render(request, 'registration/user_profile.html', added_context)


def register_new_user(request):
    log.debug('register_new_user entered')
    form=RegistrationForm(request.POST)
    if not form.is_valid():       # try again
        log.debug('invalid form, try again')
        return render(request, 'registration/login.html')


    try:
        username=form.cleaned_data['username']
        user=User.objects.get(username=username)
        log.debug('found existing user %s' % username)
        form.errors['username']='username "%s" already taken' % username
        form.reformat_errors()
        return render(request, 'registration/login.html')
    except User.DoesNotExist:
        log.debug('no user %s, proceeding' % username)
        pass

    log.debug('attempting to create new user %s' % form.cleaned_data['username'])
    username=form.cleaned_data['username']
    password1=form.cleaned_data['password2']
    password2=form.cleaned_data['password1']
    email=form.cleaned_data['email']
    lab=form.cleaned_data['lab']
    lab_url=form.cleaned_data['lab_url']
    user=User.objects.create_user(username, email, password1)
    log.debug('created user %s' % user)
    user=auth.authenticate(username=username, password=password1)
    log.debug('authenticated user %s' % user)
    auth.login(request, user)
    log.debug('login user %s' % user)
    
    url=reverse('user_profile', args=(form.cleaned_data['username'],))
    log.debug('register redirecting to %s' % url)
    return redirect(url)

def logout(request):
    try: username=request.user.name
    except AttributeError: username='nobody'

    try:
        log.debug('attempting to logout user %s' % username)
        auth.logout(request)
        log.debug('user %s logged out' % username)
    except Exception as e: 
        log.debug('error logging out user %s: %s %s' % (username, type(e), e))
        pass

    try: to_here=request.POST['next']
    except (KeyError, AttributeError): to_here=reverse('login')
    log.debug('logout: redirecting to %s' % to_here)
    return redirect(to_here)

'''
# fixme: implement the following:
def forgotten_password_request_email():
    pass

def forgotten_password_email_sent():
    pass

def forgotten_password_enter_new_password():
    pass

'''
