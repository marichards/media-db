import os, argparse, sys, csv, re
from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django
from defined_media.models import *

'''
Usage: py compounds_fields.py <in_fn> <lookup_field> <novel_field> [-v] [-n] 

Add data columns to the compounds table:

Parse a csv (or tsv); for each line,
extract a lookup value
extract a data value (to add to table), add to list
for both values, verify integrity via a regex

for lookup, values in parsed_data.items():
  lookup Compound, modify according to values, and save
  

Inputs:
- filename
- lookup fieldname, column number
- novel fieldname, column numer
- regexes for each type of field value (currently hardcoded)
'''


def get_fs():
    ''' return the list of field names as obtained from the first line of the file '''
    with open(opts.in_fn) as f:
        line1=f.readline()
        print 'line1 is %s' % line1
        fs=[x.strip() for x in re.split(r'\s+', line1)]
        print 'fs is %s' % fs
        if fs[0].startswith('#'):
            del fs[0]
            print 'fs is %s' % fs
        return fs

def verify(f,v):
    reg=re.compile(f2re[f])
    if re.search(reg, v):
        return True
    else:
        stats['bad_'+f]+=1
        if opts.v:
            print 'bad %s: "%s"' % (f, v)
        return False


def parse_file(lu_idx, val_idx):
    '''
    build f12f2 s.t. k=lookup key, v=associated value
    '''
    f12f2={}
    with open(opts.in_fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for row in reader:
            if row[0].startswith('#'):
                continue

            lu_val=row[lu_idx].strip()
            val=row[val_idx].strip()
            if not verify(opts.lookup, lu_val): continue
            if not verify(opts.novel, val): continue

            try:
                f12f2[lu_val].append(val)
            except KeyError:
                f12f2[lu_val]=[val]
            if opts.v:
                print '%s: %s' % (lu_val, f12f2[lu_val])
    return f12f2

def update_compounds(f12f2):
    for lu,nv in f12f2.items():
        # lookup compound:
        args={opts.lookup: lu}
        try:
            comp=Compounds.objects.get(**args)
        except Compounds.DoesNotExist:
            if opts.v: print 'no compound for %s=%s' % (opts.lookup, lu)
            stats['n_missing']+=1
            continue

        # store comma-separated list of values to compound:
        nvs=','.join(nv)
        setattr(comp, opts.novel, nvs)
        if opts.v:
            print 'about to save %r (%s=%s): set %s to %s' % (comp, opts.lookup, lu, opts.novel, nvs)
        if not opts.n: 
            comp.save()
        stats['n_comps']+=1

        # compile stats "histogram":
        n=len(nv)
        try:
            stats[n]+=1
        except KeyError:
            stats[n]=1

def report(stats):
    for n in sorted(stats.keys()):
        print '%s: %s' % (n, stats[n])


def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('in_fn')
    parser.add_argument('lookup')
    parser.add_argument('novel')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('-n', action='store_true')

    opts=parser.parse_args()
    opts.lookup=opts.lookup.lower()
    opts.novel=opts.novel.lower()
    return opts, parser


if __name__=='__main__':
    opts,parser=get_args()
    if opts.v: print 'opts: %s' % opts
    
    f2re={
        'compid': r'^\d+$',
        'seed_id': r'^cpd\d+$',
        'kegg_id': r'^C\d+$',
        'chebi_id': r'^\d+$',
        'pubchem_ids': r'^\d+$',
        'formula': r'^[()\w]+$',
        }

    try:
        fields=get_fs()         # can throw
        for i,f in enumerate([f.lower() for f in fields]):
            if f==opts.lookup:
                lookup_f=f.lower()
                lookup_idx=i
            elif f==opts.novel:
                novel_f=f.lower()
                novel_idx=i
    except RuntimeError as e:
        print str(e)
        parser.print_help()
        sys.exit(1)


    # verify existence of lookup_f and novel_f:
    try:
        s='lookup: %s\tnovel: %s' % (lookup_f, novel_f)
    except NameError:
        print 'missing field args (lookup or novel)'
        parser.print_help()
        sys.exit(1)
            

    stats={1:0, 2:0, 3:0, 'n_comps':0, 'n_missing':0}
    stats['bad_'+lookup_f]=0
    stats['bad_'+novel_f]=0

    f12f2=parse_file(lookup_idx, novel_idx)
    update_compounds(f12f2)
    report(stats)
