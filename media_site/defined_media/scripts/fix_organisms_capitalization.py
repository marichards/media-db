import os, argparse, sys

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *

parser=argparse.ArgumentParser()
parser.add_argument('classname')
parser.add_argument('field')
args=parser.parse_args()

try:
    classname=args.classname
    cls=globals()[classname]
except KeyError:
    print 'Unknown class "%s"' % classname
    sys.exit(1)

stats={'n_objs':0}

field=args.field
for obj in cls.objects.all():
    attr=getattr(obj, field).capitalize()
    setattr(obj, field, attr)
    obj.save()
    stats['n_objs']+=1

print stats

