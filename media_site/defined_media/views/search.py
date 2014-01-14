from defined_media.models import SearchResult
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

		c={'form':form}
		st=self._get_search_term()
		if st:
                    classnames=[]
                    results={}
                    self.object_list=self.get_queryset()
                    for obj in self.object_list:
                        classname=obj.classname
                        if classname not in results:
                            classnames.append(classname)
                            results[classname]=[]
                        results[classname].append(obj)

                    c.update({'search_term' : st,
                              'n_results': len(self.object_list),
                              'classnames': classnames,
                              'results': results,
                              'object_list': self.object_list})
				  
                context=self.get_context_data(**c)
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)

	def get_queryset(self):
		st=self._get_search_term()
                all=list(SearchResult.objects.filter(keyword__contains=st))
                final={}
                for sr in all:
                        key='%s_%s' %(sr.classname, sr.obj_id)
                        final[key]=sr
                return sorted(final.values(), key=lambda sr: sr.keyword)
						   

	def _get_search_term(self):
		try:
			return self.request.POST['search_term'].lower()
		except KeyError:
			try: return self.request.GET['search_term'].lower()
			except KeyError:
				return None
		
