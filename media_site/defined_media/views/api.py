from rest_framework import generics
from defined_media.models import Organisms
from defined_media.serializers import OrganismSerializer

class OrganismsView(generics.ListAPIView):
    model=Organisms
    serializer_class=OrganismSerializer
    
    def get_queryset(self):
        args={}
        for arg in ['genus', 'species', 'strain']:
            if arg in self.kwargs:
                args[arg]=self.kwargs[arg]
        orgs=Organisms.objects.filter(**args)

        return orgs
