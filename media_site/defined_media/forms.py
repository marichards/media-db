import re, logging
from django import forms
from defined_media.models import *
from form_helpers import ReformatsErrors, Gets1


'''
THIS FILE IS DEPRECATED AND OBSOLETE.  IT IS NO LONGER USED IN ANY WAY.
'''

#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from defined_media.models import Contributor

log=logging.getLogger(__name__)

class SearchForm(forms.Form):
    search_term=forms.CharField()


class OrganismForm(forms.ModelForm):
    class Meta:
        model=Organisms
        
class SourceForm(forms.ModelForm):
    class Meta:
        model=Sources
        widgets={'pubmed_id': forms.TextInput(attrs={})}

                


class NewCompoundMediaForm(forms.Form, ReformatsErrors, Gets1):
    ''' this is obsolete! '''
    ''' and really badly named! '''
    @classmethod                # why can't we just NewCompoundMediaForm(gd)?  Because we need to follow lists
    def from_growth_data(self, gd):
        return NewCompoundMediaForm(gd.as_dict())
            
    def __init__(self, *args, **kwargs):
        super(NewCompoundMediaForm, self).__init__(*args, **kwargs)

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

    approved=forms.BooleanField(label='Approved', required=False) # otherwise will choke if not checked
    growthid=forms.IntegerField(required=False, widget=forms.HiddenInput)
    contributor_id=forms.IntegerField(required=True, widget=forms.HiddenInput)

    species=forms.ChoiceField(required=True, label='Species', choices=())
    strain=forms.ChoiceField(required=True, label='Strain', choices=())

    new_genus=forms.CharField(label='New Genus', required=False)
    new_species=forms.CharField(label='New Species', required=False)
    new_strain=forms.CharField(label='New Strain', required=False)
    org_type_choices=[(t.typeid, t.organism_type) for t in TypesOfOrganisms.objects.all()]
    new_org_type=forms.ChoiceField(label='New Type', choices=org_type_choices, required=False)

    media_name=forms.CharField(required=True, label='Media Name',
                               widget=forms.TextInput(attrs={'size': 75}))
    is_defined=forms.CharField(label='Is defined?', widget=forms.CheckboxInput)
    is_minimal=forms.CharField(label='Is minimal?', widget=forms.CheckboxInput)

    pmid=forms.IntegerField(required=False, label='Pubmed ID',
                            widget=forms.TextInput(attrs={'size': 75}))
    first_author=forms.CharField(label='First Author', max_length=255,
                                 widget=forms.TextInput(attrs={'size': 75}))
    journal=forms.CharField(label='Journal', max_length=255,
                            widget=forms.TextInput(attrs={'size': 75}))
    year=forms.IntegerField(label='Year')
    title=forms.CharField(label='Title', max_length=255,
                          widget=forms.TextInput(attrs={'size': 75}))
    link=forms.CharField(label='Link', max_length=255,
                         widget=forms.TextInput(attrs={'size': 75}))


    comp1=forms.CharField(required=True, label='Compound')
    amount1=forms.FloatField(required=True, label='Amount (Mm)', min_value=0)

    growth_rate=forms.FloatField(min_value=0, required=False, label='Growth Rate',
                                 widget=forms.TextInput(attrs={'size':8}))
    temperature=forms.FloatField(min_value=0, required=False, label='Temperature',
                                 widget=forms.TextInput(attrs={'size':8}))
    ph=forms.FloatField(min_value=0, required=False, label='ph',
                                 widget=forms.TextInput(attrs={'size':8}))

    uptake_comp1=forms.CharField(label='Compound', required=False)
    uptake_rate1=forms.FloatField(label='Rate (+/-)', required=False)
    unit_choices=[(u,u) for u in set([u.units for u in SecretionUptake.objects.all()])]
    uptake_unit1=forms.ChoiceField(label='Units', required=False, choices=unit_choices)
    type_choices=[(u.rateid,u.rate_type) for u in SecretionUptakeKey.objects.all()]
    uptake_type1=forms.ChoiceField(label='Type', required=False, choices=type_choices)
    additional_notes=forms.CharField(required=False, 
                                     widget=forms.Textarea(attrs={'rows':3, 'cols': 40}))

    def is_valid(self):
        '''
        This method does several things (redflag!), besides call its super():
        - removes false errors in the organism form that exist because initially 
          they're blank (fix: could safely remove 'required' from form spec)
        - updates self.cleaned_data with addition args passed to the form (really necessary?)
        - checks for existence of amounts associated with compounds; can't do this
          in super because of dynamically added (by client) form fields.
        - should also call get_organism_name, but currently doesn't.  That method
          has the logic to check validity of organism name correctly.

        What the method should do:
        - Attempt to guarantee, as far as possible, that the new growth data
          record can be successfully saved.  That includes:
        - Check for completeness: all compounds have amounts, all fields of source are specified, etc;
        - Check for the existence of all named compounds;
        - Check that organism name is valid;
        - Check that floating point values are actually floating points;
        '''
        valid=super(NewCompoundMediaForm, self).is_valid()
        if not hasattr(self, 'orig_args'):
            return valid

        # back-fill missing genus, species:
        # have to do this because the form's select values are inter-dependent,
        # and start off as being empty.  This breaks the 'required' bit.
        for f in ['genus', 'species', 'strain']:
            if f in self.errors and f in self.orig_args:
                del self.errors[f]
                self.cleaned_data[f]=self.orig_args[f]

        self.cleaned_data.update(self.orig_args)
        
        # check compounds and amounts:
        err_temp='<ul class="errorlist"><li>%s: This field is required.</li></ul>'
        for key in [k for k in self.cleaned_data.keys() if k.startswith('comp')]:
            n=key.split('comp')[1]
            try:
                comp_name=self.cleaned_data.get(key)[0]
                if comp_name==None:
                    continue    # don't need to check for comp1 because it's required by form
                comp=Compounds.objects.with_name(comp_name)

                akey='amount'+n
                amount=self.cleaned_data.get(akey)

            except KeyError as ke:
                if akey in str(ke): # str(ke) has quotes
                    self.errors[akey]=err_temp % akey
                else:
                    raise ke
            except Compounds.DoesNotExist:
                self.errors[key]='Compound %s: Unknown compound "%s"' % (n,comp_name)
                continue

               
        # check completeness of all four uptake fields:
        uckeys=[k for k in self.cleaned_data.keys() if k.startswith('uptake_comp')]
        part2s=['rate', 'unit', 'type']
        for uckey in uckeys:
            # ignore this "row" if no compound given
            try: 
                comp_name=self.cleaned_data.get(uckey)[0]
                if not comp_name or len(comp_name)==0: 
                    continue
            except: 
                continue

            n=uckey.split('uptake_comp')[1]

            # look for valid compound:
            try:
                comp=Compounds.objects.with_name(comp_name)
            except Compounds.DoesNotExist:
                self.errors['uptake%s' % n]='Uptake %s: Unknown compound "%s"' % (n, comp_name)
                continue

            missing=[]
            for part2 in part2s:
                key='uptake_%s%s' % (part2, n)
                try:
                    try: val=self.cleaned_data.get(key)[0] # sometimes it's a list, sometimes it's not
                    except TypeError: val=self.cleaned_data.get(key)
                    if val==None: raise ValueError(val)
                except Exception as e:
                    missing.append(part2)
            if len(missing)>0:
                self.errors['uptake%s' % n]='Uptake %s: These fields are required: %s' % (n, ', '.join(missing))

        return len(self.errors)==0


    def get_organism_name(self):
        ''' return a tuple of genus, species, stain, and new_org (bool). 
        Also writes to self.errors if new org fields incompletely 
        specify a new org.
        '''
        species=None
        strain=None
        genus=self.get1('new_genus')
        new_org=False

        if genus:               # new genus
            species=self.get1('new_species')
            if not species:
                self.errors['new_species']='New genus requires new species'

            strain=self.get1('new_strain')
            if not strain:
                self.errors['new_strain']='New genus requires new strain'

            if species and strain:
                new_org=True
        else:
            genus=self.get1('genus')

        if not species:         # no new genus
            species=self.get1('new_species')
            if species:         # new species
                strain=self.get1('new_strain')
                if not strain or new_org: # new_org from new_genus
                    self.errors['new_strain']='New species requires new strain'
                else:
                    new_org=True
            else:
                species=self.get1('species')

        if not strain:
            strain=self.get1('new_strain')
            if strain:
                new_org=True
            else:
                strain=self.get1('strain')

        return genus, species, strain, new_org

