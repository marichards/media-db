import re, logging
from django import forms
from defined_media.models import *
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
                we can check them in is_valid(), using the variable fields
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
    unit_choices=[(u,u) for u in set([u.units for u in SecretionUptake.objects.all()])]
    uptake_unit1=forms.ChoiceField(label='Units', required=False, choices=unit_choices)
    type_choices=[(u.rateid,u.rate_type) for u in SecretionUptakeKey.objects.all()]
    uptake_type1=forms.ChoiceField(label='Type', required=False, choices=type_choices)

    def is_valid(self):
        valid=super(NewMediaForm, self).is_valid()
        if not hasattr(self, 'orig_args'):
            return valid

        # back-fill missing genus, species:
        for f in ['genus', 'species', 'strain']:
            if f in self.errors:
                del self.errors[f]
                self.cleaned_data[f]=self.orig_args[f]

        self.cleaned_data.update(self.orig_args)

        def is_missing(key):
            try: value_list=self.cleaned_data[key]
            except KeyError: 
                return True

            if value_list==None: 
                return True

            try: n=len(value_list[0].strip())
            except AttributeError, e: # if no .strip()
                n=-1
            except TypeError, e: # if len() breaks
                n=-2
            except IndexError, e: # if value[0] breaks
                n=-3
            
            ret = n<=0
            return ret
                

        # check matching compounds and amounts (beyond the first):
        err_temp='<ul class="errorlist"><li>%s: This field is required.</li></ul>'
        pairs={'comp':'amount',
               'amount':'comp',
#               'uptake_compound':'uptake_rate',
#               'uptake_rate':'uptake_compound',
               }
        for key1 in self.cleaned_data.keys():
            for k,v in pairs.items():
                if key1.startswith(k):
                    key2='%s%s' % (v,key1.split(k)[1])
                    missing1=is_missing(key1)
                    missing2=is_missing(key2)
                    if not missing1 and missing2: # don't do "missing1 != missing2" because then we'll get the error twice
                        self.errors[key2]=err_temp % key2
                    break
               
        # check completeness of all four uptake fields:
        uckeys=[k for k in self.cleaned_data.keys() if k.startswith('uptake_comp')]
        part2s=['rate', 'unit', 'type']
        for uckey in uckeys:
            try: 
                comp_name=self.cleaned_data[uckey][0]
                if not comp_name or len(comp_name)==0: continue
            except: 
                continue

            n=uckey.split('uptake_comp')[1]
            missing=[]
            for part2 in part2s:
                key='uptake_%s%s' % (part2, n)
                try:
                    val=self.cleaned_data[key][0]
                    if val==None: raise ValueError(val)
                except:
                    missing.append(part2)
            if len(missing)>0:
                self.errors['uptake%s' % n]='Uptake %s: These fields are required: %s' % (n, ', '.join(missing))

        return len(self.errors)==0
            
    def reformat_errors(self):
        '''
        self.errors is a dict() that packages each value as a <ul>...</ul>
        grrrrr...
        We strip away everything between the <ul ...>...</ul>
        '''
        log.debug('reformatting %d errors' % len(self.errors))
        errors={}
        pattern=r'<ul[^>]+><li>(.*)</li></ul>'
        rep=r'\1'
        for k,v in self.errors.items():
            errors[k]=re.sub(pattern, rep, str(v))
            log.debug('reformat: %s' % errors[k])
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
