# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models, IntegrityError
import re, inspect, logging, copy
from lazy import lazy


log=logging.getLogger(__name__)

from django.core.urlresolvers import reverse

class Biomass(models.Model):
    biomassid = models.AutoField(primary_key=True, db_column='biomassID') 
    genus = models.CharField(max_length=255L, db_column='Genus') 
    species = models.CharField(max_length=255L, db_column='Species') 
    sourceid = models.ForeignKey('Sources', null=True, db_column='sourceID', blank=True) 
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
    biocompid = models.AutoField(primary_key=True, db_column='biocompID') 
    biomassid = models.ForeignKey(Biomass, db_column='biomassID') 
    compid = models.ForeignKey('Compounds', db_column='compID') 
    coefficient = models.FloatField(null=True, db_column='Coefficient', blank=True) 
    class Meta:
        db_table = 'biomass_compounds'

    def __repr__(self):
        return 'biomass compound: biocompid=%d, biomassid=%s, compid=%s, coef=%g' % (self.biocompid, self.biomassid, self.compid, self.coefficient)

class CompoundManager(models.Manager):
    def with_name(self, name):
        try:
            return Compounds.objects.get(name=name)
        except Compounds.DoesNotExist:
            pass

        try:
            return Compounds.objects.get(formula=name)
        except Compounds.DoesNotExist:
            pass

        try:
            synonym=NamesOfCompounds.objects.get(name=name)
            return synonym.compid
        except NamesOfCompounds.DoesNotExist, e:
            pass

        
        raise Compounds.DoesNotExist(name)

class Compounds(models.Model):
    compid = models.AutoField(primary_key=True, db_column='compID') 
    kegg_id = models.CharField(max_length=255L, unique=True, db_column='KEGG_ID', blank=True, null=True) 
    bigg_id = models.CharField(max_length=255L, db_column='BiGG_ID', blank=True, null=True) 
    seed_id = models.CharField(max_length=45L, db_column='seed_id') 
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

        # add in various ids:
        for attr in 'formula seed_id kegg_id'.split(' '):
            if hasattr(self, attr) and getattr(self, attr):
                nocs.append(getattr(self, attr))

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

    

class Contributors(models.Model):
    contributorid = models.IntegerField(primary_key=True, db_column='contributorID') 
    last_name = models.CharField(max_length=255L, unique=True, db_column='Last_Name', blank=True) 
    class Meta:
        db_table = 'contributors'
        verbose_name_plural = 'contributors'
    def __unicode__(self):
        return self.last_name

class GrowthData(models.Model):
    growthid = models.AutoField(primary_key=True, db_column='growthID') 
    contributor=models.ForeignKey('Contributor')
    strainid = models.ForeignKey('Organisms', db_column='strainID') 
    medid = models.ForeignKey('MediaNames', db_column='medID') 
    sourceid = models.ForeignKey('Sources', db_column='sourceID') 
    growth_rate = models.FloatField(null=True, db_column='Growth_Rate', blank=True) 
    growth_units = models.CharField(max_length=45L, db_column='Growth_Units', blank=True) 
    ph = models.FloatField(null=True, db_column='pH', blank=True) 
    temperature_c = models.FloatField(null=True, db_column='Temperature_C', blank=True) 
    additional_notes = models.CharField(max_length=255L, db_column='Additional_Notes', blank=True, null=True) 
    approved=models.BooleanField(default=True)

    class Meta:
        db_table = 'growth_data'
	verbose_name_plural = 'growth data'
        ordering=['strainid__genus', 'strainid__species', 'strainid__strain', 'medid__media_name']
        
    #Method: Python calls Growth Object and Returns the ID instead of just "GrowthData Object" 
    def __unicode__(self):
        return '%s on %s' %(self.strainid, self.medid)   

    def __repr__(self):
        return "GrowthData(%s) %s: org(%s)=%s, media_name(%s)=%s, sourceid(%s)=%s, approved=%s" % \
            (self.growthid, self.contributor, self.strainid_id, self.strainid, self.medid_id, 
             self.medid, self.sourceid_id, self.sourceid, self.approved)


    def media_compounds_dicts(self):
        return self.medid.media_compounds_dicts()

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
            'contributor' : gd.contributor.id,
            'strainid'    : gd.strainid_id,
            'sourceid'    : gd.sourceid_id,
            'growth_rate' : gd.growth_rate,
            'temperature_c' : gd.temperature_c,
            'ph'          : gd.ph,
            }


        if hasattr(gd, 'growthid'):
            d['growthid']=gd.growthid # cloned gds lack this
            

        # make comp1 and amount1 key/value pairs:
        d.update(gd.medid.as_dict())

        n=1
        for su in gd.secretionuptake_set.all():
            comp=Compounds.objects.get(compid=su.compid_id)
            d['uptake_comp%d' % n]=comp.name
            d['uptake_rate%d' % n]=su.rate
            d['uptake_unit%d' % n]=SecretionUptakeUnit.id_of(su.units)
