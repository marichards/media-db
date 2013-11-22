import os, sys

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *

stats={'n_comps': Compounds.objects.count(), 
       'n_saved':0,
       'n_errors':0,
       }

n=0
for sc in SeedCompounds.objects.all():
    try:
        comp=Compounds.objects.get(kegg_id=sc.kegg_id)
        comp.seed_id=sc.seed_id
        comp.save()
        stats['n_saved']+=1
    except Exception as e:
        print 'caught %s: %s' % (type(e), e)
        stats['n_errors']+=1

    n+=1
    if n % 500 == 0:
        print '%d...' % n

for k,v in stats.items():
    print '%s: %s' % (k,v)
