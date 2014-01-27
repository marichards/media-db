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
import re, inspect, logging, copy
from lazy import lazy

log=logging.getLogger(__name__)


from django.core.urlresolvers import reverse

class Biomass(models.Model):
    biomassid = models.AutoField(primary_key=True, db_column='biomassID') # Field name made lowercase.
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
    biocompid = models.AutoField(primary_key=True, db_column='biocompID') # Field name made lowercase.
    biomassid = models.ForeignKey(Biomass, db_column='biomassID') # Field name made lowercase.
    compid = models.ForeignKey('Compounds', db_column='compID') # Field name made lowercase.
    coefficient = models.FloatField(null=True, db_column='Coefficient', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'biomass_compounds'

    def __repr__(self):
        return 'biomass compound: biocompid=%d, biomassid=%s, compid=%s, coef=%g' % (self.biocompid, self.biomassid, self.compid, self.coefficient)

class CompoundExceptions(models.Model):
    pk = models.AutoField(primary_key=True)
    compid = models.ForeignKey('Compounds', db_column='compID') # Field name made lowercase.
    keggorgid = models.CharField(max_length=12L, db_column='keggOrgID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'compound_exceptions'

class CompoundReplacements(models.Model):
    pk = models.AutoField(primary_key=True)
    compid = models.ForeignKey('Compounds', db_column='compID') # Field name made lowercase.
    biggid = models.CharField(max_length=12L, db_column='biggID') # Field name made lowercase.
    keggorgid = models.CharField(max_length=12L, db_column='keggOrgID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'compound_replacements'

class CompoundManager(models.Manager):
    def with_name(self, name):
        try:
            return Compounds.objects.get(name=name)
        except Compounds.DoesNotExist:
            try:
                synonym=NamesOfCompounds.objects.get(name=name)
                return synonym.compid
            except NamesOfCompounds.DoesNotExist, e:
                raise Compounds.DoesNotExist(e) 

class Compounds(models.Model):
    compid = models.AutoField(primary_key=True, db_column='compID') # Field name made lowercase.
    kegg_id = models.CharField(max_length=255L, unique=True, db_column='KEGG_ID', blank=True, null=True) # Field name made lowercase.
    bigg_id = models.CharField(max_length=255L, db_column='BiGG_ID', blank=True, null=True) # Field name made lowercase.
    seed_id = models.CharField(max_length=45L, db_column='seed_id') # Field name made lowercase.
    pubchem_ids = models.CharField(max_length=255L, db_column='pubchem_ids', null=True, blank=True) # csv
    chebi_ids = models.CharField(max_length=255L, db_column='chebi_ids', null=True, blank=True) # csv
    user_identifier = models.CharField(max_length=255L, blank=True, null=True)
    name = models.CharField(max_length=255L, unique=True)
    formula=models.CharField(max_length=255L, null=True, blank=True)

    objects=CompoundManager()

    class Meta:
        db_table = 'compounds'
	verbose_name_plural = 'compounds'
    #Return the first compound name for each thing
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return 'compound %s (%d): kegg_id=%s, bigg_id=%s, seed_id=%s, user_identifier=%s formula=%s' % \
        (self.name, self.compid, self.kegg_id, self.bigg_id, self.seed_id, self.user_identifier, self.formula)

    def keywords(self):
        nocs=[noc.name for noc in NamesOfCompounds.objects.filter(compid=self.compid)]
        if (self.name and self.name != self.compid):
            nocs.insert(0, self.name)
        return nocs

    def names(self):
        return ', '.join(self.keywords())

    def media_names(self):
        mcs=MediaCompounds.objects.filter(compid=self.compid)
        mednames=list(set([x.medid for x in mcs]))
        return sorted(mednames, key=lambda mc: mc.media_name)

    def kegg_url(self):
        return 'http://www.genome.jp/dbget-bin/www_bget?%s' % self.kegg_id

    def seed_url(self):
        return 'http://seed-viewer.theseed.org/seedviewer.cgi?page=CompoundViewer&compound=%s&model=' % self.seed_id

    

    def keywords(self):
        return [x.name for x in self.namesofcompounds_set.all()]

class Contributors(models.Model):
    contributorid = models.IntegerField(primary_key=True, db_column='contributorID') # Field name made lowercase.
    last_name = models.CharField(max_length=255L, unique=True, db_column='Last_Name', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'contributors'
        verbose_name_plural = 'contributors'
    def __unicode__(self):
        return self.last_name

class GrowthData(models.Model):
    growthid = models.AutoField(primary_key=True, db_column='growthID') # Field name made lowercase.
    contributor=models.ForeignKey('Contributor')
    strainid = models.ForeignKey('Organisms', db_column='strainID') # Field name made lowercase.
    medid = models.ForeignKey('MediaNames', db_column='medID') # Field name made lowercase.
    sourceid = models.ForeignKey('Sources', db_column='sourceID') # Field name made lowercase.
    growth_rate = models.FloatField(null=True, db_column='Growth_Rate', blank=True) # Field name made lowercase.
    growth_units = models.CharField(max_length=45L, db_column='Growth_Units', blank=True) # Field name made lowercase.
    ph = models.FloatField(null=True, db_column='pH', blank=True) # Field name made lowercase.
    temperature_c = models.FloatField(null=True, db_column='Temperature_C', blank=True) # Field name made lowercase.
    measureid = models.ForeignKey('Measurements', null=True, db_column='measureID', blank=True) # Field name made lowercase.
    additional_notes = models.CharField(max_length=255L, db_column='Additional_Notes', blank=True, null=True) # Field name made lowercase.
    class Meta:
        db_table = 'growth_data'
	verbose_name_plural = 'growth data'
    #Method: Python calls Growth Object and Returns the ID instead of just "GrowthData Object" 
    def __unicode__(self):
        return '%s on %s' %(self.strainid,self.medid)   

    def __repr__(self):
        return "GrowthData(%s) %s: org(%s)=%s, media_name(%s)=%s, sourceid(%s)=%s, measureid(%s)=%s" % \
            (self.growthid, self.contributor, self.strainid_id, self.strainid, self.medid_id, 
             self.medid, self.sourceid_id, self.sourceid, self.measureid_id, self.measureid)


    def media_compounds_dicts(self):
        return [{'comp': mc.compid.name, 'amount': mc.amount_mm} for mc in self.medid.mediacompounds_set.all()]

    def dump(self):
        '''
        List the entire growth data object, including: media_name, org, source, all media_compounds
        and secretion_uptake objects
        '''
        report='GrowthData %d:\n' % self.growthid;
        report += '      Organism(%d): %s\n' % (self.strainid_id, self.strainid)
        report += '     MediaName(%d): %s\n' % (self.medid_id, self.medid)
        report += '        Source(%d): %s\n' % (self.sourceid_id, self.sourceid)

        report += 'MediaCompounds[%d]\n' % self.medid.mediacompounds_set.count()
        for i,mc in enumerate(self.medid.mediacompounds_set.all()):
            report += ' MediaCompound[%d]: (%d) %s\n' % (i, mc.medcompid, mc)

        report += 'SecretionUptakes[%d]\n' % self.secretionuptake_set.count()
        for i,su in enumerate(self.secretionuptake_set.all()):
            report += 'SecretionUptake[%d]: (%d) %s\n' % (i, su.secretionuptakeid, su)
        return report
        

    def uptake_dicts(self):
        ''' return an array of dicts.  Each dict has keys=[comp, rate, units, type] '''
        return [{'comp': Compounds.objects.get(compid=su.compid).name, 'rate': su.rate, 'units': su.units, 'type': su.rateid_id} for su in self.secretionuptake_set.all()]

    def as_dict(gd):
        d={
            'contributor_id': gd.contributor_id,
            'genus':          gd.strainid.genus,
            'species' :       gd.strainid.species,
            'strain' :        gd.strainid.strain,

            'media_name' :    gd.medid.media_name,
            'is_defined' :    gd.medid.is_defined,
            'is_minimal' :    gd.medid.is_minimal,

            'first_author' :  gd.sourceid.first_author,
            'journal' :       gd.sourceid.journal,
            'year' :          gd.sourceid.year,
            'title' :         gd.sourceid.title,
            'link' :          gd.sourceid.link,
             
            'growth_rate' :   gd.growth_rate,
            'temperature' :   gd.temperature_c,
            'ph' :            gd.ph,
            }

        if hasattr(gd, 'growthid'):
            d['growthid']=gd.growthid # clon3d gds lack this
            

        # make comp1 and amount1 key/value pairs:
        n=1
        for medcomp in gd.medid.mediacompounds_set.all():
           d['comp%d' % n]=medcomp.compid.name
           d['amount%d' % n]=medcomp.amount_mm
           n+=1

        n=1
        for su in gd.secretionuptake_set.all():
            comp=Compounds.objects.get(compid=su.compid)
            d['uptake_comp%d' % n]=comp.name
            d['uptake_rate%d' % n]=su.rate
            d['uptake_unit%d' % n]=su.units
            d['uptake_type%d' % n]=su.rateid_id
            n+=1
        return d

    def full_delete(self):
        log.debug('full_delete called')
        # delete secretion_uptakes
        # apparently this happens automatically...
#        for su in self.secretionuptake_set.all():
#            su.delete()

        # delete media_name
        self.medid.delete()

        # delete self
        self.delete()

    def find_clone(self):
        '''
        find a growth data record that would cause self.save() to fail due to the 'unique_conditions' index:
        '''
        try:
            args={
                'strainid':self.strainid,
                'medid':self.medid,
                'sourceid':self.sourceid,
                'growth_rate':self.growth_rate,
                'ph':self.ph,
                'temperature_c':self.temperature_c,
                }
            return GrowthData.objects.get(**args)
        except GrowthData.DoesNotExist:
            return None


    def clone_and_save(self, contributor=None):
        '''
        clones may share: medid, contributor, strainid, sourceid, or any of the basic
        info.  BUT: they can't share ALL of it.  So we create a new MediaNames object,
        change its media_name field (by appending ' (clone)', and use that to satisfy
        the uniqueness constraint.
        '''
        if contributor is None:
            contributor=Contributor.objects.get(id=self.contributor_id)
        clone=copy.copy(self)
        clone.growthid=None
        clone.contributor_id=contributor.id
        clone.medid=self.medid.clone_and_save()
        clone.save()

        # have to copy medianames and secretionuptake objects:
        '''
        goddamit
        In order to make copies of secretionuptake objects,
        we need to set their growthid reference to the new
        gd's growthid.  But that doesn't exist, until we save 
        the new gd.  But saving a clone is going to trip against
        the 'unique_conditions' index, unless we change one of
        the contraints.  media_name is the best candidate for that
        (append a "clone of %growthdata_id" to the name), but then
        we also have to copy all of the media_compound objects.
        
        So we're at the point of saving all new versions of media_compound
        objects and secretionuptake objects....  AND we have to save the new
        gd object as well, in order for all this to work.
        '''
        for su in self.secretionuptake_set.all():
            new_su=copy.copy(su)
            new_su.secretionuptakeid=None
            su.growthid=clone
            su.save()

        return clone

    def equals(self, other):
        # ignore growthid unless both are defined:
        '''
        try:
            self_id=self.growthid
            other_id=other.growthid
            if self_id != None and other_id != None and self_id != other_id:
                log.debug('returning False on self_id: %s, other_id=%s' % (self_id, other_id))
                return False
        except NameError:
            pass
        '''

        if self.contributor_id != other.contributor_id:
            log.debug('returning False on contributor_id: %s vs %s' % (self.contributor_id, other.contributor_id))
            return False
        if self.strainid_id != other.strainid_id: 
            log.debug('returning False on strainid')
            return False
        if self.medid_id != other.medid_id:
            log.debug('returning False on medid: %s vs %s' % (self.medid_id, other.medid_id))
            return False
        if self.sourceid_id != other.sourceid_id:
            log.debug('returning False on sourceid')
            return False
        
        for attr in 'growth_rate growth_units ph temperature_c'.split(' '):
            if getattr(self, attr) != getattr(other, attr):
                log.debug('returing False on %s' % attr)
                return False
            
        if not self.medid._compound_list_equal(other.medid):
            log.debug('returning False on compound_list')
            return False

        log.debug('returing True')
        return True


    def not_equals(self, other):
        return not self.equals(other)

class Measurements(models.Model):
    measureid = models.AutoField(primary_key=True, db_column='measureID') # Field name made lowercase.
    measurement_technique = models.CharField(max_length=255L, unique=True, db_column='Measurement_Technique', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'measurements'
    def __unicode__(self):
        return '%s' %self.measurement_technique

class MediaCompounds(models.Model):
    medcompid = models.AutoField(primary_key=True, db_column='medcompID') # Field name made lowercase.
    medid = models.ForeignKey('MediaNames', db_column='medID') # Field name made lowercase.
    compid = models.ForeignKey(Compounds, db_column='compID') # Field name made lowercase.
    amount_mm = models.FloatField(null=True, db_column='Amount_mM', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'media_compounds'

    def __unicode__(self):
        return '%s %gmm' % (self.compid.__unicode__(), self.amount_mm)

    def __repr__(self):
        return 'MediaCompound %d: medid=%s, compid=%s, amount_mm=%g' % (self.medcompid, self.medid, self.compid, self.amount_mm)


class MediaNames(models.Model):
    medid = models.AutoField(primary_key=True, db_column='medID') # Field name made lowercase.
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
	return '%s' % self.media_name.capitalize()

    def __repr__(self):
        return 'MediaNames: (%d, %s, %s, %s)' % (self.medid, 
                                                 self.media_name, 
                                                 self.is_defined, 
                                                 self.is_minimal)

    #Define searchable terms
    def keywords(self):
	return [self.media_name]

    def sorted_compounds(self):
        ''' return a list of compounds for the MediaCompound, sorted on name '''
        # return sorted(self.mediacompounds_set.all(), key=lambda c: c.compid.keywords()[0]) # some compounds have no keywords, so keywords()[0] barfs
        return sorted(self.mediacompounds_set.all(), key=lambda c: c.compid.name) # some compounds have no keywords, so keywords()[0] barfs
#        for mc in self.mediacompounds_set.all():
            

    def sorted_organisms(self):
        return sorted(list(set([gd.strainid for gd in self.growthdata_set.all()]))) # list(set(..)) removes dups

    def sources(self):
        return [x.sourceid for x in self.growthdata_set.all()]

    def uniq_sources(self):
        return list(set([x.sourceid for x in self.growthdata_set.all()]))

    def _compound_list_equal(self, other):
        s_comps=self.mediacompounds_set
        o_comps=other.mediacompounds_set
        if s_comps.count() != o_comps.count():
            log.debug('_cle: returning False on differing length')
            return False

        s_set=set([c for c in s_comps.all()])
        o_set=set([c for c in o_comps.all()])
        if s_set!=o_set: 
            log.debug('_cle: returning False on set inequality')
            return False

        for s_mc in s_set:      # not sure this doesn't duplicate functionality above
            if s_mc not in o_set:
                log.debug('_cle: returning False on %s' % s_mc)
                return False

        log.debug('_cle: returning True')
        return True


    def clone_and_save(self):
        '''
        make a clone of an existing MediaName object, store to db
        ''' 
        clone=copy.copy(self)
        clone.medid=None
        clone.media_name=self.media_name+' (clone)'
        clone.save()
        
        for mc in self.mediacompounds_set.all():
            mc.medcompid=None
            mc.medid=clone
            mc.save()
        return clone

class NamesOfCompounds(models.Model):
    nameid = models.AutoField(primary_key=True, db_column='nameID') # Field name made lowercase.
    compid = models.ForeignKey(Compounds, db_column='compID') # Field name made lowercase.
    name = models.CharField(max_length=255L, unique=True, db_column='Name', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'names_of_compounds'
    #Return the name, not the name ID or compound ID
    def __unicode__(self):
        return '%s' %self.name

class Organisms(models.Model):
    strainid = models.AutoField(primary_key=True, db_column='strainID') # Field name made lowercase.
    genus = models.CharField(max_length=255L, db_column='Genus', blank=True) # Field name made lowercase.
    species = models.CharField(max_length=255L, db_column='Species', blank=True) # Field name made lowercase.
    strain = models.CharField(max_length=255L, db_column='Strain', blank=True) # Field name made lowercase.
#    contributorid = models.ForeignKey(Contributors, null=True, db_column='contributorID', blank=True) # Field name made lowercase.
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
    strainsourceid = models.AutoField(primary_key=True, db_column='strainsourceID') # Field name made lowercase.
    strainid = models.ForeignKey(Organisms, null=True, db_column='strainID', blank=True) # Field name made lowercase.
    sourceid = models.ForeignKey('Sources', null=True, db_column='sourceID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'organisms_sources'

class Products(models.Model):
    prodid = models.AutoField(primary_key=True, db_column='prodID') # Field name made lowercase.
    rxntid = models.ForeignKey('Reactants', db_column='rxntID') # Field name made lowercase.
    coeff = models.FloatField()
    compid = models.ForeignKey(Compounds, db_column='compID') # Field name made lowercase.
    class Meta:
        db_table = 'products'
# some comment

class Reactants(models.Model):
    rxntid = models.AutoField(primary_key=True, db_column='rxntID') # Field name made lowercase.
    compid = models.ForeignKey(Compounds, db_column='compID',related_name='compound_id') # Field name made lowercase.
    similar_compounds = models.ForeignKey(Compounds, null=True, db_column='Similar Compounds',related_name='similar_id', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        db_table = 'reactants'


class SecretionUptake(models.Model):
    secretionuptakeid = models.AutoField(primary_key=True, db_column='secretionuptakeID') # Field name made lowercase.
    growthid = models.ForeignKey(GrowthData, db_column='growthID') # Field name made lowercase.
    compid = models.IntegerField(null=True, db_column='compID', blank=True) # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    units = models.CharField(max_length=45L, db_column='Units') # Field name made lowercase.
    rateid = models.ForeignKey('SecretionUptakeKey', db_column='rateID') # Field name made lowercase.
    class Meta:
        db_table = 'secretion_uptake'

    def __repr__(self):
        return 'SecretionUptake %s: growth=%s, compound=%s, rate=%s, units=%s, rateid=%s' \
            %(self.secretionuptakeid, self.growthid, self.compid, self.rate, self.units, self.rateid)


class SecretionUptakeKey(models.Model):
    rateid = models.AutoField(primary_key=True, db_column='rateID') # Field name made lowercase.
    rate_type = models.CharField(max_length=45L, unique=True, db_column='Rate_Type', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'secretion_uptake_key'

'''
class SeedCompounds(models.Model):
    seedkeggid = models.AutoField(primary_key=True, db_column='seedkeggID') # Field name made lowercase.
    kegg_id = models.CharField(max_length=45L, db_column='KEGG_ID') # Field name made lowercase.
#    kegg_id = models.ForeignKey(Compounds, db_column='KEGG_ID') # Field name made lowercase.
    seed_id = models.CharField(max_length=45L, db_column='Seed_ID') # Field name made lowercase.
    class Meta:
        db_table = 'seed_compounds'

    def __repr__(self):
        return 'SeedCompound %s: kegg_id=%s, seed_id=%s' % (self.seedkeggid, self.kegg_id, self.seed_id)
'''
    

class Sources(models.Model):
    sourceid = models.AutoField(primary_key=True, db_column='sourceID') # Field name made lowercase.
    first_author = models.CharField(max_length=255L, db_column='First_Author', blank=True) # Field name made lowercase.
    journal = models.CharField(max_length=255L, db_column='Journal', blank=True) # Field name made lowercase.
    year = models.TextField(db_column='Year', blank=True) # Field name made lowercase. This field type is a guess.
    title = models.CharField(max_length=255L, unique=True, db_column='Title', blank=True) # Field name made lowercase.
    link = models.CharField(max_length=255L, unique=True, db_column='Link', blank=True) # Field name made lowercase.
    pubmed_id = models.IntegerField(null=True, blank=True)

    def is_pdf(self):
        return self.link.lower().endswith('pdf')

    def pubmed_link(self):
        if self.pubmed_id:
            return 'http://www.ncbi.nlm.nih.gov/pubmed/?term=%d' % self.pubmed_id
        else:
            return None

    class Meta:
        db_table = 'sources'
        verbose_name_plural = 'sources'
    def __unicode__(self):
        year=self.year or ''
        return '%s et al, %s' %(self.first_author.capitalize(),year)

    def __repr__(self):
        format='Source sourceid=%s, pubmed=%s, f_author=%s, journal=%s, year=%s, title=%s, link=%s'
        tup=(self.sourceid, self.pubmed_id, self.first_author, self.journal, self.year, self.title, self.link)
        return format % tup

    #Define searchable terms
    def keywords(self):
	return [self.first_author]

    @property
    def journal_cap(self):
        return ' '.join([x.capitalize() for x in self.journal.split(' ')])

class TypesOfOrganisms(models.Model):
    typeid = models.AutoField(primary_key=True, db_column='typeID') # Field name made lowercase.
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

    def get_obj(self):
        return get_obj(self.classname, self.obj_id)

def get_obj(classname, pk):
    cls=globals()[classname]
    pk_name=cls._meta.pk.name
    args={pk_name: pk}
    return cls.objects.get(**args)

from django.contrib.auth.models import User
class Contributor(models.Model):
    first_name=models.CharField(max_length=64, editable=False)
    last_name=models.CharField(max_length=64, editable=False)
    user=models.OneToOneField(User)
    lab=models.ForeignKey('Lab')

    class Meta:
        db_table='contributor'
    
    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __repr__(self):
        return '%s %s (%s, lab=%s)' % (self.first_name, self.last_name, self.user.username, self.lab)

    def can_edit_gd(self, gd):
        log.debug('contributor %s: is_superuser=%s, is_active=%s, self.id=%d, gd.id=%d' % (self, self.user.is_superuser, self.user.is_active, self.id, gd.contributor_id))
        return self.user.is_superuser or (self.user.is_active and self.id==gd.contributor_id)

    def editable_gds(self):
        log.debug('editable_gds: user is %s' % self.user)
        if self.user.is_superuser:
            log.debug('superuser! returning all gds')
            return GrowthData.objects.all()
        else:
            log.debug('muggle :( only returning loser gds')
            return GrowthData.objects.filter(contributor_id=self.id)

    def name(self):
        return '%s %s' % (self.first_name, self.last_name)
        

class Lab(models.Model):
    name=models.CharField(max_length=64, unique=True)
    url=models.URLField()
    

    class Meta:
        db_table='labs'

    def __unicode__(self):
        return self.name

