import re
from django import forms
from defined_media.models import Organisms
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from defined_media.models import Contributor


class SearchForm(forms.Form):
    search_term=forms.CharField()


def fix_errors(fn):
    def fixed(self):
        valid=fn(self)
        self.reformat_errors()
        return valid
    return fixed


class NewMediaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewMediaForm, self).__init__(*args, **kwargs)

        if len(args)>0:
            ''' Attach the original args (args[0]) if present so that
                we check them in is_valid(), using the variable fields
                we are going to add client-side using jQuery.
            '''
            try:
                self.orig_args=dict(args[0])
#                print 'set self.orig_data: %s' % self.orig_args
            except Exception, e:
#                print 'NewMediaForm(): caught %s: %s' % (type(e),e)
                pass


        self.organisms=Organisms.objects.all()
        genuss=sorted(list(set([o.genus.capitalize() for o in self.organisms]))) # set() to unique-ify
        self.fields['genus']=forms.ChoiceField(required=True, label='Genus', 
                                               choices=[(x,x) for x in genuss])

    species=forms.ChoiceField(required=True, label='Species', choices=())
    strain=forms.ChoiceField(required=True, label='Strain', choices=())

    media_name=forms.CharField(required=True, label='Media Name')
    is_defined=forms.CharField(label='Is defined?', widget=forms.CheckboxInput)
    is_minimal=forms.CharField(label='Is minimal?', widget=forms.CheckboxInput)
#    is_defined=forms.CharField(label='Is defined?', required=False, max_length=1, initial='Y')
#    is_minimal=forms.CharField(label='Is minimal?', required=False, max_length=1, initial='N')

    pmid=forms.CharField(required=False, label='Pubmed ID')
    first_author=forms.CharField(label='First Author')
    journal=forms.CharField(label='Journal', max_length=255)
    year=forms.CharField(label='Year')
    title=forms.CharField(label='Title', max_length=255)
    link=forms.CharField(label='Link', max_length=255)


    comp1=forms.CharField(required=True, label='Compound')
    amount1=forms.FloatField(required=True, label='Amount (Mm)', min_value=0)
#    units1=forms.ChoiceField(required=True, label='Units', 
#                            choices=(()))


    growth_rate=forms.FloatField(min_value=0, required=True, label='Growth Rate')
    temperature=forms.FloatField(min_value=0, required=True, label='Temperature')
    ph=forms.FloatField(min_value=0, required=True, label='PH')

    uptake_comp1=forms.CharField(label='Compound', required=False)
    uptake_rate1=forms.FloatField(label='Rate (+/-)', required=False)


#    @fix_errors
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

        # verify that we can find an organsism:
        try:
            org_data={'genus': self.cleaned_data['genus'][0], 
                      'species': self.cleaned_data['species'][0],
                      'strain': self.cleaned_data['strain'][0]}
            org=Organisms.objects.get(**org_data)
        except Exception, e:
            return False

        def is_missing(key):
            try:    return len(self.cleaned_data[key].strip())==0
            except: return True
                

        # check matching compounds and amounts (beyond the first):
        err_temp='<ul class="errorlist"><li>%s<ul class="errorlist"><li>This field is required.</li></ul></li></ul>'
        pairs={'comp':'amount',
               'amount':'comp',
               'uptake_comp':'uptake_rate',
               'uptake_rate':'uptake_comp'}
        for key in self.cleaned_data.keys():
            for k,v in pairs.items():
                if key.startswith(k):
                    other_key='%s%s' % (v,key.split(k)[1])
                    if not is_missing(key) and is_missing(other_key):
                        self.errors[other_key]=err_temp % other_key
                    break

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
