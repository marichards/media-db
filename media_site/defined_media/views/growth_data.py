from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.db import transaction, IntegrityError

import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms.growth_data_form import GrowthDataForm


class GrowthDataView(FormView):
    form_class=GrowthDataForm
    template_name='defined_media/growthdata_form.html'

    def get(self, request, *args, **kwargs):
        ''' serve up an edit page, either empty of filled out with the gd: '''
        try:
            gd=GrowthData.objects.get(growthid=kwargs['pk'])
            user=request.user
            if not user.contributor.can_edit_gd(gd):
                return redirect('forbidden')
            self.gd=gd
            form=self.form_class.from_growth_data(gd)
        except (GrowthData.DoesNotExist, KeyError) as e:
            form=GrowthDataForm(initial={'contributor': request.user.contributor.id})
        
        return self.form_invalid(form)
            
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        log.debug('request.POST: %s' % request.POST)
        if not form.is_valid():
            return self.form_invalid(form)

        # determine if this is a new creation or an update:
        try:
            growthid=form.cleaned_data.get('growthid')
            if growthid is not None:
                gd=GrowthData.objects.get(growthid=growthid)
                log.debug('got existing growth_record %s' % growthid)
        except GrowthData.DoesNotExist:
            raise Http404()

        # make database changes:
        try:
            with transaction.atomic():
                if growthid is not None:
                    gd.delete()
                gd=self.build_gd(form)
                self.add_secretion_uptakes(form, gd)
                self.gd=gd
        except IntegrityError:
            form.errors['error']=str(e)

        # are we happy?
        if len(form.errors)==0:
            return redirect(self.get_success_url())
        else:
            newform=self.form_class(request.POST) # can't just return self.form_invalid(form)???
            newform.errors.update(form.errors)
            return self.form_invalid(newform)

    def build_gd(self, form):
        '''
        build and save the growth_data object from the form, including secretion_uptakes (nyi)
        fixme: also does no error handling as yet.
        '''
        fcd=form.cleaned_data   # convenience
        contributor=Contributor.objects.get(id=fcd.get('contributor'))
        strainid=fcd.get('strainid')
        sourceid=fcd.get('sourceid')
        medid=medid=fcd.get('medid')
        
        growth_rate=fcd.get('growth_rate')
        temperature_c=fcd.get('temperature_c')
        ph=fcd.get('ph')
        additional_notes=fcd.get('additional_notes')

        gd=GrowthData(contributor=contributor,
                      strainid=strainid,
                      sourceid=sourceid,
                      medid=medid,

                      growth_rate=growth_rate,
                      temperature_c=temperature_c,
                      ph=ph,
                      additional_notes=additional_notes)
        growthid=fcd.get('growthid')
        log.debug('about to save growth_record: growthid=%s' % growthid)

        if growthid is not None:
            gd.growthid=growthid
        gd.save()
        return gd

    def add_secretion_uptakes(self, form, gd):
        fcd=form.cleaned_data
        upkeys=[k for k in fcd.keys() if k.startswith('uptake_comp')]
        log.debug('gd.add_secs: upkeys: %s' % upkeys)
        for upkey in upkeys:
            n=upkey.split('uptake_comp')[1]
            comp_name=fcd.get(upkey)
            if comp_name is None or len(comp_name)==0:
                continue
            log.debug('%s: looking for %s' % (upkey, comp_name))
            compound=Compounds.objects.with_name(comp_name)
            rate=fcd.get('uptake_rate%s'%n)
            units=fcd.get('uptake_units%s'%n)
            rate_type=fcd.get('uptake_type%s'%n)
            rateid=SecretionUptakeKey.objects.get(rate_type=rate_type)
            uptake=SecretionUptake(compid=compound.compid, rate=rate, units=units, rateid=rateid)
            gd.secretionuptake_set.add(uptake)



    def get_context_data(self, **kwargs):
        context=super(GrowthDataView,self).get_context_data(**kwargs)
        try: context['gd']=self.gd
        except AttributeError: pass
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('growth_record', args=(self.gd.growthid,))


