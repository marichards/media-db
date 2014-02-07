import logging
log=logging.getLogger(__name__)

from defined_media.forms import MediaNamesForm
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
            log.debug('mn: %s' % mn)
            user=request.user
            if not user.contributor.can_edit_mn(mn):
                return redirect('forbidden')

            self.mn=mn
            form=MediaNamesForm.from_media_name(mn)
            log.debug('created form from mn')

        except (MediaNames.DoesNotExist, KeyError) as e:
            log.debug('get: caught %s: %s' % (type(e), e))
            form=MediaNamesForm(initial={'contributor_id': request.user.contributor.id})
            log.debug('created empty form')
            
        return self.form_invalid(form) 
        

    def post(self, request, *args, **kwargs):
        ''' accept edits to a MediaNames object (either existing or new) '''
        log.debug('uh, hi?')
        form=MediaNamesForm(request.POST)
        if not form.is_valid():
            # maybe do something about reformatting errors....
            log.debug('form not valid: errors=%s' % form.errors)
            return self.form_invalid(form)

        # probably something about getting/creating the MediaNames,
        # setting up its mediacompounds_set, and possibly saving
        comps=self.get_compounds(form)
        try:
            with transaction.atomic():
                mn=self.get_medianames(form, comps)
                self.mn=mn                       # this used to be just after the assignment to mn=...; why moved again????  
                log.debug('after get_medianames: %d form errors: %s' % (len(form.errors), ', '.join(form.errors.keys())))
                for f,err in form.errors.items():
                    log.debug('form.errors[%s]: %s' % (f,err))

                if len(form.errors)>0:
                    raise IntegrityError('awww') # this gets caught and a different one raised in atomic.__exit__().  Or, not.  Well, sometimes.
        except Exception as e:
            log.debug('post: caught and ignoring %s: %s' % (type(e), e))
#            log.exception(e)
            pass

        # also have to save state between calls if there's an error
        # so Matt doesn't have to re-enter everything on any little mistake.

        # what is the mixin that checks the form for validity, does the create/edit,
        # and returns either form_invalid() or redirect()?
        success=len(form.errors)==0
        if success:
            log.debug('post: success')
            return redirect(self.get_success_url())
        else:
            log.debug('post: failure: %d mediacomps in mn' % self.mn.mediacompounds_set.count())
#            log.debug('post: failure: creating form from:')
            # rollbacks probably cause mn to lose all medcomps?  But it shouldn't...
            d=mn.as_dict()
#            for k,v in d.items():
#                log.debug('d[%s]: %s' % (k,v))
            newform=MediaNamesForm(mn.as_dict())
            for f,err in form.errors.items():
                newform.errors[f]=err
            return self.form_invalid(newform)

    def get_medianames(self, form, comps):
        ''' get or create a MediaNames object based on the form values.
            If unable to create (eg, bad media compound), return None
            returns save()d MediaNames object.
        '''


        medid=form.cleaned_data.get('medid')
        if False:
#        if medid is not None:
            # This is a bug; regardless of the form, we just return this and call it a day
            try:
                log.debug('returning medid %s from form' % medid)
                return MediaNames.objects.get(medid=medid)
            except MediaNames.DoesNotExist:
                pass

        # build from scratch:
        log.debug('building from scratch')
        medid=form.cleaned_data.get('medid')
        media_name=form.cleaned_data.get('media_name')
        is_defined='Y'
        is_minimal='Y' if form.cleaned_data.get('is_minimal') else 'N'
        mn=MediaNames(medid=medid, media_name=media_name, is_defined=is_defined, is_minimal=is_minimal)

        mn.save()
        log.debug('MediaNames "%s" saved' % mn.media_name)

        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        for key in keys:
            amt_key='amount'+key.split('comp')[1]
            amount=form.cleaned_data.get(amt_key)
            if amount is None:
                form.errors[amt_key]=' This field is required'
                log.debug('no amount for %s' % key)
                continue
            log.debug('%s: %s' % (amt_key, amount))
            try:
                comp=comps[key]
                medcomp=MediaCompounds(medid=mn, compid=comp, amount_mm=amount)
                mn.mediacompounds_set.add(medcomp) # doesn't work unless mn has been saved
                log.debug('added medcomp %s' % medcomp)
            except TransactionManagementError as e:
                log.debug('Transaction Management Error, probably due to trying to add existing media_comp; ignoring')
            except IntegrityError as e:
                log.debug('IntegrityError: %s, probably due to trying to add existing media_comp; ignoring' % e)
            except Exception as e:
                log.debug('Unable to create compound for %s, %s: %s (%s)' % (form.cleaned_data.get(key), amount, e, type(e)))
#                log.exception(e)
                form.errors[amt_key]='Bad compound'

        return mn
        
    def get_compounds(self, form):
        '''
        Return a hash: k=compound key, v=compound
        Have to do this because apparently you can't query the db from within the transaction
        '''
        comps={}
        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        for key in keys:
            name=form.cleaned_data.get(key)
            try:
                comps[key]=Compounds.objects.with_name(name)
            except Compounds.DoesNotExist as e:
                form.errors[key]='Unknown compound: %s' % name
                comps[key]=None
        return comps

    def get_context_data(self, **kwargs):
        context=super(NewMediaView,self).get_context_data(**kwargs)
        try: context['mn']=self.mn
        except AttributeError: pass
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('media_record', args=(self.mn.medid,))


            
