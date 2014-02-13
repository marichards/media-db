from django import forms
from defined_media.models import Organisms, Sources

class SearchForm(forms.Form):
    search_term=forms.CharField()


class OrganismForm(forms.ModelForm):
    class Meta:
        model=Organisms
        
class SourceForm(forms.ModelForm):
    class Meta:
        model=Sources
        widgets={'pubmed_id': forms.TextInput(attrs={})}
