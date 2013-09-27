# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import re
from lazy import lazy

from django.core.urlresolvers import reverse

class Biomass(models.Model):
    biomassid = models.IntegerField(primary_key=True, db_column='biomassID') # Field name made lowercase.
    genus = models.CharField(max_length=255L, db_column='Genus') # Field name made lowercase.
    species = models.CharField(max_length=255L, db_column='Species') # Field name made lowercase.
    sourceid = models.ForeignKey('Sources', null=True, db_column='sourceID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'biomass'
        verbose_name_plural = 'biomass compositions'
    	#order_with_respect_to = 'genus'
    #Return the organism for the biomass
    def __unicode__(self):
        return '%s %s' %(self.genus.capitalize(),self.species.lower())

    #Define searchable terms
    def keywords(self):
	return [self.genus, self.species]

class BiomassCompounds(models.Model):
    biocompid = models.IntegerField(primary_key=True, db_column='biocompID') # Field name made lowercase.
    biomassid = models.ForeignKey(Biomass, db_column='biomassID') # Field name made lowercase.
    compid = models.ForeignKey('Compounds', db_column='compID') # Field name made lowercase.
    coefficient = models.FloatField(null=True, db_column='Coefficient', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'biomass_compounds'

class CompoundExceptions(models.Model):
    pk = models.IntegerField(primary_key=True)
    compid = models.ForeignKey('Compounds', db_column='compID') # Field name made lowercase.
    keggorgid = models.CharField(max_length=12L, db_column='keggOrgID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'compound_exceptions'

class CompoundReplacements(models.Model):
    pk = models.IntegerField(primary_key=True)
    compid = models.ForeignKey('Compounds', db_column='compID') # Field name made lowercase.
    biggid = models.CharField(max_length=12L, db_column='biggID') # Field name made lowercase.
    keggorgid = models.CharField(max_length=12L, db_column='keggOrgID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'compound_replacements'

class Compounds(models.Model):
    compid = models.IntegerField(primary_key=True, db_column='compID') # Field name made lowercase.
    kegg_id = models.CharField(max_length=255L, unique=True, db_column='KEGG_ID', blank=True) # Field name made lowercase.
    bigg_id = models.CharField(max_length=255L, db_column='BiGG_ID', blank=True) # Field name made lowercase.
    user_identifier = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'compounds'
	verbose_name_plural = 'compounds'
    #Return the first compound name for each thing
    def __unicode__(self):
#	return '%s' %self.compid
        return self.keywords()[0]


    def keywords(self):
        try:
            return self._keywords
        except AttributeError:
            self._keywords=[x.name for x in self.namesofcompounds_set.all()]
            return self._keywords

#    	return self.namesofcompounds_set.all() # matt's version

    def names(self):
        return ', '.join(self.keywords())

    def media_names(self):
        mcs=MediaCompounds.objects.filter(compid=self.compid)
        mednames=list(set([x.medid for x in mcs]))
        return sorted(mednames, key=lambda mc: mc.media_name)

#    @property
    def name0(self):
        return self.keywords()[0]

class Contributors(models.Model):
    contributorid = models.IntegerField(primary_key=True, db_column='contributorID') # Field name made lowercase.
    last_name = models.CharField(max_length=255L, unique=True, db_column='Last_Name', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'contributors'
        verbose_name_plural = 'contributors'
    def __unicode__(self):
        return '%s' %self.last_name.capitalize()

class GrowthData(models.Model):
    growthid = models.IntegerField(primary_key=True, db_column='growthID') # Field name made lowercase.
    strainid = models.ForeignKey('Organisms', db_column='strainID') # Field name made lowercase.
    medid = models.ForeignKey('MediaNames', db_column='medID') # Field name made lowercase.
    sourceid = models.ForeignKey('Sources', db_column='sourceID') # Field name made lowercase.
    growth_rate = models.FloatField(null=True, db_column='Growth_Rate', blank=True) # Field name made lowercase.
    growth_units = models.CharField(max_length=45L, db_column='Growth_Units', blank=True) # Field name made lowercase.
    ph = models.FloatField(null=True, db_column='pH', blank=True) # Field name made lowercase.
    temperature_c = models.FloatField(null=True, db_column='Temperature_C', blank=True) # Field name made lowercase.
    measureid = models.ForeignKey('Measurements', null=True, db_column='measureID', blank=True) # Field name made lowercase.
    additional_notes = models.CharField(max_length=255L, db_column='Additional_Notes', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'growth_data'
	verbose_name_plural = 'growth data'
    #Method: Python calls Growth Object and Returns the ID instead of just "GrowthData Object" 
    def __unicode__(self):
        return '%s on %s' %(self.strainid,self.medid)   

class Measurements(models.Model):
    measureid = models.IntegerField(primary_key=True, db_column='measureID') # Field name made lowercase.
    measurement_technique = models.CharField(max_length=255L, unique=True, db_column='Measurement_Technique', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'measurements'
    def __unicode__(self):
        return '%s' %self.measurement_technique

class MediaCompounds(models.Model):
    medcompid = models.IntegerField(primary_key=True, db_column='medcompID') # Field name made lowercase.
    medid = models.ForeignKey('MediaNames', db_column='medID') # Field name made lowercase.
    compid = models.ForeignKey(Compounds, db_column='compID') # Field name made lowercase.
    amount_mm = models.FloatField(null=True, db_column='Amount_mM', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'media_compounds'

    def __unicode__(self):
        return self.compid.__unicode__()


class MediaNames(models.Model):
    medid = models.IntegerField(primary_key=True, db_column='medID') # Field name made lowercase.
    media_name = models.CharField(max_length=255L, db_column='Media_name', blank=True) # Field name made lowercase.
    is_defined = models.CharField(max_length=1L, db_column='Is_defined', blank=True) # Field name made lowercase.
    is_minimal = models.CharField(max_length=1L, db_column='Is_minimal', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'media_names'
	verbose_name_plural = 'media names'
    def __unicode__(self):
        #Define a method that grabs everything in a given medium
        #compounds_list = MediaCompounds.objects.filter(medid=self.medid)
        #compounds_str = '%s contains: ' %self.media_name
	#for item in compounds_list:
        #    compounds_str += '%s:\t%s mM\n' %(item.compid,item.amount_mm)
        #return '%s' %compounds_str
	return '%s' %self.media_name.capitalize()

    #Define searchable terms
    def keywords(self):
	return [self.media_name]

    def __repr__(self):
        return '%s: id=%d, media_name=%s' % (type(self), self.medid, self.media_name)


    def sorted_compounds(self):
        return sorted(self.mediacompounds_set.all(), key=lambda c: c.compid.keywords()[0])

    def sorted_organisms(self):
        return sorted(list(set([gd.strainid for gd in self.growthdata_set.all()]))) # list(set(..)) removes dups

    def sources(self):
        return [x.sourceid for x in self.growthdata_set.all()]

class NamesOfCompounds(models.Model):
    nameid = models.IntegerField(primary_key=True, db_column='nameID') # Field name made lowercase.
    compid = models.ForeignKey(Compounds, db_column='compID') # Field name made lowercase.
    name = models.CharField(max_length=255L, unique=True, db_column='Name', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'names_of_compounds'
    #Return the name, not the name ID or compound ID
    def __unicode__(self):
        return '%s' %self.name

class Organisms(models.Model):
    strainid = models.IntegerField(primary_key=True, db_column='strainID') # Field name made lowercase.
    genus = models.CharField(max_length=255L, db_column='Genus', blank=True) # Field name made lowercase.
    species = models.CharField(max_length=255L, db_column='Species', blank=True) # Field name made lowercase.
    strain = models.CharField(max_length=255L, db_column='Strain', blank=True) # Field name made lowercase.
    contributorid = models.ForeignKey(Contributors, null=True, db_column='contributorID', blank=True) # Field name made lowercase.
    typeid = models.ForeignKey('TypesOfOrganisms', null=True, db_column='typeID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'organisms'
        verbose_name_plural = 'organisms'
    #Call the Organisms object and return the Strain Name and such instead
    def __unicode__(self):
        return '%s %s %s' %(self.genus.capitalize(),self.species.lower(),self.strain)

    #Define searchable terms
    def keywords(self):
	return [self.genus,self.species,self.strain]

    def __cmp__(self, other):
        ''' thought I would need this for sorting, but instead we sort in views.OrganismsListView '''
        for attr in ['genus', 'species', 'strain']:
            if getattr(self, attr).capitalize() > getattr(other,attr).capitalize(): return 1
            if getattr(self, attr).capitalize() < getattr(other,attr).capitalize(): return -1
        return 0

class OrganismsSources(models.Model):
    strainsourceid = models.IntegerField(primary_key=True, db_column='strainsourceID') # Field name made lowercase.
    strainid = models.ForeignKey(Organisms, null=True, db_column='strainID', blank=True) # Field name made lowercase.
    sourceid = models.ForeignKey('Sources', null=True, db_column='sourceID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'organisms_sources'

class Products(models.Model):
    prodid = models.IntegerField(primary_key=True, db_column='prodID') # Field name made lowercase.
    rxntid = models.ForeignKey('Reactants', db_column='rxntID') # Field name made lowercase.
    coeff = models.FloatField()
    compid = models.ForeignKey(Compounds, db_column='compID') # Field name made lowercase.
    class Meta:
        db_table = 'products'
# some comment

class Reactants(models.Model):
    rxntid = models.IntegerField(primary_key=True, db_column='rxntID') # Field name made lowercase.
    compid = models.ForeignKey(Compounds, db_column='compID',related_name='compound_id') # Field name made lowercase.
    similar_compounds = models.ForeignKey(Compounds, null=True, db_column='Similar Compounds',related_name='similar_id', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        db_table = 'reactants'

class SecretionUptake(models.Model):
    secretionuptakeid = models.IntegerField(primary_key=True, db_column='secretionuptakeID') # Field name made lowercase.
    growthid = models.ForeignKey(GrowthData, db_column='growthID') # Field name made lowercase.
    compid = models.IntegerField(null=True, db_column='compID', blank=True) # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    units = models.CharField(max_length=45L, db_column='Units') # Field name made lowercase.
    rateid = models.ForeignKey('SecretionUptakeKey', db_column='rateID') # Field name made lowercase.
    class Meta:
        db_table = 'secretion_uptake'

class SecretionUptakeKey(models.Model):
    rateid = models.IntegerField(primary_key=True, db_column='rateID') # Field name made lowercase.
    rate_type = models.CharField(max_length=45L, unique=True, db_column='Rate_Type', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'secretion_uptake_key'

class SeedCompounds(models.Model):
    seedkeggid = models.IntegerField(primary_key=True, db_column='seedkeggID') # Field name made lowercase.
    kegg_id = models.ForeignKey(Compounds, db_column='KEGG_ID') # Field name made lowercase.
    seed_id = models.CharField(max_length=45L, db_column='Seed_ID') # Field name made lowercase.
    class Meta:
        db_table = 'seed_compounds'

class Sources(models.Model):
    sourceid = models.IntegerField(primary_key=True, db_column='sourceID') # Field name made lowercase.
    first_author = models.CharField(max_length=255L, db_column='First_Author', blank=True) # Field name made lowercase.
    journal = models.CharField(max_length=255L, db_column='Journal', blank=True) # Field name made lowercase.
    year = models.TextField(db_column='Year', blank=True) # Field name made lowercase. This field type is a guess.
    title = models.CharField(max_length=255L, unique=True, db_column='Title', blank=True) # Field name made lowercase.
    link = models.CharField(max_length=255L, unique=True, db_column='Link', blank=True) # Field name made lowercase.

    def is_pdf(self):
        return self.link.lower().endswith('pdf')

    class Meta:
        db_table = 'sources'
        verbose_name_plural = 'sources'
    def __unicode__(self):
        return '%s et al, %d' %(self.first_author.capitalize(),self.year)   


    #Define searchable terms
    def keywords(self):
	return [self.first_author]

    @property
    def journal_cap(self):
        return ' '.join([x.capitalize() for x in self.journal.split(' ')])

class TypesOfOrganisms(models.Model):
    typeid = models.IntegerField(primary_key=True, db_column='typeID') # Field name made lowercase.
    organism_type = models.CharField(max_length=255L, unique=True, db_column='Organism_type', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'types_of_organisms'



class SearchResult(models.Model):
    keyword=models.CharField(max_length=255, db_index=True, editable=False)
    classname=models.CharField(max_length=64, editable=False)
    obj_id=models.IntegerField(editable=False)
    
    bad_chars=r'[@+*!]'

    class2view={
        'Compounds' : 'compound_record',
        'Organisms' : 'organism_record',
        'MediaNames' : 'media_record',
        'Biomass' : 'biomass_record',
        'Sources' : 'source_record',
        }

    class Meta:
        db_table='search_results'

    def __repr__(self):
        return '<pk=%s> %s-%s-%s' % (self.id, self.keyword, self.classname, self.obj_id)

    def __unicode__(self):
        return '%s: %s' % (self.classname, self.keyword)

    def clean(self):
        self.keyword=re.sub(self.bad_chars, '', self.keyword.lower())
        return self

    def obj_url(self):
        return reverse(self.class2view[self.classname], args=[self.obj_id])
