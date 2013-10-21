import os, cPickle, shutil, sys

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *

attrs=[a for a in dir(Compounds) if a.endswith('_set')]
attrs.remove('seedcompounds_set')

def n_related(self):
    try: return self._n_related
    except AttributeError: 
        import pdb
#        pdb.set_trace()
        n=0
        for attr in attrs:
            other_getter=getattr(self, attr)
#            print '%s: %s' % (self, attr)
            l=list(other_getter.all())
            n+=len(l)
                
        return n

Compounds.n_related=n_related

def main():
    n=50
    compounds=Compounds.objects.all()[:n]
    print 'n=%d, len(compounds)=%d' % (n, len(compounds))

    print 'calculating n_related() for compounds...'
    for c in compounds:
         try:
            c.n_related()
#            print '%s: n_related=%d' % (c, c.n_related())
         except Exception, e:
            print 'compound %s: caught %s' % (c, e)


    print 'sorting compounds...'
    compounds=sorted(compounds, key=n_related)
    print 'done sorting'

    stats={}
    def add_stat(k,v):
        try: stats[k]+=v
        except KeyError: stats[k]=v

    media_objs=[]
    for c in compounds[-20:]:   # last 20 compounds, sorted by n_related()
        print '%s: %d others' % (c, c.n_related())
        media_objs.append(c)
        add_stat('Compounds', 1)

        for a in attrs:
            objs=getattr(c,a).all()
#            print '%d objects in %s' % (len(objs), a)
#            print '%d objects in %s for compound %s' % (len(objs), a, c.compid)
            if len(objs)==0: continue
            media_objs.extend(objs)
            k=objs[0].__class__.__name__
            add_stat(k,len(objs))

    print
    for k,v in stats.items():
        print '%s: %d' % (k,v)

    out_fn='fixture.pk'
    with open(out_fn, 'w') as f:
        cPickle.dump(media_objs, f)
        print '%s written' % out_fn

    dest_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests', out_fn))
    with open(dest_fn, 'w') as f:
        cPickle.dump(media_objs, f)
        print '%s written' % dest_fn


if __name__=='__main__':
    main()
