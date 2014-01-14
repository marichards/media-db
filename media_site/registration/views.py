import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib.auth import authenticate
import django.contrib.auth as auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from defined_media.models import Contributor, Lab
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
    next=get_next(request)
    added_context={
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        'next': next,
        }
    
    # get request?
    if request.method.lower()=='get':
        return render(request, 'registration/login.html', added_context)
        
    # login attempt:
    login_form=LoginForm(request.POST)
    added_context['login_form']=login_form
    if not login_form.is_valid():
        added_context['login_form']=LoginForm(request.POST).reformat_errors()
        return render(request, 'registration/login.html', added_context)

    username=request.POST['username']
    password=request.POST['password']
    user=auth.authenticate(username=username, password=password)
    if user is None:
        log.info('incorrect user/password for user %s' % username)
        login_form.errors.msgs.append('incorrect user/password')
        return render(request, 'registration/login.html', added_context)
    else:
        auth.login(request, user)
        log.info('user logged in: %s' % username)

    if not next or next==reverse('logout') or next==reverse('login'):
        next=reverse('user_profile', args=(username,))
    return redirect(next)
        

def get_next(request):
    try:
        return request.GET['next']
    except KeyError:
        try:
            return request.POST['next']
        except KeyError:
            return None

            
    


# login_required (as per urls.py)
def user_profile(request, **kwargs):
    if request.method.lower()=='get':
        return user_profile_get(request, **kwargs)
    else:
        return user_profile_post(request, **kwargs)


# login_required (as per urls.py)
def user_profile_get(request, **kwargs):
    reg_form=RegistrationForm.from_user(request.user)
    added_context={'registration_form': reg_form}
    return render(request, 'registration/user_profile.html', added_context)


# login_required (as per urls.py)
def user_profile_post(request, **kwargs):
    log.debug('hi!')
    user=request.user
    form=RegistrationForm(request.POST)
    added_context={'registration_form': form}
    if not form.is_valid(user=user):
        form.reformat_errors()
        log.debug('user %r not valid, aborting' % user.contributor)
        return render(request, 'registration/user_profile.html', added_context)
    
    user.first_name=form.cleaned_data['first_name']
    user.last_name=form.cleaned_data['last_name']
    user.email=form.cleaned_data['email']
    user.password=form.cleaned_data['password1']
    user.contributor.lab.name=form.cleaned_data['lab']
    user.contributor.lab.url=form.cleaned_data['lab_url']
    try:
        log.debug('about to save user: %r' % user.contributor)
        user.save()
        added_context['msgs']='Profile successfully updated'
    except Exception as e:
        msgs='Unable to save user information: %s' % e
        added_context['msgs']=msgs
        log.debug(msgs)

    
    return render(request, 'registration/user_profile.html', added_context)



def register_new_user(request):
    form=RegistrationForm(request.POST)
    log.debug('hi, prospective new user')
    if not form.is_valid():       # try again
        log.debug('form invalid, try again')
        form.reformat_errors()
        return render(request, 'registration/login.html', {'registration_form': form, 'fart2': 'fjdskl'})

    # check for previously existing user of that name:
    try:
        username=form.cleaned_data['username']
        user=User.objects.get(username=username)
        form.errors['username']='username "%s" already taken' % username
        log.debug('username %s already taken' % username)
        form.reformat_errors()
        return render(request, 'registration/login.html', {'registration_form': form, 'fart2': 'fjdskl'})
    except User.DoesNotExist:
#        log.debug('no user %s, proceeding' % username)
        pass

    # create User:
    log.info('attempting to create new user %s' % form.cleaned_data['username'])
    username=form.cleaned_data['username']
    first_name=form.cleaned_data['first_name']
    last_name=form.cleaned_data['last_name']
    password1=form.cleaned_data['password2']
    password2=form.cleaned_data['password1']
    email=form.cleaned_data['email']
    lab_name=form.cleaned_data['lab']
    lab_url=form.cleaned_data['lab_url']

    user=User.objects.create_user(username, email, password1)
    user=auth.authenticate(username=username, password=password1)
    auth.login(request, user)
    log.info('new user %s logged in' % user.username)

    # create lab and contributor:
    try:
        lab=Lab.objects.get(name=lab_name)
    except Lab.DoesNotExist:
        lab=Lab(name=lab_name, url=lab_url)
        lab.save()
    log.debug('new user: lab is %s' % lab)

    try:
        contributor=Contributor.objects.get(user=user)
    except Contributor.DoesNotExist:
        contributor=Contributor(user=user, first_name=first_name, last_name=last_name, lab=lab)
        contributor.save()
    log.debug('contributor is %s' % contributor)

    url=reverse('user_profile', args=(user.username,))
    return redirect(url)

def logout(request):
    try: username=request.user.username
    except AttributeError: username='nobody'

    try:
        auth.logout(request)
#        log.debug('user %s logged out' % username)
    except Exception as e: 
#        log.debug('error logging out user %s: %s %s' % (username, type(e), e))
        pass

    to_here=reverse('login')
    return render(request, 'registration/login.html', {'msgs': '%s logged out' % username})


def forbidden(request):
    return render(request, 'registration/forbidden.html', {})

'''
# fixme: implement the following:
def forgotten_password_request_email():
    pass

def forgotten_password_email_sent():
    pass

def forgotten_password_enter_new_password():
    pass

'''
