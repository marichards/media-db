from django import template
register=template.Library()

from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf

class LoginFormTag(template.Node):
    def render(self, context):
        context.update({'form': AuthenticationForm()})
        return get_template('defined_media/login_tag.html').render(context)

def do_login_form(parser, token):
    return LoginFormTag()


register.tag('login_form', do_login_form)

'''
{% search_form %}

Inserts the search form.  Pretty simple.

'''
