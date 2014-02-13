import logging
log=logging.getLogger(__name__)

from defined_media.forms import SourceForm
from defined_media.models import *

from django.views.generic.edit import CreateView
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

class NewSourceView(CreateView):
    model=Sources

    def get_success_url(self, *args, **kwargs):
        try:
            pubmed_id=int(self.request.POST['pubmed_id'])
            source=Sources.objects.get(pubmed_id=pubmed_id)
        except (ValueError, Sources.DoesNotExist) as e:
            keys='first_author journal year title'.split(' ')
            args=dict((k, self.request.POST[k]) for k in keys)
            source=get_object_or_404(Sources, **args)
        return reverse('source_record', args=(source.sourceid,))

    def post(self, request, *args, **kwargs):
        try:
            keys='first_author journal year title'.split(' ')
            args=dict((k,self.request.POST[k]) for k in keys)
            n_sources=Sources.objects.filter(**args).count()
            if n_sources > 0:
                log.debug('barf')
                self.object=None
                raise IntegrityError('This message is not used')

            return super(NewSourceView,self).post(request, *args, **kwargs)
        except IntegrityError:
            self.Error='This source already exists in the database.'
            form=SourceForm(self.request.POST)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context=super(NewSourceView,self).get_context_data(**kwargs)
        try: context['Error']=self.Error
        except AttributeError: pass
        try: context['object']=self.object
        except AttributeError: pass
        return context
