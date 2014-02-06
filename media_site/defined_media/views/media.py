import logging
log=logging.getLogger(__name__)

from defined_media.forms import MediaNamesForm
from defined_media.models import *

from django.views.generic.edit import FormView
from django.db import IntegrityError, transaction
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404

class NewMediaView(FormView):
    template_name='defined_media/medianames_form.html'
    form_class=MediaNamesForm

    def get(self, request, *args, **kwargs):
        ''' serve up an empty edit page, or one initialized with a MediaNames object, for editing '''
        log.debug('get() called')
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
        ''' accept edits to a MediaNames object (either existing or new) '''
        log.debug('hi from post')
        form=MediaNamesForm(request.POST)
        if not form.is_valid():
            # maybe do something about reformatting errors....
            log.debug('form not valid: errors=%s' % form.errors)
            return self.form_invalid()

        # probably something about getting/creating the MediaNames,
        # setting up its mediacompounds_set, and possibly saving
        try:
            with transaction.atomic():
                mn=self.get_medianames(form)
                if len(form.errors)>0:
                    raise IntegrityError('awww') # this gets caught and a different one raised in atomic.__exit__().  Or, not.
                self.mn=mn
        except Exception as e:
            log.debug('post: caught and ignoring %s: %s' % (type(e), e))
            log.exception(e)

        # error handling: have to make sure compounds exist and amounts
        # are kosher; do that in form.is_valid?

        # also have to save state between calls if there's an error
        # so Matt doesn't have to re-enter everything on any little mistake.

        # might also have to do the transaction thing
        
#        return super(NewMediaView,self).post(request, *args, **kwargs)
        # what is the mixin that checks the form for validity, does the create/edit,
        # and returns either form_invalid() or redirect()?
        log.debug('form.errors: %s' % form.errors)
        log.debug('len(form.errors): %d' % len(form.errors))
        success=len(form.errors)==0
        if success:
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_medianames(self, form):
        ''' get or create a MediaNames object based on the form values.
            If unable to create (eg, bad media compound), return None
            returns save()d MediaNames object.
        '''

        medid=form.cleaned_data.get('medid')
        if medid is not None:
            try:
                log.debug('returning medid from form')
                return MediaNames.objects.get(medid=medid)
            except MediaNames.DoesNotExist:
                pass

        # build from scratch:
        log.debug('building from scratch')
        is_defined='Y'
        is_minimal='Y' if form.cleaned_data.get('is_minimal') else 'N'
        media_name=form.cleaned_data.get('media_name')
        mn=MediaNames(media_name=media_name, is_defined=is_defined, is_minimal=is_minimal)

        mn.save()
        log.debug('MediaNames "%s" saved' % mn.media_name)

        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        log.debug('keys are %s' % keys)
        for key in keys:
            amt_key='amount'+key.split('comp')[1]
            amount=form.cleaned_data.get(amt_key)
            if amount is None:
                form.errors[amt_key]=' This field is required'
                log.debug('no amount for %s' % key)
                continue
            try:
                comp=Compounds.objects.with_name(form.cleaned_data.get(key))
                medcomp=MediaCompounds(medid=mn, compid=comp, amount_mm=amount)
                mn.mediacompounds_set.add(medcomp) # doesn't work unless mn has been saved
                log.debug('added medcomp %s' % medcomp)
            except Exception as e:
                log.debug('Unable to create compound for %s, %s: %s' % (form.cleaned_data.get(key), amount, e))
                form.errors[amt_key]='Bad compound'

        return mn
        
    def get_context_data(self, **kwargs):
        context=super(NewMediaView,self).get_context_data(**kwargs)
        try: context['mn']=self.mn
        except AttributeError: pass
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('media_record', args=(self.mn.medid,))


            
