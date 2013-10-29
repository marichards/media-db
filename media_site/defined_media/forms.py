import re
from django import forms
from defined_media.models import Organisms
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from defined_media.models import Contributor


class SearchForm(forms.Form):
    search_term=forms.CharField()

class NewMediaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewMediaForm, self).__init__(*args, **kwargs)

        if len(args)>0:
            try:
                self.orig_args=dict(args[0])
#                print 'set self.orig_data: %s' % self.orig_args
            except Exception, e:
#                print 'NewMediaForm(): caught %s: %s' % (type(e),e)
                pass


        self.organisms=Organisms.objects.all()
        genuss=sorted(list(set([o.genus.capitalize() for o in self.organisms]))) # set to get unique
        self.fields['genus']=forms.ChoiceField(required=True, label='Genus', 
                                               choices=[(x,x) for x in genuss])

    species=forms.ChoiceField(required=True, label='Species', choices=())
    strain=forms.ChoiceField(required=True, label='Strain', choices=())

    pmid=forms.CharField(required=True, label='Pubmed ID')

    comp1=forms.CharField(required=True, label='Compound')
    amount1=forms.FloatField(required=True, label='Amount (Mm)', min_value=0)
#    units1=forms.ChoiceField(required=True, label='Units', 
#                            choices=(()))


    growthrate=forms.FloatField(min_value=0, required=True, label='Growth Rate')
    temperature=forms.FloatField(min_value=0, required=True, label='Temperature')
    ph=forms.FloatField(min_value=0, required=True, label='PH')

    uptake_comp1=forms.CharField(label='Compound', required=False)
    uptake_rate1=forms.FloatField(label='Rate (+/-)', required=False)


    def is_valid(self):
        err_temp='<ul class="errorlist"><li>%s<ul class="errorlist"><li>This field is required.</li></ul></li></ul>'
        valid=super(NewMediaForm, self).is_valid()
        if not hasattr(self, 'orig_args'):
#            print 'no orig_args, returning %s' % valid
            return valid
#        print 'is_valid: orig_args: %s' % self.orig_args

        # have to back-fill missing genus, species:
        for f in ['genus', 'species', 'strain']:
            if f in self.errors:
                del self.errors[f]
                self.cleaned_data[f]=self.orig_args[f]

        self.cleaned_data.update(self.orig_args)

        try:
            org_data={'genus': self.cleaned_data['genus'], 
                      'species': self.cleaned_data['species'],
                      'strain': self.cleaned_data['strain']}
            org=Organisms.objects.get(**org_data)
#            print 'NMF.is_valid(): found org %s' % org
                    
        except Exception, e:
            print 'NMF.is_valid(): caught %s: %s' % (type(e), e)
            return False

#        for k,v in self.cleaned_data.items():
#            print 'cleaned_data[%s]: %s' % (k,v)

        def is_missing(key):
            try:
                return len(self.cleaned_data[key].strip())==0
            except Exception, e:
                return True

        # check matching compounds and amounts (beyond the first):
        pairs={'comp':'amount',
               'amount':'comp',
               'uptake_comp':'uptake_rate',
               'uptake_rate':'uptake_comp'}
        for key in self.cleaned_data.keys():
#            print 'key is %s' % key
            for k,v in pairs.items():
#                print 'k,v are %s,%s' % (k,v)
                if key.startswith(k):
                    other_key='%s%s' % (v,key.split(k)[1])
#                    if other_key not in self.cleaned_data or not self.cleaned_data[other_key]:
                    if not is_missing(key) and is_missing(other_key):
#                        print 'self.errors[%s] set' % other_key
                        self.errors[other_key]=err_temp % other_key
                    break

            '''
            
            if key.startswith('comp'):
                amt_key='amount%s' % key.split('comp')[1]
                if amt_key not in self.cleaned_data or not self.cleaned_data[amt_key]:
                    self.errors[amt_key]=err_temp % amt_key
            elif key.startswith('amount'):
                comp_key='comp%s' % key.split('amount')[1]
                if comp_key not in self.cleaned_data or not self.cleaned_data[comp_key]:
                    self.errors[comp_key]=err_temp % comp_key
            elif key.startswith('uptake_comp'):
                rate_key='uptake_rate%s' % key.split('comp')[1]
                if rate_key not in self.cleaned_data or not self.cleaned_data[rate_key]:
                    self.errors[rate_key]=err_temp % rate_key
            elif key.startswith('uptake_rate'):
                comp_key='uptake_comp%s' % key.split('rate')[1]
                if comp_key not in self.cleaned_data or not self.cleaned_data[comp_key]:
                    self.errors[comp_key]=err_temp % comp_key
            '''

#        print 'errors: %s' % self.errors
        return len(self.errors)==0
            


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
