import logging
log=logging.getLogger(__name__)

from defined_media.forms import OrganismForm
from defined_media.models import *

from django.views.generic.edit import CreateView
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

class NewOrganismView(CreateView):
    model=Organisms

    def get_success_url(self, *args, **kwargs):
        org=get_object_or_404(Organisms,
                              genus=self.request.POST['genus'],
                              species=self.request.POST['species'],
                              strain=self.request.POST['strain'])
        return reverse('organism_record', args=(org.strainid,))

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('forbidden')
        return super(NewOrganismView,self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('forbidden')

        try:
            return super(NewOrganismView,self).post(request, *args, **kwargs)
        except IntegrityError:
            self.Error='An organism of this genus/species/strain/ already exists!'
            form=OrganismForm(self.request.POST)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context=super(NewOrganismView,self).get_context_data(**kwargs)
        try: context['Error']=self.Error
        except AttributeError: pass
        return context
