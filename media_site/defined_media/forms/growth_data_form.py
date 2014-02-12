import django.forms as forms
from defined_media.models import GrowthData, Organisms, MediaNames, Sources, SecretionUptake, SecretionUptakeKey, Compounds
import logging, re
log=logging.getLogger(__name__)

class GrowthDataForm(forms.Form):
    ''' Form holding create/edit info for GrowthData
    Template has:
    Dynamic, cascading selects for organism (genus, species, strain)
    Auto-complete fields for MediaName.media_name, Source.first_author
    Regular fields for growth_rate, temperature_c, ph, additional_notes
    Dynamic-length list for secretion uptake
    '''

    @classmethod
    def from_growth_data(self, gd):
        return GrowthDataForm(gd.as_dict())

    # regular fields (override so we can set the widget size)
    growth_rate=forms.FloatField(min_value=0, required=False, label='Growth Rate',
                                 widget=forms.TextInput(attrs={'size':8}))
    temperature_c=forms.FloatField(min_value=0, required=False, label='Temperature',
                                 widget=forms.TextInput(attrs={'size':8}))
    ph=forms.FloatField(min_value=0, required=False, label='ph',
                                 widget=forms.TextInput(attrs={'size':8}))

    # override so we can set the widget
    contributor=forms.CharField(widget=forms.HiddenInput())
    growthid=forms.CharField(widget=forms.HiddenInput())
    additional_notes=forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40}),
                                     required=False,
                                     )

    strainid=forms.ModelChoiceField(queryset=Organisms.objects.all())
    sourceid=forms.ModelChoiceField(queryset=Sources.objects.all())
    medid=forms.ModelChoiceField(queryset=MediaNames.objects.all())


    def __init__(self, *args, **kwargs):
        super(GrowthDataForm, self).__init__(*args, **kwargs)
        self.uptakes_list=[]
        
        # add form sec-uptake fields if args[0] is a GrowthData object
        try:
            try:
                gd=args[0]
                d=gd.as_dict()
                self.gd=gd
            except AttributeError:
                d=args[0]
            
            n=1
            for k,v in d.items():
                if k.startswith('uptake_comp'):
                    # keys are uptake_comp, uptake_rate, uptake_unit, uptake_type
                    hashlette={'comp':v}

                    for suffix in 'rate unit type'.split(' '):
                        field_key=re.sub('comp', suffix, k)
                        try: field_val=d[field_key]
                        except KeyError: field_val=''
                        hashlette[suffix]=field_val
                    log.debug('about to add hashlette: %s' % hashlette)
                    self._add_uptake_field(n, hashlette)
                    n+=1

        except (IndexError) as e:  # nevermind, maybe args[0] wasn't a GrowthData object or something
            log.debug('GrowthDataForm.__init__(): ignoring %s: %s' % (type(e), e))
            log.exception(e)
            
        # if nothing happened, we need to at least create the first uptake set:
        if 'uptake_comp1' not in self.fields:
            log.debug('adding first empty uptake row')
            self._add_uptake_field(1, {'comp': '', 
                                        'rate': '',
                                        'unit' : '',
                                        'type' : ''})

    def _add_uptake_field(self, n, hashlette):
        ''' add a field for compound, rate, unit, and uptake (from hashlette) '''
        self.uptakes_list.append(hashlette)
        self.fields['uptake_comp%d' % n]=forms.CharField(label='Compound %d' % n, required=False, 
                                                         initial=hashlette['comp'])
        self.fields['uptake_rate%d' % n]=forms.FloatField(label='Rate', 
                                                          required=False, 
                                                          initial=hashlette['rate'])
        initial=hashlette['unit']
        if initial is None or len(initial)==0:
            initial=0
        self.fields['uptake_unit%d' % n]=forms.ModelChoiceField(label='Units', 
                                                           required=False, 
                                                           initial=initial,
                                                           queryset=SecretionUptake.objects.all(),
                                                           )

        initial=hashlette['type']
        if initial is None or len(initial)==0:
            initial=0
        self.fields['uptake_type%d' % n]=forms.ModelChoiceField(label='Type', 
                                                                required=False, 
                                                                initial=initial,
                                                                queryset=SecretionUptakeKey.objects.all(),
                                                                )



    def is_valid(self):
        log.debug('got here: gdf.is_valid')
        valid=super(GrowthDataForm,self).is_valid()
        log.debug('gdf.valid=%s' % valid)
        cd=self.cleaned_data

        # check uptakes:
        upkeys=[k for k in self.fields.keys() if k.startswith('uptake_comp')]
        log.debug('gdf.is_valid: upkeys: %s' % upkeys)
        for key in upkeys:
            try:
                comp_name=cd.get(key)
                if comp_name is None: continue
                if len(comp_name)==0: continue
                log.debug('is_valid: looking for compound "%s"' % comp_name)
                compound=Compounds.objects.with_name(comp_name)
                
                # check that rate is present, and can be converted to float:
                # (conversion check might not be necessary)
                rate_key=re.sub(r'comp', 'rate', key)
                rate=cd.get(rate_key)
                if rate is None:
                    self.errors[rate_key]='rate required for compound %s' % comp_name
                    valid=False
                else:
                    try:
                        r=float(rate)
                    except (ValueError, TypeError) as e:
                        self.errors[rate_key]='%s: must be a floating point number'
                        valid=False

            except Compounds.DoesNotExist as e:
                log.debug('caught bad compound "%s"' % comp_name)
                self.errors[key]='%s: no such compound' % comp_name
                valid=False

        return valid

    