#            d['uptake_unit%d' % n]=su.units_id
            d['uptake_type%d' % n]=su.rateid_id
            n+=1
        return d

    def find_clone(self):
        '''
        find a growth data record that would cause self.save() to fail due to the 'unique_conditions' index:
        '''
        try:
            args={
                'strainid':self.strainid,
                'medid':self.medid,
                'sourceid':self.sourceid,
                }
            
            # sometimes these are not defined:
            for f in 'growth_rate ph temperature_c'.split(' '):
                try:
                    args[f]=float(getattr(self, f))
                except (ValueError, TypeError) as e:
                    pass

            return GrowthData.objects.get(**args)
        except GrowthData.DoesNotExist:
            return None



    def clone_and_save(self, contributor=None):
        '''
        clones may share: medid, contributor, strainid, sourceid, or any of the basic
        info.  BUT: they can't share ALL of it.  So we create a new MediaNames object,
        change its media_name field (by appending ' (clone)', and use that to satisfy
        the uniqueness constraint).
        '''
        if contributor is None:
            contributor=Contributor.objects.get(id=self.contributor_id)
        clone=copy.copy(self)
        clone.growthid=None
        clone.contributor_id=contributor.id
        clone.medid=self.medid.clone()
        clone.save()

        # have to copy medianames and secretionuptake objects:
        for su in self.secretionuptake_set.all():
            new_su=copy.copy(su)
            new_su.secretionuptakeid=None
            su.growthid=clone
            su.save()

        return clone

    def equals(self, other):
        '''
        Check various fields and lists in the growth record to determine equality.
        '''
        if self.contributor_id != other.contributor_id:
            return False
        if self.strainid_id != other.strainid_id: 
            return False
        if self.medid_id != other.medid_id:
            return False
        if self.sourceid_id != other.sourceid_id:
            return False
        
        for attr in 'growth_rate growth_units ph temperature_c'.split(' '):
            if getattr(self, attr) != getattr(other, attr):
                return False
            
        if not self.medid._compound_list_equal(other.medid):
            return False

        return True


    def not_equals(self, other):
        return not self.equals(other)

class MediaCompounds(models.Model):
    medcompid = models.AutoField(primary_key=True, db_column='medcompID') 
    medid = models.ForeignKey('MediaNames', db_column='medID') 
    compid = models.ForeignKey(Compounds, db_column='compID') 
    amount_mm = models.FloatField(null=True, db_column='Amount_mM', blank=True) 
    class Meta:
        db_table = 'media_compounds'

    def __unicode__(self):
#        return '%s %gmm' % (self.compid.__unicode__(), self.amount_mm)
        return '%s %smm' % (self.compid.__unicode__(), self.amount_mm)

    def __repr__(self):
        return 'MediaCompound %d: medid=%s, compid=%s, amount_mm=%g' % (self.medcompid, self.medid, self.compid, self.amount_mm)


