import logging
log=logging.getLogger(__name__)

from defined_media.forms import MediaNamesForm
from defined_media.models import *

from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

class NewMediaView(FormView):
    template_name='defined_media/medianames_form.html'
    form_class=MediaNamesForm

#    def get_success_url(self, *args, **kwargs):
#        pass

    def get(self, request, *args, **kwargs):
        try:
            mn=GrowthData.objects.get(growthid=kwargs['pk'])
            user=request.user
            if not user.contributor.can_edit_mn(mn):
                return redirect('forbidden')

            self.mn=mn
            form=MediaNamesForm.from_media_name(mn)

        except (GrowthData.DoesNotExist, KeyError):
            form=MediaNamesForm(initial={'contributor_id': request.user.contributor.id})
            
        return self.form_invalid(form) 
        

    def post(self, request, *args, **kwargs):
        return super(NewMediaView,self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super(NewMediaView,self).get_context_data(**kwargs)
        try: context['mn']=self.mn
        except AttributeError: pass
        return context

            
