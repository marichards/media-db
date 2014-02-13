# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Biomass'
        db.create_table(u'biomass', (
            ('biomassid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'biomassID')),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Genus')),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Species')),
            ('sourceid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Sources'], null=True, db_column=u'sourceID', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['Biomass'])

        # Adding model 'BiomassCompounds'
        db.create_table(u'biomass_compounds', (
            ('biocompid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'biocompID')),
            ('biomassid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Biomass'], db_column=u'biomassID')),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Compounds'], db_column=u'compID')),
            ('coefficient', self.gf('django.db.models.fields.FloatField')(null=True, db_column=u'Coefficient', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['BiomassCompounds'])

        # Adding model 'CompoundExceptions'
        db.create_table(u'compound_exceptions', (
            ('pk', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Compounds'], db_column=u'compID')),
            ('keggorgid', self.gf('django.db.models.fields.CharField')(max_length=12L, db_column=u'keggOrgID', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['CompoundExceptions'])

        # Adding model 'CompoundReplacements'
        db.create_table(u'compound_replacements', (
            ('pk', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Compounds'], db_column=u'compID')),
            ('biggid', self.gf('django.db.models.fields.CharField')(max_length=12L, db_column=u'biggID')),
            ('keggorgid', self.gf('django.db.models.fields.CharField')(max_length=12L, db_column=u'keggOrgID', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['CompoundReplacements'])

        # Adding model 'Compounds'
        db.create_table(u'compounds', (
            ('compid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'compID')),
            ('kegg_id', self.gf('django.db.models.fields.CharField')(max_length=255L, unique=True, null=True, db_column=u'KEGG_ID', blank=True)),
            ('bigg_id', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, db_column=u'BiGG_ID', blank=True)),
            ('seed_id', self.gf('django.db.models.fields.CharField')(max_length=45L, db_column=u'seed_id')),
            ('pubchem_ids', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, db_column=u'pubchem_ids', blank=True)),
            ('chebi_ids', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, db_column=u'chebi_ids', blank=True)),
            ('user_identifier', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L)),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['Compounds'])

        # Adding model 'Contributors'
        db.create_table(u'contributors', (
            ('contributorid', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column=u'contributorID')),
            ('last_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_column=u'Last_Name', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['Contributors'])

        # Adding model 'GrowthData'
        db.create_table(u'growth_data', (
            ('growthid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'growthID')),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Contributor'])),
            ('strainid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Organisms'], db_column=u'strainID')),
            ('medid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.MediaNames'], db_column=u'medID')),
            ('sourceid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Sources'], db_column=u'sourceID')),
            ('growth_rate', self.gf('django.db.models.fields.FloatField')(null=True, db_column=u'Growth_Rate', blank=True)),
            ('growth_units', self.gf('django.db.models.fields.CharField')(max_length=45L, db_column=u'Growth_Units', blank=True)),
            ('ph', self.gf('django.db.models.fields.FloatField')(null=True, db_column=u'pH', blank=True)),
            ('temperature_c', self.gf('django.db.models.fields.FloatField')(null=True, db_column=u'Temperature_C', blank=True)),
            ('measureid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Measurements'], null=True, db_column=u'measureID', blank=True)),
            ('additional_notes', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, db_column=u'Additional_Notes', blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'defined_media', ['GrowthData'])

        # Adding model 'Measurements'
        db.create_table(u'measurements', (
            ('measureid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'measureID')),
            ('measurement_technique', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_column=u'Measurement_Technique', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['Measurements'])

        # Adding model 'MediaCompounds'
        db.create_table(u'media_compounds', (
            ('medcompid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'medcompID')),
            ('medid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.MediaNames'], db_column=u'medID')),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Compounds'], db_column=u'compID')),
            ('amount_mm', self.gf('django.db.models.fields.FloatField')(null=True, db_column=u'Amount_mM', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['MediaCompounds'])

        # Adding model 'MediaNames'
        db.create_table(u'media_names', (
            ('medid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'medID')),
            ('media_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_column=u'Media_name')),
            ('is_defined', self.gf('django.db.models.fields.CharField')(max_length=1L, db_column=u'Is_defined', blank=True)),
            ('is_minimal', self.gf('django.db.models.fields.CharField')(max_length=1L, db_column=u'Is_minimal', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['MediaNames'])

        # Adding model 'NamesOfCompounds'
        db.create_table(u'names_of_compounds', (
            ('nameid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'nameID')),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Compounds'], db_column=u'compID')),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_column=u'Name', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['NamesOfCompounds'])

        # Adding model 'Organisms'
        db.create_table(u'organisms', (
            ('strainid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'strainID')),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Genus')),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Species')),
            ('strain', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Strain')),
            ('typeid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.TypesOfOrganisms'], db_column=u'typeID')),
        ))
        db.send_create_signal(u'defined_media', ['Organisms'])

        # Adding model 'OrganismsSources'
        db.create_table(u'organisms_sources', (
            ('strainsourceid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'strainsourceID')),
            ('strainid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Organisms'], null=True, db_column=u'strainID', blank=True)),
            ('sourceid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Sources'], null=True, db_column=u'sourceID', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['OrganismsSources'])

        # Adding model 'Products'
        db.create_table(u'products', (
            ('prodid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'prodID')),
            ('rxntid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Reactants'], db_column=u'rxntID')),
            ('coeff', self.gf('django.db.models.fields.FloatField')()),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Compounds'], db_column=u'compID')),
        ))
        db.send_create_signal(u'defined_media', ['Products'])

        # Adding model 'Reactants'
        db.create_table(u'reactants', (
            ('rxntid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'rxntID')),
            ('compid', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'compound_id', db_column=u'compID', to=orm['defined_media.Compounds'])),
            ('similar_compounds', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'similar_id', null=True, db_column=u'Similar Compounds', to=orm['defined_media.Compounds'])),
        ))
        db.send_create_signal(u'defined_media', ['Reactants'])

        # Adding model 'SecretionUptake'
        db.create_table(u'secretion_uptake', (
            ('secretionuptakeid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'secretionuptakeID')),
            ('growthid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.GrowthData'], db_column=u'growthID')),
            ('compid', self.gf('django.db.models.fields.IntegerField')(null=True, db_column=u'compID', blank=True)),
            ('rate', self.gf('django.db.models.fields.FloatField')(db_column=u'Rate')),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=45L, db_column=u'Units')),
            ('rateid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.SecretionUptakeKey'], db_column=u'rateID')),
        ))
        db.send_create_signal(u'defined_media', ['SecretionUptake'])

        # Adding model 'SecretionUptakeKey'
        db.create_table(u'secretion_uptake_key', (
            ('rateid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'rateID')),
            ('rate_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=45L, db_column=u'Rate_Type', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['SecretionUptakeKey'])

        # Adding model 'SecretionUptakeUnit'
        db.create_table(u'secretion_uptake_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
        ))
        db.send_create_signal(u'defined_media', ['SecretionUptakeUnit'])

        # Adding model 'Sources'
        db.create_table(u'sources', (
            ('sourceid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'sourceID')),
            ('first_author', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'First_Author', blank=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Journal', blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4L, db_column=u'Year', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_column=u'Title', blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255L, db_column=u'Link', blank=True)),
            ('pubmed_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['Sources'])

        # Adding unique constraint on 'Sources', fields ['first_author', 'journal', 'title']
        db.create_unique(u'sources', [u'First_Author', u'Journal', u'Title'])

        # Adding model 'TypesOfOrganisms'
        db.create_table(u'types_of_organisms', (
            ('typeid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column=u'typeID')),
            ('organism_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255L, db_column=u'Organism_type', blank=True)),
        ))
        db.send_create_signal(u'defined_media', ['TypesOfOrganisms'])

        # Adding model 'SearchResult'
        db.create_table(u'search_results', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('obj_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'defined_media', ['SearchResult'])

        # Adding model 'Contributor'
        db.create_table(u'contributor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['defined_media.Lab'])),
        ))
        db.send_create_signal(u'defined_media', ['Contributor'])

        # Adding model 'Lab'
        db.create_table(u'labs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'defined_media', ['Lab'])


    def backwards(self, orm):
        # Removing unique constraint on 'Sources', fields ['first_author', 'journal', 'title']
        db.delete_unique(u'sources', [u'First_Author', u'Journal', u'Title'])

        # Deleting model 'Biomass'
        db.delete_table(u'biomass')

        # Deleting model 'BiomassCompounds'
        db.delete_table(u'biomass_compounds')

        # Deleting model 'CompoundExceptions'
        db.delete_table(u'compound_exceptions')

        # Deleting model 'CompoundReplacements'
        db.delete_table(u'compound_replacements')

        # Deleting model 'Compounds'
        db.delete_table(u'compounds')

        # Deleting model 'Contributors'
        db.delete_table(u'contributors')

        # Deleting model 'GrowthData'
        db.delete_table(u'growth_data')

        # Deleting model 'Measurements'
        db.delete_table(u'measurements')

        # Deleting model 'MediaCompounds'
        db.delete_table(u'media_compounds')

        # Deleting model 'MediaNames'
        db.delete_table(u'media_names')

        # Deleting model 'NamesOfCompounds'
        db.delete_table(u'names_of_compounds')

        # Deleting model 'Organisms'
        db.delete_table(u'organisms')

        # Deleting model 'OrganismsSources'
        db.delete_table(u'organisms_sources')

        # Deleting model 'Products'
        db.delete_table(u'products')

        # Deleting model 'Reactants'
        db.delete_table(u'reactants')

        # Deleting model 'SecretionUptake'
        db.delete_table(u'secretion_uptake')

        # Deleting model 'SecretionUptakeKey'
        db.delete_table(u'secretion_uptake_key')

        # Deleting model 'SecretionUptakeUnit'
        db.delete_table(u'secretion_uptake_unit')

        # Deleting model 'Sources'
        db.delete_table(u'sources')

        # Deleting model 'TypesOfOrganisms'
        db.delete_table(u'types_of_organisms')

        # Deleting model 'SearchResult'
        db.delete_table(u'search_results')

        # Deleting model 'Contributor'
        db.delete_table(u'contributor')

        # Deleting model 'Lab'
        db.delete_table(u'labs')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'defined_media.biomass': {
            'Meta': {'object_name': 'Biomass', 'db_table': "u'biomass'"},
            'biomassid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'biomassID'"}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Genus'"}),
            'sourceid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Sources']", 'null': 'True', 'db_column': "u'sourceID'", 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Species'"})
        },
        u'defined_media.biomasscompounds': {
            'Meta': {'object_name': 'BiomassCompounds', 'db_table': "u'biomass_compounds'"},
            'biocompid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'biocompID'"}),
            'biomassid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Biomass']", 'db_column': "u'biomassID'"}),
            'coefficient': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "u'Coefficient'", 'blank': 'True'}),
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Compounds']", 'db_column': "u'compID'"})
        },
        u'defined_media.compoundexceptions': {
            'Meta': {'object_name': 'CompoundExceptions', 'db_table': "u'compound_exceptions'"},
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Compounds']", 'db_column': "u'compID'"}),
            'keggorgid': ('django.db.models.fields.CharField', [], {'max_length': '12L', 'db_column': "u'keggOrgID'", 'blank': 'True'}),
            'pk': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'defined_media.compoundreplacements': {
            'Meta': {'object_name': 'CompoundReplacements', 'db_table': "u'compound_replacements'"},
            'biggid': ('django.db.models.fields.CharField', [], {'max_length': '12L', 'db_column': "u'biggID'"}),
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Compounds']", 'db_column': "u'compID'"}),
            'keggorgid': ('django.db.models.fields.CharField', [], {'max_length': '12L', 'db_column': "u'keggOrgID'", 'blank': 'True'}),
            'pk': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'defined_media.compounds': {
            'Meta': {'object_name': 'Compounds', 'db_table': "u'compounds'"},
            'bigg_id': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'db_column': "u'BiGG_ID'", 'blank': 'True'}),
            'chebi_ids': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'db_column': "u'chebi_ids'", 'blank': 'True'}),
            'compid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'compID'"}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'blank': 'True'}),
            'kegg_id': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'unique': 'True', 'null': 'True', 'db_column': "u'KEGG_ID'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L'}),
            'pubchem_ids': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'db_column': "u'pubchem_ids'", 'blank': 'True'}),
            'seed_id': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'db_column': "u'seed_id'"}),
            'user_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'blank': 'True'})
        },
        u'defined_media.contributor': {
            'Meta': {'object_name': 'Contributor', 'db_table': "u'contributor'"},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Lab']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'defined_media.contributors': {
            'Meta': {'object_name': 'Contributors', 'db_table': "u'contributors'"},
            'contributorid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "u'contributorID'"}),
            'last_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_column': "u'Last_Name'", 'blank': 'True'})
        },
        u'defined_media.growthdata': {
            'Meta': {'object_name': 'GrowthData', 'db_table': "u'growth_data'"},
            'additional_notes': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'db_column': "u'Additional_Notes'", 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Contributor']"}),
            'growth_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "u'Growth_Rate'", 'blank': 'True'}),
            'growth_units': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'db_column': "u'Growth_Units'", 'blank': 'True'}),
            'growthid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'growthID'"}),
            'measureid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Measurements']", 'null': 'True', 'db_column': "u'measureID'", 'blank': 'True'}),
            'medid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.MediaNames']", 'db_column': "u'medID'"}),
            'ph': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "u'pH'", 'blank': 'True'}),
            'sourceid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Sources']", 'db_column': "u'sourceID'"}),
            'strainid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Organisms']", 'db_column': "u'strainID'"}),
            'temperature_c': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "u'Temperature_C'", 'blank': 'True'})
        },
        u'defined_media.lab': {
            'Meta': {'object_name': 'Lab', 'db_table': "u'labs'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'defined_media.measurements': {
            'Meta': {'object_name': 'Measurements', 'db_table': "u'measurements'"},
            'measureid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'measureID'"}),
            'measurement_technique': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_column': "u'Measurement_Technique'", 'blank': 'True'})
        },
        u'defined_media.mediacompounds': {
            'Meta': {'object_name': 'MediaCompounds', 'db_table': "u'media_compounds'"},
            'amount_mm': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "u'Amount_mM'", 'blank': 'True'}),
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Compounds']", 'db_column': "u'compID'"}),
            'medcompid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'medcompID'"}),
            'medid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.MediaNames']", 'db_column': "u'medID'"})
        },
        u'defined_media.medianames': {
            'Meta': {'ordering': "[u'media_name']", 'object_name': 'MediaNames', 'db_table': "u'media_names'"},
            'is_defined': ('django.db.models.fields.CharField', [], {'max_length': '1L', 'db_column': "u'Is_defined'", 'blank': 'True'}),
            'is_minimal': ('django.db.models.fields.CharField', [], {'max_length': '1L', 'db_column': "u'Is_minimal'", 'blank': 'True'}),
            'media_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_column': "u'Media_name'"}),
            'medid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'medID'"})
        },
        u'defined_media.namesofcompounds': {
            'Meta': {'object_name': 'NamesOfCompounds', 'db_table': "u'names_of_compounds'"},
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Compounds']", 'db_column': "u'compID'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_column': "u'Name'", 'blank': 'True'}),
            'nameid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'nameID'"})
        },
        u'defined_media.organisms': {
            'Meta': {'ordering': "[u'genus', u'species', u'strain']", 'object_name': 'Organisms', 'db_table': "u'organisms'"},
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Genus'"}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Species'"}),
            'strain': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Strain'"}),
            'strainid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'strainID'"}),
            'typeid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.TypesOfOrganisms']", 'db_column': "u'typeID'"})
        },
        u'defined_media.organismssources': {
            'Meta': {'object_name': 'OrganismsSources', 'db_table': "u'organisms_sources'"},
            'sourceid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Sources']", 'null': 'True', 'db_column': "u'sourceID'", 'blank': 'True'}),
            'strainid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Organisms']", 'null': 'True', 'db_column': "u'strainID'", 'blank': 'True'}),
            'strainsourceid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'strainsourceID'"})
        },
        u'defined_media.products': {
            'Meta': {'object_name': 'Products', 'db_table': "u'products'"},
            'coeff': ('django.db.models.fields.FloatField', [], {}),
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Compounds']", 'db_column': "u'compID'"}),
            'prodid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'prodID'"}),
            'rxntid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.Reactants']", 'db_column': "u'rxntID'"})
        },
        u'defined_media.reactants': {
            'Meta': {'object_name': 'Reactants', 'db_table': "u'reactants'"},
            'compid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'compound_id'", 'db_column': "u'compID'", 'to': u"orm['defined_media.Compounds']"}),
            'rxntid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'rxntID'"}),
            'similar_compounds': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'similar_id'", 'null': 'True', 'db_column': "u'Similar Compounds'", 'to': u"orm['defined_media.Compounds']"})
        },
        u'defined_media.searchresult': {
            'Meta': {'object_name': 'SearchResult', 'db_table': "u'search_results'"},
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'obj_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'defined_media.secretionuptake': {
            'Meta': {'object_name': 'SecretionUptake', 'db_table': "u'secretion_uptake'"},
            'compid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'compID'", 'blank': 'True'}),
            'growthid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.GrowthData']", 'db_column': "u'growthID'"}),
            'rate': ('django.db.models.fields.FloatField', [], {'db_column': "u'Rate'"}),
            'rateid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['defined_media.SecretionUptakeKey']", 'db_column': "u'rateID'"}),
            'secretionuptakeid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'secretionuptakeID'"}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '45L', 'db_column': "u'Units'"})
        },
        u'defined_media.secretionuptakekey': {
            'Meta': {'object_name': 'SecretionUptakeKey', 'db_table': "u'secretion_uptake_key'"},
            'rate_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45L', 'db_column': "u'Rate_Type'", 'blank': 'True'}),
            'rateid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'rateID'"})
        },
        u'defined_media.secretionuptakeunit': {
            'Meta': {'object_name': 'SecretionUptakeUnit', 'db_table': "u'secretion_uptake_unit'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'})
        },
        u'defined_media.sources': {
            'Meta': {'ordering': "[u'first_author', u'title']", 'unique_together': "([u'first_author', u'journal', u'title'],)", 'object_name': 'Sources', 'db_table': "u'sources'"},
            'first_author': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'First_Author'", 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Journal'", 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'db_column': "u'Link'", 'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sourceid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'sourceID'"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_column': "u'Title'", 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4L', 'db_column': "u'Year'", 'blank': 'True'})
        },
        u'defined_media.typesoforganisms': {
            'Meta': {'object_name': 'TypesOfOrganisms', 'db_table': "u'types_of_organisms'"},
            'organism_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255L', 'db_column': "u'Organism_type'", 'blank': 'True'}),
            'typeid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'typeID'"})
        }
    }

    complete_apps = ['defined_media']