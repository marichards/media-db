from models import *
from search import *
from cPickle import load 
import os, sys
from defined_media.models import *

def setup():
    pass

def setup1():
    reuse_db=os.environ['REUSE_DB'] if 'REUSE_DB' in os.environ else None # was printing this out, no longer
    fixture_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixture.pk'))
    print 'using fixtures in %s' % fixture_fn

    stats={}
    def add_stat(key):
        try:             stats[key]+=1
        except KeyError: stats[key]=1

    with open(fixture_fn) as f:
        media_objs=load(f)
        print 'tests: %d media_objs' % len(media_objs)

    classes=[Compounds, NamesOfCompounds, Products]
    classes=[Compounds, MediaCompounds]

    for obj in media_objs:
        try:
            add_stat(obj.__class__.__name__)
            if obj.__class__ not in classes: 
                continue
            print 'attempting to save %r' % obj
            obj.save()
        except Exception, e:
            print 'caught %s: %s' % (type(e), e)
            add_stat('error: '+obj.__class__.__name__)

    for k in sorted(stats.keys()):
        v=stats[k]
        print 'tests.__init__: %s: %d' % (k,v)
    print 

def teardown():
    pass
