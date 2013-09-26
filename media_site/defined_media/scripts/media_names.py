import os
from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))

init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *
comp144=Compounds.objects.filter(compid=144)[0]
print 'comp144 is %s' % comp144
mednames=comp144.media_names()
print '%d mednames' % len(mednames)
for n in mednames:
    print n

