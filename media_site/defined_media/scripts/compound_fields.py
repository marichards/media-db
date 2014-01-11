import os, argparse, sys, csv, re
from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django
from defined_media.models import *

'''
Usage: py compounds_fields.py <in_fn> <field1> <field2> [-v] [-n] [-flip]

'''


parser=argparse.ArgumentParser()
parser.add_argument('in_fn')
parser.add_argument('field1')
parser.add_argument('field2')
parser.add_argument('-v', action='store_true')
parser.add_argument('-n', action='store_true')
parser.add_argument('-flip', action='store_true')
opts=parser.parse_args()
if opts.v: print 'opts: %s' % opts

def flip(v1,v2):
    tmp=v1
    v1=v2
    v2=tmp
    return (v1,v2)


f2re={'seed_id': r'^cpd\d+$',
      'kegg_id': r'^C\d+$',
      'chebi_id': r'^\d+$',
      'pubchem_id': r'^\d+$'}

f1=opts.field1
f2=opts.field2
if opts.flip:
    (f1,f2)=flip(f1,f2)
f12f2={}
stats={1:0, 2:0, 3:0, 'n_comps':0, 'n_missing':0}
stats['bad_'+f1]=0
stats['bad_'+f2]=0

with open(opts.in_fn) as f:
    reader=csv.reader(f, delimiter='\t')
    for row in reader:
        v1,v2=row
        if opts.flip:
            (v1,v2)=flip(v1,v2)

        # look up f1:
        if f1 in f2re:
            if not re.search(f2re[f1], v1):
                stats['bad_'+f1]+=1
                if opts.v:
                    print 'bad %s: %s' % (f1, v1)
                continue
        # look up f2
        if f2 in f2re:
            if not re.search(f2re[f2], v2):
                stats['bad_'+f2]+=1
                if opts.v:
                    print 'bad %s: %s' % (f2, v2)
                continue

        # add to f2 to f1's list:
        try:
            f12f2[v1].append(v2)
        except KeyError:
            f12f2[v1]=[v2]

# look up compounds based on f1, update object with csv(f2):
for v1,v2l in f12f2.items():
    args={f1:v1}
    try:
        comp=Compounds.objects.get(**args)
    except Compounds.DoesNotExist:
        if opts.v: print 'no compound for %s=%s' % (f1, v1)
        stats['n_missing']+=1
        continue

    v2s=','.join(v2l)
    setattr(comp, f2, ','.join(v2l))
    if opts.v:
        print 'about to save %s (%s=%s): set %s to %s' % (comp, f1, v1, f2, v2s)
    if not opts.n: 
        comp.save()
    stats['n_comps']+=1

    # make note of large n:n r'ships:
    n=len(v2l)
    if n>4:
        print 'big_n=%d, v1=%s, v2l=%s' % (n, v1, v2l)
    try:
        stats[n]+=1
    except KeyError:
        stats[n]=1

# report stats:
for n in sorted(stats.keys()):
    print '%s: %s' % (n, stats[n])
