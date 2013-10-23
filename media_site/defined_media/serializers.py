from rest_framework import serializers
from defined_media.models import Organisms

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organisms
