from defined_media.forms import NewMediaForm
from django.views.generic.edit import FormView

class NewMediaView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=NewMediaForm
    
    def post(self, request, *args, **kwargs):
        form=NewMediaForm(request.POST)
        form.orig_data=request.POST
        print 'form.is_valid(): %s' % form.is_valid()
        if not form.is_valid():
            print 'form errors:'
            for k,v in form.errors.items():
                print 'error: %s -> %s' % (k,v)

        # return an un-rendered TemplateResponse object:
        return super(NewMediaView, self).post(request, *args, **kwargs)

