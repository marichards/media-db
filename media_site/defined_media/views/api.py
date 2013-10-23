from rest_framework import generics
from defined_media.models import Organisms
from defined_media.serializers import OrganismSerializer

class OrganismsView(generics.ListAPIView):
    model=Organisms
    serializer_class=OrganismSerializer