class MediaNames(models.Model):
    medid = models.AutoField(primary_key=True, db_column='medID') 
    media_name = models.CharField(max_length=255L, db_column='Media_name', blank=False, unique=True) 
    is_defined = models.CharField(max_length=1L, db_column='Is_defined', blank=True) 
    is_minimal = models.CharField(max_length=1L, db_column='Is_minimal', blank=True) 

    class Meta:
        db_table = 'media_names'
	verbose_name_plural = 'media names'
        ordering=['media_name']

    def __unicode__(self):
        #Define a method that grabs everything in a given medium
        #compounds_list = MediaCompounds.objects.filter(medid=self.medid)
        #compounds_str = '%s contains: ' %self.media_name
	#for item in compounds_list:
        #    compounds_str += '%s:\t%s mM\n' %(item.compid,item.amount_mm)
        #return '%s' %compounds_str
	return '%s' % self.media_name.capitalize()

    def __repr__(self):
        return 'MediaNames: (medid=%s, %s, %s, %s)' % (self.medid, 
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
            return False

        s_set=set([c for c in s_comps.all()])
        o_set=set([c for c in o_comps.all()])
        if s_set!=o_set: 
            return False

        for s_mc in s_set:      # not sure this doesn't duplicate functionality above
            if s_mc not in o_set:
                return False

        return True


    def clone(self):
        '''
        make a clone of an existing MediaName object, store to db
        ''' 
        clone=copy.copy(self)
        clone.medid=None
        clone.media_name=self.media_name+' (clone)'
        clone.save()

        for mc in self.mediacompounds_set.all():
            mc=MediaCompounds(compid=mc.compid, amount_mm=mc.amount_mm)
            clone.mediacompounds_set.add(mc)

        return clone


    def media_compounds_dicts(self):
        ''' 
        return a list of hashlettes: d[compN]=compound name, d[amountN]=amount.
        Used by medianames_form.html and core.MediaText
        '''
        return [{'comp': mc.compid.name, 
                 'amount': mc.amount_mm,
                 'kegg_id' : mc.compid.kegg_id or None,
                 'bigg_id': mc.compid.bigg_id or None,
                 'seed_id': mc.compid.seed_id or None,
                 'pubchem_ids': mc.compid.pubchem_ids or None,
                 'chebi_ids': mc.compid.chebi_ids or None,
                 } for mc in self.mediacompounds_set.all()]

    def as_dict(self):
        d=dict((attr, getattr(self, attr)) for attr in 'medid media_name is_defined is_minimal'.split(' '))

        for n,medcomp in enumerate(self.mediacompounds_set.all()):
           d['comp%d' % n]=medcomp.compid.name
           d['amount%d' % n]=medcomp.amount_mm
        return d


class NamesOfCompounds(models.Model):
    nameid = models.AutoField(primary_key=True, db_column='nameID') 
    compid = models.ForeignKey(Compounds, db_column='compID') 
    name = models.CharField(max_length=255L, unique=True, db_column='Name', blank=True) 
    class Meta:
        db_table = 'names_of_compounds'
    #Return the name, not the name ID or compound ID
    def __unicode__(self):
        return '%s' %self.name

class Organisms(models.Model):
    strainid = models.AutoField(primary_key=True, db_column='strainID')
    # Not sure about blank=False on these; might mess up newmediaform since species and strain added dynamically
    genus = models.CharField(max_length=255L, db_column='Genus', blank=False, null=False)
    species = models.CharField(max_length=255L, db_column='Species', blank=False, null=False)
    strain = models.CharField(max_length=255L, db_column='Strain', blank=False, null=False) 
    typeid = models.ForeignKey('TypesOfOrganisms', db_column='typeID')

    class Meta:
        db_table = 'organisms'
        verbose_name_plural = 'organisms'
        ordering=['genus', 'species', 'strain']

    #Call the Organisms object and return the Strain Name and such instead
    def __unicode__(self):
        return '%s %s %s' %(self.genus.capitalize(),self.species.lower(),self.strain)
    
    #Return link to NCBI genome project
    def ncbi_link(self):
	return 'http://www.ncbi.nlm.nih.gov/genome/?term=%s+%s' %(self.genus,self.species)

    def save(self):
        missing=[]
        for attr in 'genus species strain'.split(' '):
            try:
                if len(getattr(self, attr))==0:
                    missing.append('%s blank' % attr)
            except AttributeError:
                missing.append('%s missing' % attr)
        if len(missing)>0:
            raise IntegrityError(', '.join(missing))

        return super(Organisms,self).save()

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
    strainsourceid = models.AutoField(primary_key=True, db_column='strainsourceID') 
    strainid = models.ForeignKey(Organisms, null=True, db_column='strainID', blank=True) 
    sourceid = models.ForeignKey('Sources', null=True, db_column='sourceID', blank=True) 
    class Meta:
        db_table = 'organisms_sources'

class SecretionUptake(models.Model):
    secretionuptakeid = models.AutoField(primary_key=True, db_column='secretionuptakeID') 
    growthid = models.ForeignKey(GrowthData, db_column='growthID') 
#    compid = models.IntegerField(null=True, db_column='compID', blank=True) 
    compid = models.ForeignKey(Compounds, null=True, db_column='compID', blank=True) 
    rate = models.FloatField(db_column='Rate') 
    units = models.CharField(max_length=45L, db_column='Units') 
    rateid = models.ForeignKey('SecretionUptakeKey', db_column='rateID') 

    class Meta:
        db_table = 'secretion_uptake'

    def __unicode__(self):
        return repr(self)

    def __repr__(self):
        return 'SecretionUptake %s: growth (%d)=%s, compound=%s, rate=%s, units=%s, rateid=%s' \
            %(self.secretionuptakeid, self.growthid_id, self.growthid, self.compid, self.rate, self.units, self.rateid)


class SecretionUptakeKey(models.Model):
    rateid = models.AutoField(primary_key=True, db_column='rateID') 
    rate_type = models.CharField(max_length=45L, unique=True, db_column='Rate_Type', blank=True) 
    class Meta:
        db_table = 'secretion_uptake_key'

    def __unicode__(self):
        return '%s' % (self.rate_type)

class SecretionUptakeUnit(models.Model):
    unit=models.CharField(max_length=12, unique=True, blank=False)
    class Meta:
        db_table='secretion_uptake_unit'

    def __unicode__(self):
        return '%s' % self.unit
    
    @classmethod
    def _get_unit2id(self):
        u2i={}
        for suu in self.objects.all():
            u2i[suu.unit]=suu.id
        return u2i

    @classmethod
    def id_of(self, unit):
        try: return self._unit2id[unit]
        except AttributeError:
            self._unit2id=self._get_unit2id()
            return self._unit2id[unit]
            

'''
class SeedCompounds(models.Model):
    seedkeggid = models.AutoField(primary_key=True, db_column='seedkeggID') 
    kegg_id = models.CharField(max_length=45L, db_column='KEGG_ID') 
#    kegg_id = models.ForeignKey(Compounds, db_column='KEGG_ID') 
    seed_id = models.CharField(max_length=45L, db_column='Seed_ID') 
    class Meta:
        db_table = 'seed_compounds'

    def __repr__(self):
        return 'SeedCompound %s: kegg_id=%s, seed_id=%s' % (self.seedkeggid, self.kegg_id, self.seed_id)
'''
    

class Sources(models.Model):
    sourceid = models.AutoField(primary_key=True, db_column='sourceID') 
    first_author = models.CharField(max_length=255L, db_column='First_Author', blank=True) 
    journal = models.CharField(max_length=255L, db_column='Journal', blank=True) 
    year = models.CharField(db_column='Year', blank=True, max_length=4L)  
    title = models.CharField(max_length=255L, unique=True, db_column='Title', blank=True) 
    link = models.CharField(max_length=255L, unique=False, db_column='Link', blank=True) 
    pubmed_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'sources'
        verbose_name_plural = 'sources'
        unique_together='first_author journal title'.split(' ')

        ordering=['first_author', 'title']

    def is_pdf(self):
        return self.link.lower().endswith('pdf')

    def pubmed_link(self):
        if self.pubmed_id:
            return 'http://www.ncbi.nlm.nih.gov/pubmed/?term=%d' % self.pubmed_id
        else:
            return None

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
    typeid = models.AutoField(primary_key=True, db_column='typeID') 
    organism_type = models.CharField(max_length=255L, unique=True, db_column='Organism_type', blank=True)
    
    class Meta:
        db_table = 'types_of_organisms'

    def __unicode__(self):
        return self.organism_type


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

    def can_edit_gd(self, gd=None):
        return self.user.is_superuser
#        return self.user.is_superuser or (self.user.is_active and self.id==gd.contributor_id)

    def editable_gds(self):
        if self.user.is_superuser:
            return GrowthData.objects.all()
        else:
#            return GrowthData.objects.filter(contributor_id=self.id)
            return []

    def editable_mns(self):
        if self.user.is_superuser:
            return MediaNames.objects.all()
        else:
#            return MediaNames.objects.filter(contributor_id=self.id)
            return []

    def can_edit_mn(self, mn=None):
        return self.user.is_superuser

    def name(self):
        return '%s %s' % (self.first_name, self.last_name)
        

class Lab(models.Model):
    name=models.CharField(max_length=64, unique=True)
    url=models.URLField()
    

    class Meta:
        db_table='labs'

    def __unicode__(self):
        return self.name

class DatabaseSnapshot(models.Model):
    timestamp=models.DateField(auto_now_add=True, unique=True)
    template='media_database.%s.sql.gz'

    class Meta:
        ordering=['timestamp']

    def __unicode__(self):
        import datetime
        return self.template % self.datestr()

    def datestr(self):
        return self.timestamp.strftime('%d%b%Y')

    def datestr_long(self):
        return self.timestamp.strftime('%d %B, %Y')
    def get_absolute_url(self):
        from django.templatetags.static import static
        return static('defined_media/downloads/%s' % self)
