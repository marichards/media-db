import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms import NewMediaForm
from django.views.generic.edit import FormView
from defined_media.views.contributors import NewMediaView
from django.core.urlresolvers import reverse

class CloneGrowthDataView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=NewMediaForm
    success_url='/defined_media/newmedia'

    def get(self, request, *args, **kwargs):

        try:
            old_gd=GrowthData.objects.get(growthid=kwargs['pk'])
        except GrowthData.DoesNotExist:
            raise Http404()         # or something

        user=request.user
        if old_gd.contributor_id != user.contributor.id:
            return redirect('forbidden')

        new_gd=old_gd.clone()
        form=NewMediaForm.from_growth_data(new_gd)
        form.is_valid()
        log.debug('form is %s' % form.cleaned_data)
        
        return self.form_invalid(form, new_gd)

    def form_invalid(self, form, new_gd, **kwargs):
        context = super(CloneGrowthDataView, self).get_context_data(**kwargs)
        context['action']=reverse('clone_growth_data', args=(new_gd.growthid,))
        context['gd']=new_gd
        context['form']=form
        return self.render_to_response(context)

#    def post(self, request, *args, **kwargs):
#       # don't think we'll even get here if using NewMediaView
        


