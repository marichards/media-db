import re, logging
from django import forms
from defined_media.models import Organisms
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from defined_media.models import Contributor

log=logging.getLogger(__name__)

class SearchForm(forms.Form):
    search_term=forms.CharField()


class NewMediaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewMediaForm, self).__init__(*args, **kwargs)

        if len(args)>0:
            ''' Attach the original args (args[0]) if present so that
                we check them in is_valid(), using the variable fields
                we are going to add client-side using jQuery.
            '''
            self.orig_args=dict(args[0])

        self.organisms=Organisms.objects.all()
        genuss=sorted(list(set([o.genus.capitalize() for o in self.organisms]))) # set() to unique-ify
        self.fields['genus']=forms.ChoiceField(required=True, label='Genus', 
                                               choices=[(x,x) for x in genuss])

    species=forms.ChoiceField(required=True, label='Species', choices=())
    strain=forms.ChoiceField(required=True, label='Strain', choices=())

    media_name=forms.CharField(required=True, label='Media Name')
    is_defined=forms.CharField(label='Is defined?', widget=forms.CheckboxInput)
    is_minimal=forms.CharField(label='Is minimal?', widget=forms.CheckboxInput)

    pmid=forms.CharField(required=False, label='Pubmed ID')
    first_author=forms.CharField(label='First Author')
    journal=forms.CharField(label='Journal', max_length=255)
    year=forms.CharField(label='Year')
    title=forms.CharField(label='Title', max_length=255)
    link=forms.CharField(label='Link', max_length=255)


    comp1=forms.CharField(required=True, label='Compound')
    amount1=forms.FloatField(required=True, label='Amount (Mm)', min_value=0)

    growth_rate=forms.FloatField(min_value=0, required=True, label='Growth Rate')
    temperature=forms.FloatField(min_value=0, required=True, label='Temperature')
    ph=forms.FloatField(min_value=0, required=True, label='PH')

    uptake_comp1=forms.CharField(label='Compound', required=False)
    uptake_rate1=forms.FloatField(label='Rate (+/-)', required=False)


    def is_valid(self):
        log.debug('is_valid entered')
        valid=super(NewMediaForm, self).is_valid()
        if not hasattr(self, 'orig_args'):
            log.debug('no orig_args, returning %s' % valid)
            return valid
        # back-fill missing genus, species:
        for k,v in self.cleaned_data.items():
            log.debug('cleaned[%s]: %s' % (k, self.cleaned_data[k]))

        for f in ['genus', 'species', 'strain']:
            if f in self.errors:
                del self.errors[f]
                self.cleaned_data[f]=self.orig_args[f]

        self.cleaned_data.update(self.orig_args)

        '''
        # verify that we can find an organsism:
        try:
            org_data={'genus': self.cleaned_data['genus'][0], 
                      'species': self.cleaned_data['species'][0],
                      'strain': self.cleaned_data['strain'][0]}
            org=Organisms.objects.get(**org_data)
        except Organisms.DoesNotExist:
            log.debug('returning False: no org found for %s' % org_data)
            return False
        '''
        def is_missing(key):
            try: value_list=self.cleaned_data[key]
            except KeyError: 
                log.debug('is_missing(%s): no %s in data, returning True' % (key, key))
                return True

            if value_list==None: 
                log.debug('is_missing(%s): data[%s] is None' % (key, key))
                return True

            try: n=len(value_list[0].strip())
            except AttributeError, e: # if no .strip()
                n=-1
            except TypeError, e: # if len() breaks
                n=-2
            except IndexError, e: # if value[0] breaks
                n=-3
            
            log.debug('is_missing(%s): value_list=%s, n=%s' % (key, value_list, n))
            ret = n<=0
            return ret
                

        # check matching compounds and amounts (beyond the first):
        err_temp='<ul class="errorlist"><li>%s<ul class="errorlist"><li>This field is required.</li></ul></li></ul>'
        pairs={'comp':'amount',
               'amount':'comp',
               'uptake_comp':'uptake_rate',
               'uptake_rate':'uptake_comp'}
        for key1 in self.cleaned_data.keys():
            for k,v in pairs.items():
                if key1.startswith(k):
                    key2='%s%s' % (v,key1.split(k)[1])
                    missing1=is_missing(key1)
                    missing2=is_missing(key2)
                    log.debug('is_missing(%s): %s' % (key1, missing1))
                    log.debug('is_missing(%s): %s' % (key2, missing2))
                    if not missing1 and missing2: # don't do "missing1 != missing2" because then we'll get the error twice
                        self.errors[key2]=err_temp % key2
                        log.debug('is mismatched: %s and %s' % (key1, key2))
                    else:
                        log.debug('not mismatched: %s and %s' % (key1, key2))
                    break
        log.debug('is_valid: len(errors)=%d' % len(self.errors))
        return len(self.errors)==0
            
    def reformat_errors(self):
        '''
        self.errors is a dict() that packages each value as a <ul>...</ul>
        grrrrr...
        We strip away everything between the <ul ...>...</ul>
        '''
        errors={}
        pattern=r'<ul[^>]+><li>(.*)</li></ul>'
        rep=r'\1'
        for k,v in self.errors.items():
            errors[k]=re.sub(pattern, rep, str(v))
        self.my_errors=errors


'''
class CreateContributorForm(UserCreationForm):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()

    def __init__(self, *args, **kargs):
        super(CreateContributorForm, self).__init__(*args, **kargs)
        del self.fields['username']
        
        
    class Meta:
        model=Contributor
        fields=('email',)

class ChangeContributorForm(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(ChangeContributorForm,self).__init__(*args, **kargs)
        del self.fields['username']
        
        class Meta:
            model=Contributor

'''
