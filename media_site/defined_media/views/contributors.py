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
        for k,v in request.POST.items():
            log.debug('POST[%s]: %s' % (k, request.POST[k]))
        form=NewMediaForm(request.POST)
        form.orig_data=request.POST
        valid=form.is_valid()
#        print 'NewMediaView: form.is_valid(): %s' % valid
        form.reformat_errors()

        if not valid:
            log.debug('form not valid, aborting')
            for k,v in form.errors.items():
                log.debug('error: %s -> %s' % (k, form.errors[k]))
            return self.form_invalid(form)
        
        growth_data=self.get_growth_data(form)
        log.debug('growth_data is %s' % growth_data)
        if not growth_data:
            log.debug('failed, returning form.invalid')
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
            log.debug("No such organism: "+str(e))
            form.errors['Organism']="No such organism: "+str(e)
            return None
    
    def get_media_name(self, form):
        log.debug('get_media_name entered')
        try:
            m=MediaNames.objects.get(media_name=form.cleaned_data['media_name'][0])
            log.debug('got m: %s' % m)
            return m
        except MediaNames.DoesNotExist:
            log.debug('creating a new media_name')
            try:
                is_defined='Y' if 'is_defined' in self.request.POST else 'N'
                is_minimal='Y' if 'is_minimal' in self.request.POST else 'N'

                args={'media_name': form.cleaned_data['media_name'][0],
                      'is_defined': is_defined,
                      'is_minimal': is_minimal
                      }
                log.debug('args are %s' % args)
                m=MediaNames(**args)
                log.debug('m is %s' % m)
                try:
                    m.save()
                except Exception, e:
                    log.debug('caught e: %s' % e)
                    import traceback
                    traceback.print_exc()
                    raise e
                log.debug('saved m')
                log.debug('returning new media_name %s' % m)
                return m
            except Exception, e:
                log.debug("Unable to create MediaNames record (%s): " %(type(e),str(e)))
                form.errors['MediaNames']="Unable to create media name record: "+str(e)
                return None

    def get_growth_data(self, form):
        try:
            org=self.get_organism(form)
            log.debug('org is %s' % org)
            source=self.get_source(form)
            log.debug('source is %s' % source)
            media_name=self.get_media_name(form)
            log.debug('media_name is %r' % media_name)
            if not (org and source and media_name):
                log.debug('get_growth_data: cannot create sub-object(s), leaving')
                return None

            log.debug('about to create growth_data object')
            args={'strainid': org,
                  'medid': media_name,
                  'sourceid': source,
                  'growth_rate': form.cleaned_data['growth_rate'][0],
                  'growth_units': '1/h',
                  'ph': form.cleaned_data['ph'][0],
                  'temperature_c': form.cleaned_data['temperature'][0],
                  'additional_notes': '',
                  }
            log.debug('args are %s' % args)
            gd=GrowthData(**args)
            log.debug('gd is %s' % gd)
            gd.save()
            return gd
        except Exception, e:
            log.debug("Unable to create growth data record (%s): %s" % (type(e), str(e)))
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
                log.debug('Source args: %s' % args)
                src=Sources.objects.create(**args)
                return src
            except Exception, e:
                log.debug("Unable to create source record(%s): %s" % (type(e), str(e)))
                form.errors['Sources']="Unable to create source record: "+str(e)
                return None


                          
