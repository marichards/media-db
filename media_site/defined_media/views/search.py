from defined_media.forms import SearchForm
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

class SearchView(FormView):
	form_class=SearchForm
	template_name='defined_media/searchresult_list.html'

class SearchResultsView(ListView, FormView):
	template_name='defined_media/searchresult_list.html'

	def get(self, request, *args, **kwargs):

		form_class=SearchForm
		form=self.get_form(form_class)

		self.object_list=[]
		c={'form':form, 'object_list':self.object_list}
		st=self._get_search_term()
		if st:
			self.object_list=self.get_queryset()
			c.update({'object_list' : self.object_list,
				  'search_term' : st})
				  
		context=self.get_context_data(**c)
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)

	def get_queryset(self):
		st=self._get_search_term()
		return SearchResult.objects.filter(keyword__contains=st).order_by('keyword')
						   

	def _get_search_term(self):
		try:
			return self.request.POST['search_term'].lower()
		except KeyError:
			try: return self.request.GET['search_term'].lower()
			except KeyError:
				return None
		
