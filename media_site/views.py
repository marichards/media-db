import logging
from django.shortcuts import render
from django.http import HttpResponse
from registration.forms import LoginForm, RegistrationForm

log=logging.getLogger('defined_media')

def login2(request):
    # if just a get, return the blank template
    if request.method.lower()=='get':
        added_context={
            'login_form': LoginForm(),
            'registration_form': RegistrationForm(),
            }
        return render(request, 'registration/login.html', added_context)

    # if a post, figure out which of the forms was filled out
    if request.method.lower()=='post':
        pass

def login2_login(request):
    pass

def login2_register(request):
    pass

def user_profile(request):
    user=request.user
    return HttpResponse('register new user (NYI)')

def register(request):
    pass

def logout(request):
    pass
