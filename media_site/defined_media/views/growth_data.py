import logging
log=logging.getLogger(__name__)

from defined_media.models import *
from defined_media.forms import GrowthDataForm
from django.views.generic.edit import EditView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class CreateGrowthData(CreateView):
    model=GrowthData
