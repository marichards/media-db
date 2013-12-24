import os, argparse, sys, csv, re
from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django
from defined_media.models import *


parser=argparse.ArgumentParser()
parser.add_argument('source_pubmed_fn', default='source_pubmed.txt')
parser.add_argument('-v', action='store_true')

opts=parser.parse_args()
if opts.v: print 'opts: %s' % opts

r=re.compile('^\d+$')
stats={
    'n_srcs':0,
    'n_missing_pubmed':0,
    'n_src_not_found':0,
    'n_saved':0,
}

with open(opts.source_pubmed_fn) as f:
    reader=csv.reader(f, delimiter='\t')
    for row in reader:
        (sourceid, pubmed_id)=row

        if not re.search(r, sourceid) and not re.search(r, pubmed_id):
            continue

        if not re.search(r, pubmed_id):
            stats['n_missing_pubmed']+=1
            continue
            
        try:
            src=Sources.objects.get(sourceid=sourceid)
            stats['n_srcs']+=1
        except Sources.DoesNotExist:
            if opts.v:
                print 'no Sources for sourceid=%s' % sourceid
            stats['n_src_not_found']+=1
            continue

        try:
            src.pubmed_id=pubmed_id
            print '%r' % src
            src.save()
            stats['n_saved']+=1
            print 'saved %s' % src
        except Exception as e:
            print 'caught %s: %s' % (type(e), e)


for k,v in stats.items():
    print '%s: %s' % (k,v)
