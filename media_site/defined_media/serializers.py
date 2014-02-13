from rest_framework import serializers
from defined_media.models import Organisms, GrowthData, Sources, MediaNames

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organisms

class SourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sources

class MediaNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model=MediaNames

class GrowthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=GrowthData

