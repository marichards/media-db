from django import template
register=template.Library()

from defined_media.forms import SearchForm
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf

class SearchFormTag(template.Node):
    def render(self, context):
        context.update({'search_form': SearchForm()})
        return get_template('defined_media/search.html').render(context)

def do_search_form(parser, token):
    return SearchFormTag()


register.tag('search_form', do_search_form)

'''
{% search_form %}

Inserts the search form.  Pretty simple.

'''
