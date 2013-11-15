from rest_framework import serializers
from defined_media.models import Organisms, GrowthData

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organisms

class GrowthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=GrowthData

