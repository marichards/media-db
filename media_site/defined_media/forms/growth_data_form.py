import django.forms as forms
from defined_media.models import GrowthData, Organisms

class GrowthDataForm(forms.ModelForm):
    ''' Form holding create/edit info for GrowthData
    Template has:
    Dynamic, cascading selects for organism (genus, species, strain)
    Auto-complete fields for MediaName.media_name, Source.first_author
    Regular fields for growth_rate, temperature_c, ph, additional_notes
    Dynamic-length list for secretion uptake
    '''
    class Meta:
        model=GrowthData

    def __init__(self, **kwargs):
        super(GrowthDataForm, self).__init__(**kwargs)
        self.organisms=Organisms.objects.all()
        genuss=sorted(list(set([o.genus.capitalize() for o in self.organisms]))) # set() to unique-ify
        self.fields['genus']=forms.ChoiceField(required=True, label='Genus', 
                                               choices=[(x,x) for x in genuss])

    # regular fields
    growth_rate=forms.FloatField(min_value=0, required=False, label='Growth Rate',
                                 widget=forms.TextInput(attrs={'size':8}))
    temperature_c=forms.FloatField(min_value=0, required=False, label='Temperature',
                                 widget=forms.TextInput(attrs={'size':8}))
    ph=forms.FloatField(min_value=0, required=False, label='ph',
                                 widget=forms.TextInput(attrs={'size':8}))

    # other organism fields
    species=forms.ChoiceField(required=True, label='Species', choices=())
    strain=forms.ChoiceField(required=True, label='Strain', choices=())

    media_name=forms.CharField(required=True, label='Media Name',
                               widget=forms.TextInput(attrs={'size': 75}))
    sourceid=forms.CharField(label='Source', max_length=255,
                             widget=forms.TextInput(attrs={'size': 75}))


    def is_valid(self):
        valid=super(GrowthDataForms.self).is_valid()
        # check other stuff
        return valid
