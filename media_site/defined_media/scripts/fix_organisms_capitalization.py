import os

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import Organisms

for org in Organisms.objects.all():
    org.genus=org.genus.capitalize()
    print org.genus
    org.save()


