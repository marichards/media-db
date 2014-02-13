
from django.views.generic.edit import CreateView

import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms.growth_data_form import GrowthDataForm
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class CreateGrowthDataView(CreateView):
    form_class=GrowthDataForm
    template_name='defined_media/growthdata_form.html'

    def get_success_url(self):
        return reverse('growth_record', args=(self.object.growthid,))