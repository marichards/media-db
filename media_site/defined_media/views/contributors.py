from defined_media.forms import NewMediaForm
from django.views.generic.edit import FormView

class NewMediaView(FormView):
	template_name='defined_media/newmedia_form.html'
	form_class=NewMediaForm
	
	def get_context_data(self, **kwargs):
		context=super(NewMediaView, self).get_context_data(**kwargs)
		context['fart']='brrappphhhh'
		return context
