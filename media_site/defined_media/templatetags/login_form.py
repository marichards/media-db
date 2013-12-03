from django import template
register=template.Library()

from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template

class LoginFormTag(template.Node):
    def render(self, context):
        context.update({'login_tag_form': AuthenticationForm()})
        return get_template('defined_media/login_tag.html').render(context)

def do_login_form(parser, token):
    return LoginFormTag()


register.tag('login_form', do_login_form)

'''
{% load login_form %}
{% login_form %}

Inserts the login form.  Pretty simple.

'''
