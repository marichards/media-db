from defined_media.forms import NewMediaForm
from django.views.generic.edit import FormView

class NewMediaView(FormView):
	template_name='defined_media/newmedia_form.html'
	form_class=NewMediaForm
