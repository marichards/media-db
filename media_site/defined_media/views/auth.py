########################################################################
'''
import django.contrib.auth.views as auth_views

def df_login(request, *args, **kwargs):
	return auth_views.login(request, 'defined_media/login_page.html')

def df_logout(request, *args, **kwargs):
	return auth_views.logout(request, 
				 template_name='defined_media/login_page.html',
				 extra_context=kwargs)

from django.views.generic.edit import CreateView
from defined_media.models import Contributor
from defined_media.forms import CreateContributorForm

class CreateContributor(CreateView):
	model=Contributor
	form_class=CreateContributorForm

	def render_to_response1(context, **kwargs):
		print 'got here'
		return super(CreateContributor, self).render_to_response(context, **kwargs)

'''

########################################################################
