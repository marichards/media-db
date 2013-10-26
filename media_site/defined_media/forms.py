from django import forms
from defined_media.models import Organisms
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from defined_media.models import Contributor


class SearchForm(forms.Form):
    search_term=forms.CharField()


class NewMediaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewMediaForm, self).__init__(*args, **kwargs)

        self.organisms=Organisms.objects.all()
        genuss=sorted(list(set([o.genus.capitalize() for o in self.organisms]))) # set to get unique
        self.fields['genus']=forms.ChoiceField(required=True, label='Genus', 
                                               choices=[(x,x) for x in genuss])

    species=forms.ChoiceField(required=True, label='Species', choices=())
    strain=forms.ChoiceField(required=True, label='Strain', choices=())

    pmid=forms.CharField(required=True, label='Pubmed ID')

    comp1=forms.CharField(required=True, label='Compound')
    amount1=forms.CharField(required=True, label='Amount (Mm)')
#    units1=forms.ChoiceField(required=True, label='Units', 
#                            choices=(()))

        # more to come...

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
