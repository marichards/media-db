from django.contrib import admin
from defined_media.models import Biomass, BiomassCompounds, Compounds , GrowthData, MediaNames,Organisms, Sources 

#Inline things
#class BiomassCompoundsInline(admin.TabularInline):
#	model = BiomassCompounds

class BiomassAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['genus','species']}),
		('Source', {'fields': ['sourceid']}),
	]
	readonly_fields=('biomassid',)
#	inlines = BiomassCompoundsInline

admin.site.register(Biomass,BiomassAdmin)

class CompoundsAdmin(admin.ModelAdmin):
	fieldsets = [
		('Identifiers',{'fields': ['kegg_id','bigg_id']}),
	]

admin.site.register(Compounds,CompoundsAdmin)

'''
class ContributorsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['last_name']}),
	]

admin.site.register(Contributors,ContributorsAdmin)
'''

class GrowthDataAdmin(admin.ModelAdmin):
	fieldsets = [
		('Condition Information',{'fields': ['growthid','strainid','medid','sourceid']}),
		('Measurement Information',{'fields': ['growth_rate','growth_units','ph','temperature_c','measureid']}),
		(None, {'fields': ['additional_notes']}),
	]
	readonly_fields=('growthid',)

admin.site.register(GrowthData,GrowthDataAdmin)

class MediaNamesAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['media_name']}),
		('Is Minimal?', {'fields': ['is_minimal']}),
	]

admin.site.register(MediaNames,MediaNamesAdmin)

class OrganismsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['genus','species','strain']}),
	]
	search_fields = ['genus','species','strain']
admin.site.register(Organisms,OrganismsAdmin)

class SourcesAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['first_author','journal','year','title','link']}),
	]

admin.site.register(Sources,SourcesAdmin)


