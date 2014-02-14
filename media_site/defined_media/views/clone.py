import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms.growth_data_form import GrowthDataForm
from defined_media.forms.media_names_form import MediaNamesForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

class CloneGrowthDataView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=GrowthDataForm
    success_url='/defined_media/newmedia'

    def get(self, request, *args, **kwargs):

        try:
            old_gd=GrowthData.objects.get(growthid=kwargs['pk'])
        except GrowthData.DoesNotExist:
            raise Http404()         # or something

        contributor=request.user.contributor
        new_gd=old_gd.clone_and_save(contributor)
        new_gd.approved=False;
        form=GrowthDataForm.from_growth_data(new_gd)

        context=self.get_context_data(new_gd=new_gd, 
                                      action=reverse('clone_growth_data', args=(new_gd.growthid,)), # this would change
                                      gd=new_gd,
                                      form=form,
                                      )
        # redirect to edit form:
        return redirect('edit_growth_data', pk=new_gd.growthid)
        


class CloneMediaNamesView(FormView):
    # I don't know that these three are actually used... They're certainly suspect (or even wrong)
#    template_name='defined_media/medianames_form.html'
#    form_class=MediaNamesForm
#    success_url='/defined_media/newmedia'

    def get(self, request, *args, **kwargs):
        try:
            old_mn=MediaNames.objects.get(medid=kwargs['pk'])
        except MediaNames.DoesNotExist:
            raise Http404()         # or something

        new_mn=old_mn.clone()
#        new_mn.approved=False;
        form=MediaNamesForm.from_media_name(new_mn)

        context=self.get_context_data(new_mn=new_mn, 
#                                      action=reverse('clone_growth_data', args=(new_mn.medid,)), # this would change
                                      mn=new_mn,
                                      form=form,
                                      )
        # redirect to edit form:
        return redirect('new_media', pk=new_mn.medid)
        


