'''
Add Kegg formula to compounds.
Sample input: keggcompounds.txt
'''
import sys, os, argparse
from keggcompounds_parser import KeggCompoundsParser

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django
from defined_media.models import *

def args():
    parser=argparse.ArgumentParser()
    parser.add_argument('kegg_fn')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('-n', action='store_true', dest='dry_run')
    args=parser.parse_args()
    return args

def main(args):
    stats={'n_missing_compound': 0,
           'n_formulas': 0,
           'n_skipped': 0,
           'n_duplicates': 0,
           'n_overwritten': 0,
           'n_new': 0,
           }
    parser=KeggCompoundsParser(args.kegg_fn)
    for kegg_id, formula in parser.next():
        if args.v:
            print 'kegg_id %s: %s' % (kegg_id, formula)
        try:
            comp=Compounds.objects.get(kegg_id=kegg_id)
        except Compounds.DoesNotExist:
            stats['n_missing_compound']+=1
            continue

        if args.v:
            print '%s: formula=%s' % (comp, formula)

        if comp.formula:
            if comp.formula==formula:
                stats['n_duplicates']+=1
                continue
            else:
                stats['n_overwritten']+=1
        else:
            stats['n_new']+=1

        comp.formula=formula
        if not args.dry_run:
            comp.save()
            stats['n_formulas']+=1
        else:
            stats['n_skipped']+=1
        
    report(stats)
    return 0

def report(stats):
    for k in sorted(stats.keys()):
        print '%s: %d' % (k, stats[k])

if __name__=='__main__':
    sys.exit(main(args()))
