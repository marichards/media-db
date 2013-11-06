import logging
log=logging.getLogger(__name__)

from defined_media.forms import NewMediaForm
from defined_media.models import *
from django.views.generic.edit import FormView
#from django.core.urlresolvers import reverse

class NewMediaView(FormView):
    template_name='defined_media/newmedia_form.html'
    form_class=NewMediaForm
#    success_url=reverse('new_media_form')
    success_url='/defined_media/newmedia'

    def post(self, request, *args, **kwargs):
        form=NewMediaForm(request.POST)
        form.orig_data=request.POST
        valid=form.is_valid()
        form.reformat_errors()

        if not valid:
            return self.form_invalid(form)
        
        growth_data=self.get_growth_data(form)
        if not growth_data:
            # set some errors
            return self.form_invalid(form)

        return self.form_valid(form)

        # return an un-rendered TemplateResponse object:
#        return super(NewMediaView, self).post(request, *args, **kwargs)


    def get_organism(self, form):
        try:
            return Organisms.objects.get(genus=form.cleaned_data['genus'][0],
                                        species=form.cleaned_data['species'][0],
                                        strain=form.cleaned_data['strain'][0])
        except Organisms.DoesNotExist, e:
            form.errors['Organism']="No such organism: "+str(e)
            return None
    
    def get_media_name(self, form):
        try:
            m=MediaNames.objects.get(media_name=form.cleaned_data['media_name'][0])
            return m
        except MediaNames.DoesNotExist:
            try:
                is_defined='Y' if 'is_defined' in self.request.POST else 'N'
                is_minimal='Y' if 'is_minimal' in self.request.POST else 'N'

                args={'media_name': form.cleaned_data['media_name'][0],
                      'is_defined': is_defined,
                      'is_minimal': is_minimal
                      }
                m=MediaNames(**args)
                try:
                    m.save()
                except Exception, e:
                    import traceback
                    traceback.print_exc()
                    raise e
                return m
            except Exception, e:
                form.errors['MediaNames']="Unable to create media name record: "+str(e)
                return None

    def get_growth_data(self, form):
        try:
            org=self.get_organism(form)
            source=self.get_source(form)
            media_name=self.get_media_name(form)
            if not (org and source and media_name):
                return None


            args={'strainid': org,
                  'medid': media_name,
                  'sourceid': source,
                  'growth_rate': form.cleaned_data['growth_rate'][0],
                  'growth_units': '1/h',
                  'ph': form.cleaned_data['ph'][0],
                  'temperature_c': form.cleaned_data['temperature'][0],
                  'additional_notes': '',
                  }
            gd=GrowthData(**args)
            gd.save()
            return gd
        except Exception, e:
            form.errors['GrowthData']="Unable to create growth data record: "+str(e)
            return None

    def get_source(self, form):
        title=form.cleaned_data['title'][0]
        try:
            return Sources.objects.get(title=title)
        except Sources.DoesNotExist:
            try:
                args={'title': form.cleaned_data['title'][0],
                      'journal': form.cleaned_data['journal'][0],
                      'first_author': form.cleaned_data['first_author'][0],
                      'year': int(form.cleaned_data['year'][0]),
                      'link': form.cleaned_data['link'][0]}
                src=Sources.objects.create(**args)
                return src
            except Exception, e:
                form.errors['Sources']="Unable to create source record: "+str(e)
                return None


                          
    '''
    def get_uptakes(self, form):
        for key in [k for k in form.cleaned_data.keys() if k.startswith('uptake_comp')]:
            try:
                n=key.split('uptake_comp')[1]
                uptake_comp=form.cleaned_data[key][0]
                uptake_rate=form.cleaned_data['uptake_rate'+n][0]
    '''
