import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms import NewCompoundMediaForm
from django.views.generic.edit import FormView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class NewGrowthData(CreateView):


class CloneGrowthDataView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=NewCompoundMediaForm
    success_url='/defined_media/newmedia'

    def get(self, request, *args, **kwargs):

        try:
            old_gd=GrowthData.objects.get(growthid=kwargs['pk'])
        except GrowthData.DoesNotExist:
            raise Http404()         # or something

        contributor=request.user.contributor
        new_gd=old_gd.clone_and_save(contributor)
        new_gd.approved=False;
        form=NewCompoundMediaForm.from_growth_data(new_gd)
#        form.is_valid()         # why? to get form.cleaned_data?

        context=self.get_context_data(new_gd=new_gd, 
                                      action=reverse('clone_growth_data', args=(new_gd.growthid,)), # this would change
                                      gd=new_gd,
                                      form=form,
                                      )
#        return self.render_to_response(context)
        return redirect('new_media_form', pk=new_gd.growthid)
        


