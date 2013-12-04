import logging
log=logging.getLogger(__name__)

from defined_media.forms import NewMediaForm
from defined_media.models import *

from django.views.generic.edit import FormView
from django.db import transaction, IntegrityError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class NewMediaView(FormView):
    '''
    Basic "goal" is to store one GrowthData record, with as many attendent 
    compound/amount pairs (MediaCompound) records as provided.  Additionally,
    a source (Sources) record must be cited.  Finally, a variable number of 
    secretion uptake records may be associated with the growth data record.
    '''
    template_name='defined_media/newmedia_form.html'
    form_class=NewMediaForm
#    success_url=reverse('new_media_form')
    success_url='/defined_media/newmedia'

    def get_context_data(self, *args, **kwargs):
        context = super(NewMediaView, self).get_context_data(**kwargs)
        try:
            context['gd']=self.gd
        except (KeyError, AttributeError) as e:
            log.debug('no self.gd found')
            pass
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.gd=GrowthData.objects.get(growthid=kwargs['pk'])
            form=NewMediaForm.from_growth_data(self.gd)
        except (GrowthData.DoesNotExist, KeyError):
            form=NewMediaForm()
            
        return self.form_invalid(form) 


#    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form=NewMediaForm(request.POST)

        if not form.is_valid():
            log.debug('form is invalid, aborting')
            form.reformat_errors()
            return self.form_invalid(form)

        try:
            org=self.get_organism(form)
            source=self.get_source(form)
            media_name=self.get_media_name(form)

#            with transaction.atomic():
            try:
                try: 
                    growthid=request.POST['growthid']
                    old_gd=GrowthData.objects.get(growthid=int(growthid)) # here
                    old_gd.full_delete()
                except (KeyError, ValueError) as e:
                    log.debug('no valid growthid in form, not trying to call full_delete')
                    pass

                media_name.save()

                growth_data=self.get_growth_data(form, org, source, media_name)
                growth_data.save()  # this can barf on IntegrityError: duplicate entry '8-304-113-1-7-35' for key 'unique_conditions' ????
                log.debug('growth_data saved: growthid=%d' % growth_data.growthid)

                media_comps=self.get_media_comps(form, media_name)
                for mcomp in media_comps:
                    mcomp.save()

                uptakes=self.get_uptakes(form, growth_data)
                for uptake in uptakes:
                    uptake.save()
                
                transaction.commit()
                log.debug('yay! commitment!')
            except IntegrityError as ie:
                log.debug('caught %s: %s; rolling back' % (type(ie), ie))
                log.debug('growth_data is: %r' % growth_data)
                transaction.rollback()
                form.errors['Error']=str(ie)

        finally:
            form.reformat_errors()

        if len(form.errors)==0:
            log.debug('growth_data.growthid: %s' % growth_data.growthid)
            url=reverse('new_media_form', args=(growth_data.growthid,))
            return redirect(url)
        else:
            return self.form_invalid(form)


    def get_organism(self, form):
        try:
            return Organisms.objects.get(genus=form.get1('genus'),
                                        species=form.get1('species'),
                                        strain=form.get1('strain'))
        except Organisms.DoesNotExist, e:
            form.errors['Organism']="No such organism: "+str(e)
            raise e
    
    def get_media_name(self, form):
        try:
            return MediaNames.objects.get(media_name=form.get1('media_name'))
        except MediaNames.DoesNotExist:
            try:
                is_defined='Y' if 'is_defined' in self.request.POST else 'N'
                is_minimal='Y' if 'is_minimal' in self.request.POST else 'N'
                
                args={'media_name': form.get1('media_name'),
                      'is_defined': is_defined,
                      'is_minimal': is_minimal
                      }
                return MediaNames(**args)
            except Exception, e:
                form.errors['MediaNames']="Unable to create media name record: "+str(e)
                raise e

    def get_media_comps(self, form, media_name):
        ''' get the list of comp/amount objects, referencing the media_name object: '''
        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        med_comps=[]
        for ckey in keys:
            n=ckey.split('comp')[1]
            akey='amount'+n
            comp=Compounds.objects.with_name(form.get1(ckey))
            amount=form.get1(akey)
            med_comp=MediaCompounds(medid=media_name, compid=comp, amount_mm=amount)
            med_comps.append(med_comp)

        return med_comps

    def get_growth_data(self, form, org, source, media_name):
        args={'strainid': org,
              'medid': media_name,
              'sourceid': source,
              'growth_rate': form.get1('growth_rate'),
              'growth_units': '1/h',
              'ph': form.get1('ph'),
              'temperature_c': form.get1('temperature'),
              'additional_notes': '',
              }
        try:
            args['growthid']=form.get1('growthid', int)
            log.debug('existing args[growthid]=%s' % args['growthid'])
        except (ValueError, KeyError, TypeError) as e:
            log.debug('get_growth_data: no "growthid" form (ok)')
            pass

        gd=GrowthData(**args)
        gd.strainid=org
        gd.sourceid=source
        gd.medid=media_name
        return gd

    def get_source(self, form):
        ''' fixme: what happens if one field of an existing Sources record is changed?
            create a totally new record?  Leave the old record dangling?
        '''
        fields=['first_author', 'journal', 'year', 'title', 'link']
        args={k:v for (k,v) in [(f,form.get1(f)) for f in fields]}
        try:
            src, created=Sources.objects.get_or_create(**args)
        except IntegrityError as e:
            form.errors['Sources']='Error creating Source: %s' % e
            raise e
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
                log.debug('comp_name for key=%s: %s'% (key, comp_name))
                if comp_name==None or len(comp_name)==0: continue # ignore the whole row
            except (TypeError, ValueError) as e: 
                log.debug('no comp_name for key=%s: e=%s' % (key, e))
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
            uptakes.append(uptake)
        return uptakes


