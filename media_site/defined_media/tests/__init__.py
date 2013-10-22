from models import *
from search import *
from cPickle import load 
import os

def setup_old():
    reuse_db=os.environ['REUSE_DB'] if 'REUSE_DB' in os.environ else None # was printing this out, no longer
    fixture_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixture.pk'))
    print 'using fixtures in %s' % fixture_fn

    stats={}
    def add_stat(key):
        try:             stats[key]+=1
        except KeyError: stats[key]=1

    with open(fixture_fn) as f:
        media_objs=load(f)
#        print 'tests: %d media_objs' % len(media_objs)
        for obj in media_objs:
            obj.save()
            add_stat(obj.__class__.__name__)

#    for k,v in stats.items():
#        print '%s: %d' % (k,v)

def teardown():
    pass
