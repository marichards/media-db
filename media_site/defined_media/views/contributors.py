import logging
log=logging.getLogger(__name__)

from defined_media.forms import NewCompoundMediaForm, OrganismForm
from defined_media.models import *

from django.views.generic.edit import FormView, CreateView
from django.db import transaction, IntegrityError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404


class NewGrowthDataView(FormView):
    '''
    Basic "goal" is to store one GrowthData record, with as many attendent 
    compound/amount pairs (MediaCompound) records as provided.  Additionally,
    a source (Sources) record must be cited.  Finally, a variable number of 
    secretion uptake records may be associated with the growth data record.
    '''
    template_name='defined_media/newmedia_form.html'
    form_class=NewCompoundMediaForm
#    success_url=reverse('new_media_form')
    success_url='/defined_media/newmedia'

    def get_context_data(self, *args, **kwargs):
        context = super(NewMediaView, self).get_context_data(**kwargs)
        try: context['gd']=self.gd
        except (KeyError, AttributeError) as e: pass
        return context

    # login_required, as per urls.py
    def get(self, request, *args, **kwargs):
        try:
            gd=GrowthData.objects.get(growthid=kwargs['pk'])
            self.gd=gd
            user=request.user
            if not user.contributor.can_edit_gd(gd):
                return redirect('forbidden')

            form=NewCompoundMediaForm.from_growth_data(gd)
        except (GrowthData.DoesNotExist, KeyError):
            form=NewCompoundMediaForm(initial={'contributor_id': request.user.contributor.id})
            
        return self.form_invalid(form) 


    # login_required, as per urls.py
#    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form=NewCompoundMediaForm(request.POST)

        # fixme: this only reports on certain errors; omits errors in get_organism, etc.
        # originally, it was meant that if the form was valid, we could go ahead and
        # create everything.
        if not form.is_valid():
            log.debug('form is invalid, aborting')
            form.reformat_errors()
            return self.form_invalid(form)

#        form.is_valid()   # checks errors, allows processing to continue so we can detect more errors
        # as it currently stands, some errors that should cause a rollback currently 
        # don't (eg missing amount1)
        try:
            with transaction.atomic():
                growth_data=self.get_growth_data(form)
                growth_data.strainid=self.get_organism(form)
                growth_data.sourceid=self.get_source(growth_data, form)
                growth_data.medid=self.get_media_name(growth_data, form)
                
                clone=growth_data.find_clone()
                log.debug('looking for clone; got: %r' % clone)
                if clone is not None:
                    form.errors['Clone']='A growth record with the same information (strain, media name, source, growth rate, ph, and temperature) already exists'
                    raise Exception('clone found')

                growth_data.save() # to get growth_data.growthid, so we can add objects:
            
                for media_comp in growth_data.medid.mediacompounds_set.all():
                    media_comp.delete()
                media_comps=self.get_media_comps(form, growth_data.medid) # barfing on missing key
                for mcomp in media_comps:
                    if mcomp not in growth_data.medid.mediacompounds_set.all():
                        growth_data.medid.mediacompounds_set.add(mcomp)


                for uptake in growth_data.secretionuptake_set.all():
                    uptake.delete()
                uptakes=self.get_uptakes(form, growth_data)
                log.debug('get_uptakes returned %d uptakes' % len(uptakes))
                log.debug('start: %d uptakes in gd' % growth_data.secretionuptake_set.count())
                for uptake in growth_data.secretionuptake_set.all():
                    log.debug('gd.uptake: %s' % uptake)
                for uptake in uptakes:
                    if uptake not in growth_data.secretionuptake_set.all():
                        growth_data.secretionuptake_set.add(uptake) # adding also calls .save()
                        log.debug('appending: %s' % uptake)
                    else:
                        log.debug('skipping uptake %s' % uptake)
                log.debug('finish: %d uptakes in gd' % growth_data.secretionuptake_set.count())
                

        except Exception as e:
            log.debug('caught and ignoring %s: %s' % (type(e), e))
            log.exception(e)
            form.errors['Error']=str(e)

        log.debug('%d form.errors' % len(form.errors))
        for k,v in form.errors.items():
            log.debug('error: %s=%s' % (k,v))

        form.reformat_errors()
        if len(form.errors)==0 and growth_data: # fixme: all these conditions still necessary?
            # on success, redirect to growth record detail:
            url=reverse('growth_record', args=(growth_data.growthid,))
            log.debug('returning redirect to %s code=302' % url)
            return redirect(url)
        else:
            log.debug('returning form_invalid (code=200(?))')
            return self.form_invalid(form) # status code 200, right?


    def get_growth_data(self, form):
        '''
        return an existing growth_data record, based on the form's growthid field, 
        or create a new one:
        '''
        try:
            gd=GrowthData.objects.get(growthid=form.get1('growthid'))
        except (KeyError, GrowthData.DoesNotExist) as e:
            gd=GrowthData()

        gd.approved=form.get1('approved')
        gd.contributor_id=form.get1('contributor_id')
        gd.growth_units='1/h'
        gd.additional_notes=form.get1('additional_notes')

        # these really shouldn't be necessary; form.cleaned_data is supposed to 
        # do the conversions for us, and get1 does use cleaned_data
        conversions={'ph': float,
                     'growth_rate': float,
                     'temperature_c': float}
        for f,t in conversions.items():
            try:
                setattr(gd,f,form.get1(f,t))
