import os, sys

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *

stats={'n_comps': Compounds.objects.count(), 
       'n_no_name':0}

for comp in Compounds.objects.all():
    try:
        names=list(comp.keywords())
        comp.name=names[0]
        NamesOfCompounds.objects.get(compid=comp.compid, name=comp.name).delete()
    except IndexError, e:
        comp.name=str(comp.compid)
        print '%s: no name, using compid' % comp
        stats['n_no_name']+=1

    except Exception, e:
        print 'caught %s: %s' % (type(e), e)
        print 'possible cause: nothing matches compid=%d, name=%s' % (comp.compid, comp.name)

    finally:
        comp.save()



for k,v in stats.items():
    print '%s: %s' % (k,v)
