from defined_media.forms import NewMediaForm
from django.views.generic.edit import FormView

class NewMediaView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=NewMediaForm
    
    def post(self, request, *args, **kwargs):
        form=NewMediaForm(request.POST)
        form.orig_data=request.POST
        valid=form.is_valid()
        form.reformat_errors()
        print 'form.is_valid(): %s' % valid
        if not valid:
            return self.form_invalid(form)
        
        return self.form_valid(form)

        # return an un-rendered TemplateResponse object:
#        return super(NewMediaView, self).post(request, *args, **kwargs)

