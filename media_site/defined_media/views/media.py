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
        form=MediaNamesForm(request.POST)
        if not form.is_valid():
            # maybe do something about reformatting errors....
            return self.form_invalid()

        # probably something about getting/creating the MediaNames,
        # setting up its mediacompounds_set, and possibly saving
        mn=self.get_medianames(form)

        # error handling: have to make sure compounds exist and amounts
        # are kosher; do that in form.is_valid?

        # also have to save state between calls if there's an error
        # so Matt doesn't have to re-enter everything on any little mistake.

        # might also have to do the transaction thing
        
#        return super(NewMediaView,self).post(request, *args, **kwargs)
        # what is the mixin that checks the form for validity, does the create/edit,
        # and returns either form_invalid() or redirect()?
        if success:
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_medianames(self, form):
        ''' get or create a MediaNames object based on the form values '''
        if form.

    def get_context_data(self, **kwargs):
        context=super(NewMediaView,self).get_context_data(**kwargs)
        try: context['mn']=self.mn
        except AttributeError: pass
        return context

            
