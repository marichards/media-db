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


    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form=NewMediaForm(request.POST)

        try:
            if not form.is_valid():
                log.debug('form is invalid, aborting')
                return self.form_invalid(form)
            
            org=self.get_organism(form)
            source=self.get_source(form)

            media_name=self.get_media_name(form)
            media_name.save()

            growth_data=self.get_growth_data(form, org, source, media_name)
            growth_data.save()
            
            media_comps=self.get_media_comps(form, media_name)
            for mcomp in media_comps:
                mcomp.save()
            
            uptakes=self.get_uptakes(form, growth_data)
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
            raise e
    
    def get_media_name(self, form):
        try:
            return MediaNames.objects.get(media_name=form.cleaned_data['media_name'][0])
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
                raise e

    def get_media_comps(self, form, media_name):
        ''' get the list of comp/amount objects, referencing the media_name object: '''
        keys=[k for k in form.cleaned_data.keys() if k.startswith('comp')]
        med_comps=[]
        for ckey in keys:
            n=ckey.split('comp')[1]
            akey='amount'+n
            comp=Compounds.objects.with_name(form.cleaned_data[ckey][0])
            amount=form.cleaned_data[akey][0]
            med_comp=MediaCompounds(medid=media_name, compid=comp, amount_mm=amount)
            med_comps.append(med_comp)

        return med_comps

    def get_media_comps_old(self, form, media_name):
        ''' get the list of comp/amount objects, referencing the media_name object: '''
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
            except Compounds.DoesNotExist as e:
                form.errors[ckey]='No compounds for %s' % form.cleaned_data[ckey][0]
                raise e
            except ValueError as e:
                form.errors[ckey]='No amount provided for %s' % form.cleaned_data[ckey][0]
                raise e
            except Exception as e:
                form.errors[ckey]='Error: %s' % e
                raise e

        if len(med_comps)==0:
            form.errors['MediaCompounds']='No valid compound/amount pairs found'
            raise ValueError

        return med_comps

    def get_growth_data_old(self, form, org, source, media_name):
        try:
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
            raise e

    def get_growth_data(self, form, org, source, media_name):
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

    def get_source(self, form):
        title=form.cleaned_data['title'][0]
        try:
            return Sources.objects.get(title=title)
        except Sources.DoesNotExist:
            args={'title': form.cleaned_data['title'][0],
                  'journal': form.cleaned_data['journal'][0],
                  'first_author': form.cleaned_data['first_author'][0],
                  'year': int(form.cleaned_data['year'][0]),
                  'link': form.cleaned_data['link'][0]}
            src=Sources.objects.create(**args)
            return src


                          

    def get_uptakes(self, form, gd):
        '''
        return a list of saved SecretionUptake objects
        each obj needs a growthdata object (shared), a compound/rate/units triple, and a rate type
        '''
        uptakes=[]
        for key in [k for k in form.cleaned_data.keys() if k.startswith('uptake_comp')]:
            n=key.split('uptake_comp')[1]
            try: comp_name=form.cleaned_data[key][0]
            except IndexError: continue # this only happens for key=='uptake_comp1'
            
            comp=Compounds.objects.with_name(comp_name)
            rate=form.cleaned_data['uptake_rate'+n][0]
            up_type_id=form.cleaned_data['uptake_type'+n][0]
            up_type=SecretionUptakeKey(rateid=up_type_id)
            units=form.cleaned_data['uptake_unit'+n][0]
            uptake=SecretionUptake(growthid=gd,
                                   compid=comp.compid,
                                   rate=rate,
                                   units=units,
                                   rateid=up_type)
            uptakes.append(uptake)
        return uptakes
