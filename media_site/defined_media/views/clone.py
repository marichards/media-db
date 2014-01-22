import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms import NewMediaForm
from django.views.generic.edit import FormView
from defined_media.views.contributors import NewMediaView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

class CloneGrowthDataView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=NewMediaForm
    success_url='/defined_media/newmedia'

    def get(self, request, *args, **kwargs):

        try:
            old_gd=GrowthData.objects.get(growthid=kwargs['pk'])
        except GrowthData.DoesNotExist:
            raise Http404()         # or something

        contributor=request.user.contributor
        if not contributor.can_edit_gd(old_gd):
            return redirect('forbidden')

        new_gd=old_gd.clone_and_save(contributor)
        form=NewMediaForm.from_growth_data(new_gd)
#        form.is_valid()         # why? to get form.cleaned_data?

        context=self.get_context_data(new_gd=new_gd, 
                                      action=reverse('clone_growth_data', args=(new_gd.growthid,)), # this would change
                                      gd=new_gd,
                                      form=form,
                                      )
#        return self.render_to_response(context)
        return redirect('new_media_form', pk=new_gd.growthid)
        

