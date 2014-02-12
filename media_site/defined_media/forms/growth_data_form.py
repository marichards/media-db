import django.forms as forms
from defined_media.models import GrowthData, Organisms, MediaNames, Sources

class GrowthDataForm(forms.Form):
    ''' Form holding create/edit info for GrowthData
    Template has:
    Dynamic, cascading selects for organism (genus, species, strain)
    Auto-complete fields for MediaName.media_name, Source.first_author
    Regular fields for growth_rate, temperature_c, ph, additional_notes
    Dynamic-length list for secretion uptake
    '''
    class Meta:
        model=GrowthData


    # regular fields (override so we can set the widget size)
    growth_rate=forms.FloatField(min_value=0, required=False, label='Growth Rate',
                                 widget=forms.TextInput(attrs={'size':8}))
    temperature_c=forms.FloatField(min_value=0, required=False, label='Temperature',
                                 widget=forms.TextInput(attrs={'size':8}))
    ph=forms.FloatField(min_value=0, required=False, label='ph',
                                 widget=forms.TextInput(attrs={'size':8}))

    # override so we can set the widget
    contributor=forms.CharField(widget=forms.HiddenInput())
    additional_notes=forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40}),
                                     required=False,
                                     )

    strainid=forms.ModelChoiceField(queryset=Organisms.objects.all())
    sourceid=forms.ModelChoiceField(queryset=Sources.objects.all())
    medid=forms.ModelChoiceField(queryset=MediaNames.objects.all())

    @classmethod
    def from_growth_data(self, gd):
        return GrowthDataForm(gd.as_dict())



    def is_valid(self):
        valid=super(GrowthDataForm,self).is_valid()
        # check other stuff
        return valid

    