#                log.debug('set gd.%s to %s' % (f, getattr(gd, f)))
            except (ValueError, KeyError, TypeError) as e:
#                log.debug('get_growth_data: no "%s" form (ok)' % f)
                pass

        return gd

    def get_organism(self, form):
        genus, species, strain, new_org=form.get_organism_name()

        if new_org:
            typeid=form.get1('new_org_type')
            new_type=TypesOfOrganisms.objects.get(typeid=typeid)
            org=Organisms(genus=genus, species=species, strain=strain, typeid=new_type)
            return org

        try:
            return Organisms.objects.get(genus=genus,
                                        species=species,
                                        strain=strain)
        except Organisms.DoesNotExist, e:
            form.errors['Organism']="No such organism: "+str(e)
            raise e
    
    def get_media_name(self, gd, form):
        try:
            medid=gd.medid
        except (AttributeError, MediaNames.DoesNotExist) as e:
            medid=MediaNames()

        # now update fields (might already be the same):
        medid.media_name=form.get1('media_name')
        medid.is_defined='Y'  # always
        medid.is_minimal='Y' if 'is_minimal' in self.request.POST else 'N'
        medid.save()
        return medid

    def get_media_comps(self, form, media_name):
        ''' get the list of comp/amount objects, referencing the media_name object: '''
        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        med_comps=[]
        for ckey in keys:
            n=ckey.split('comp')[1]
            akey='amount'+n
            comp=Compounds.objects.with_name(form.get1(ckey))
            try: amount=form.get1(akey)
            except KeyError: amount=None
            med_comp=MediaCompounds(medid=media_name, compid=comp, amount_mm=amount)
            med_comps.append(med_comp)

        return med_comps


    def get_source(self, gd, form):
        ''' fixme: what happens if one field of an existing Sources record is changed?
            create a totally new record?  Leave the old record dangling?
        '''
        try:
            src=Sources.objects.get(pk=gd.sourceid_id)
        except Sources.DoesNotExist:
            fields=['first_author', 'journal', 'year', 'title', 'link']
            args=dict((k,v) for (k,v) in [(f,form.get1(f)) for f in fields])
            try:
                src=Sources.objects.get(**args)
            except Exception as e:
                src=Sources(**args)
        src.save()
        return src

    def get_uptakes(self, form, gd):
        '''
        return a list of saved SecretionUptake objects
        each obj needs a growthdata object (shared), a compound/rate/units triple, and a rate type
        '''
        uptakes=[]
        for key in [k for k in form.cleaned_data.keys() if k.startswith('uptake_comp')]:
            n=key.split('uptake_comp')[1]
            try: 
                comp_name=form.get1(key)
                if comp_name==None or len(comp_name)==0: continue # ignore the whole row
            except (TypeError, ValueError) as e: 
#                log.debug('no comp_name for key=%s: e=%s' % (key, e))
                continue # this only happens for key=='uptake_comp1'
            
            try:
                comp=Compounds.objects.with_name(comp_name)
            except Compounds.DoesNotExist as e:
                log.debug('get_uptakes: %s: no such compound for key=%s' % (comp_name, key))
                form.errors[key]='%s: no such compound' % comp_name
                raise IntegrityError(e)
                continue

            rate=form.get1('uptake_rate'+n)
            up_type_id=form.get1('uptake_type'+n)
            up_type=SecretionUptakeKey(rateid=up_type_id)
            units=form.get1('uptake_unit'+n)
            uptake=SecretionUptake(growthid=gd,
                                   compid=comp.compid,
                                   rate=rate,
                                   units=units,
                                   rateid=up_type)
            log.debug('get_uptakes() appending: %s' % uptake)
            uptakes.append(uptake)
        return uptakes


