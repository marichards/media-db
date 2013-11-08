import logging
log=logging.getLogger(__name__)

from defined_media.forms import NewMediaForm
from defined_media.models import *
from django.views.generic.edit import FormView
from django.db import transaction

#from django.core.urlresolvers import reverse

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

    def post(self, request, *args, **kwargs):
        try:
            form=NewMediaForm(request.POST)
            form.orig_data=request.POST
            valid=form.is_valid()
            
            if not valid:
                return self.form_invalid(form)
            
            media_name=self.get_media_name(form)
            if media_name==None: 
                return self.form_invalid(form)
            media_name.save()

            growth_data=self.get_growth_data(form, media_name)
            if not growth_data: 
                return self.form_invalid(form)
            growth_data.save()
            
            media_comps=self.get_media_comps(form, media_name)
            if len(media_comps)==0:
                form.errors['MediaCompounds']='No valid compound/amount pairs found'
                return self.form_invalid(form)
            for mcomp in media_comps:
                mcomp.save()
            
            uptakes=self.get_uptakes(form, growth_data)
            log.debug('%d new uptakes' % len(uptakes))
            for uptake in uptakes:
                uptake.save()
                
            if len(form.errors)==0:
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        finally:
            form.reformat_errors()


    def get_organism(self, form):
        try:
            return Organisms.objects.get(genus=form.cleaned_data['genus'][0],
                                        species=form.cleaned_data['species'][0],
                                        strain=form.cleaned_data['strain'][0])
        except Organisms.DoesNotExist, e:
            form.errors['Organism']="No such organism: "+str(e)
            return None
    
    def get_media_name(self, form):
        try:
            m=MediaNames.objects.get(media_name=form.cleaned_data['media_name'][0])
            return m
        except MediaNames.DoesNotExist:
            try:
                is_defined='Y' if 'is_defined' in self.request.POST else 'N'
                is_minimal='Y' if 'is_minimal' in self.request.POST else 'N'

                args={'media_name': form.cleaned_data['media_name'][0],
                      'is_defined': is_defined,
                      'is_minimal': is_minimal
                      }
                return MediaNames(**args)
            except Exception, e:
                form.errors['MediaNames']="Unable to create media name record: "+str(e)
                return None

    def get_media_comps(self, form, media_name):
        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        med_comps=[]
        for ckey in keys:
            try:
                n=ckey.split('comp')[1]
                akey='amount'+n
                comp=Compounds.objects.with_name(form.cleaned_data[ckey][0])
                amount=form.cleaned_data[akey][0]
                if amount==None: raise ValueError()
                med_comp=MediaCompounds(medid=media_name, compid=comp, amount_mm=amount)
                med_comps.append(med_comp)
            except Compounds.DoesNotExist:
                form.errors[ckey]='No compounds for %s' % form.cleaned_data[ckey][0]
            except ValueError:
                form.errors[ckey]='No amount provided for %s' % form.cleaned_data[ckey][0]
            except Exception, e:
                form.errors[ckey]='Error: %s' % e

        return med_comps

    def get_growth_data(self, form, media_name):
        try:
            org=self.get_organism(form)
            source=self.get_source(form)

            if not (org and source and media_name):
                return None


            args={'strainid': org,
                  'medid': media_name,
                  'sourceid': source,
                  'growth_rate': form.cleaned_data['growth_rate'][0],
                  'growth_units': '1/h',
                  'ph': form.cleaned_data['ph'][0],
                  'temperature_c': form.cleaned_data['temperature'][0],
                  'additional_notes': '',
                  }
            return GrowthData(**args)
        except Exception, e:
            form.errors['GrowthData']="Unable to create growth data record: "+str(e)
            return None

    def get_source(self, form):
        title=form.cleaned_data['title'][0]
        try:
            return Sources.objects.get(title=title)
        except Sources.DoesNotExist:
            try:
                args={'title': form.cleaned_data['title'][0],
                      'journal': form.cleaned_data['journal'][0],
                      'first_author': form.cleaned_data['first_author'][0],
                      'year': int(form.cleaned_data['year'][0]),
                      'link': form.cleaned_data['link'][0]}
                src=Sources.objects.create(**args)
                return src
            except Exception, e:
                form.errors['Sources']="Unable to create source record: "+str(e)
                return None


                          

    def get_uptakes(self, form, gd):
        '''
        return a list of saved SecretionUptake objects
        each obj needs a growthdata object (shared), a compound/rate/units triple, and a rate type
        '''
        uptakes=[]
        for key in [k for k in form.cleaned_data.keys() if k.startswith('uptake_comp')]:
            try:
                n=key.split('uptake_comp')[1]
                try: comp_name=form.cleaned_data[key][0]
                except IndexError: continue # this only happens for key=='uptake_comp1'
                    
                comp=Compounds.objects.with_name(comp_name)
                log.debug('uptakes: compound%s is %s' % (n, comp))
                rate=form.cleaned_data['uptake_rate'+n][0]
                up_type_id=form.cleaned_data['uptake_type'+n][0]
                up_type=SecretionUptakeKey(rateid=up_type_id)
                log.debug('up_type is %s' % up_type)
                units=form.cleaned_data['uptake_unit'+n][0]
                log.debug('gd is %r' % gd)
                uptake=SecretionUptake(growthid=gd,
                                       compid=comp.compid,
                                       rate=rate,
                                       units=units,
                                       rateid=up_type)
                uptakes.append(uptake)
            except Exception, e:
                log.debug('trying to create SecretionUptake object: caught %s: %s' % (type(e),e))
                form.errors[key]='Error creating secretion-uptake(%s): %s' % (type(e), e)
        return uptakes
