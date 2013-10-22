from django import forms
from defined_media.models import Organisms

class SearchForm(forms.Form):
    search_term=forms.CharField()

class MediaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MediaForm, self).__init__(self, *args, **kwargs)
        self.organisms=Organisms.objects.all()
        genuss=set([o.genus for o in self.organisms]) # set to get unique
        self.fields['genus']=forms.ChoiceField(required=True, label='Genus', 
                                               choices=[(x,x) for x in genuss])
        # more to come...
