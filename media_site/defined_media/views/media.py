import logging
log=logging.getLogger(__name__)

from defined_media.forms.media_names_form import MediaNamesForm
from defined_media.models import *

from django.views.generic.edit import FormView
from django.db import IntegrityError, transaction
from django.db.transaction import TransactionManagementError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404

class NewMediaView(FormView):
    template_name='defined_media/medianames_form.html'
    form_class=MediaNamesForm

    def get(self, request, *args, **kwargs):
        ''' serve up an empty edit page, or one initialized with a MediaNames object, for editing '''
        try:
            mn=MediaNames.objects.get(medid=kwargs['pk'])
            user=request.user
            if not user.contributor.can_edit_mn(mn):
                return redirect('forbidden')

            self.mn=mn
            form=MediaNamesForm.from_media_name(mn)

        except (MediaNames.DoesNotExist, KeyError) as e:
            form=MediaNamesForm(initial={'contributor_id': request.user.contributor.id})
            
        return self.form_invalid(form) 
        

    def post(self, request, *args, **kwargs):
        ''' accept edits to a MediaNames object (either existing or new) '''
        form=MediaNamesForm(request.POST)
        if not form.is_valid():
            # maybe do something about reformatting errors....
            return self.form_invalid(form)

        try:
            medid=form.cleaned_data.get('medid')
            if medid is not None:
                mn=MediaNames.objects.get(medid=medid)
        except MediaNames.DoesNotExist:
            raise Http404()

        try:
            with transaction.atomic():
                if medid is not None:
                    mn.delete()
                mn=self.build_mn(form) # saves everything
                self.mn=mn
        except IntegrityError as e:
            form.errors['error']=str(e)

        # random spurious comment

        # also have to save state between calls if there's an error
        # so Matt doesn't have to re-enter everything on any little mistake.

        # what is the mixin that checks the form for validity, does the create/edit,
        # and returns either form_invalid() or redirect()?
        success=len(form.errors)==0
        if success:
            return redirect(self.get_success_url())
        else:
            newform=MediaNamesForm(request.POST)
            for f,err in form.errors.items():
                newform.errors[f]=err
            return self.form_invalid(newform)



    def build_mn(self, form):
        fcd=form.cleaned_data
        media_name=fcd.get('media_name')
        is_defined='Y'
        is_minimal='Y' if fcd.get('is_minimal') else 'N'
        mn=MediaNames(media_name=media_name, is_defined=is_defined, is_minimal=is_minimal)
        medid=fcd.get('medid')
        if medid is not None:
            mn.medid=medid
        mn.save()

        # build media compound objects (don't want to try and re-use existing ones?)
        for compkey in [k for k in fcd.keys() if k.startswith('comp')]:
            comp_name=fcd.get(compkey)
            if comp_name is None or len(comp_name)==0:
                continue
            amt_key='amount'+compkey.split('comp')[1]
            amount=fcd.get(amt_key)
            if amount is None:
                form.errors[amt_key]='Amount needed for compound %s!' % comp_name # should have already been checked in form.is_valid()
                continue
            comp=Compounds.objects.with_name(comp_name)
            medcomp=MediaCompounds(compid=comp, amount_mm=amount)
            mn.mediacompounds_set.add(medcomp) # should save medcomp


        return mn

            
        
    def get_context_data(self, **kwargs):
        context=super(NewMediaView,self).get_context_data(**kwargs)
        try: context['mn']=self.mn
        except AttributeError: pass
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('media_record', args=(self.mn.medid,))

