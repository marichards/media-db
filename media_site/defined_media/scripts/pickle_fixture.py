import os, cPickle, shutil, sys

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *
from django.core import serializers

attrs=[a for a in dir(Compounds) if a.endswith('_set')]
attrs.remove('seedcompounds_set')




def all_related(obj, related={}):
    n=0
    manager_names=[a for a in dir(obj) if a.endswith('_set')]
    if 'seedcompounds_set' in manager_names: 
        manager_names.remove('seedcompounds_set')
    if 'products_set' in manager_names:
        manager_names.remove('products_set')

#    print '%s: %s' % (type(obj), manager_names)
    
    for mn in manager_names:
        manager=getattr(obj, mn)
        objs=manager.all()
        n+=len(objs)
#        print '%s: %d objs' % (mn, n)
        if len(objs)==0:
            continue
        classname=objs[0].__class__.__name__
        related[classname]=objs

        for o in objs:
            all_related(o, related)
    return (related, n)

def add_secretion_uptakes(media_objs):
    growth_ids=[254, 265, 210]  # one for each unit type
    sec_uptakes=[]
    for gid in growth_ids:
        sec_uptakes.extend(list(SecretionUptake.objects.filter(growthid=gid)))
    media_objs['SecretionUptake']=sec_uptakes

def add_secretion_uptake_keys(media_objs):
    media_objs['SecretionUptakeKey']=SecretionUptakeKey.objects.all()
    

def add_biomass(media_objs):
    all_biomass=Biomass.objects.all()
    media_objs['Biomass']=all_biomass
    source_ids=[x.sourceid_id for x in all_biomass]
    sources=[Sources.objects.get(sourceid=id) for id in source_ids]
    media_objs['Sources']=sources
        

def add_organisms(media_objs):
    ''' add, I dunno, 25 organisms to the fixture: '''
    orgs=Organisms.objects.all()[:25]
    media_objs['Organisms']=orgs
    media_objs['TypesOfOrganisms']=TypesOfOrganisms.objects.all() # all 3 of them
        
def add_search_results(media_objs):
    media_objs['SearchResult']=SearchResult.objects.filter(keyword='Acinetobacter')
    

def add_media_names(media_objs, compounds):
    mednames=set()
    for comp in compounds:
        for mc in comp.mediacompounds_set.all():
            mednames.add(mc.medid)
    media_objs['MediaNames']=list(mednames)

def add_reactants(media_objs):
    reactants=set()
    for p in media_objs['Products']:
        reactants.add(p.rxntid)
    media_objs['Reactants']=list(reactants)


def main():
    n=50

    stats={}
    def add_stat(k,v):
        try: stats[k]+=v
        except KeyError: stats[k]=v


    # calc all_related for all compounds:
    compounds=Compounds.objects.all()[:n]
    print 'n=%d, len(compounds)=%d' % (n, len(compounds))

    print 'calculating all_related() for compounds...'
    media_objs={'Compounds':set()}
    bad_compounds=[]
    for c in compounds:
        c.n_related=0
        media_objs['Compounds'].add(c)
        try:
            (related,n)=all_related(c)
        except Exception, e:
            bad_compounds.append(c)
            continue

        c.related=related
        c.n_related=n
#        print '%s: %d related objects' % (c, c.n_related)
        for classname,objs in related.items():
            try:
                media_objs[classname].update(set(objs))
            except KeyError:
                print 'new set: %s' % classname
                media_objs[classname]=set(objs)
#            print '%s: added %d objs, total=%d' % (classname, len(objs), len(media_objs[classname]))


    print 'sorting compounds...'
    compounds=sorted(compounds, key=lambda c: c.n_related)
    print 'done sorting'

    add_secretion_uptakes(media_objs)
    add_secretion_uptake_keys(media_objs)
    add_biomass(media_objs)
    add_organisms(media_objs)
    add_search_results(media_objs)
    add_media_names(media_objs, compounds)
#    add_reactants(media_objs)

    write_fixture(media_objs)
    report(media_objs, bad_compounds)

def report(media_objs, bad_compounds):
    print
    for k in sorted(media_objs.keys()):
        v=media_objs[k]
        print '%s: %d' % (k,len(v))
    print '%d bad compounds' % len(bad_compounds)

def write_fixture(media_objs):
    json_fn='fixture.json'
    pk_fn='fixture.pk'

    l=[]
    for k,v in media_objs.items():
        l.extend(list(v))

    with open(json_fn, 'w') as f:
        f.write(serializers.serialize('json', l, indent=4))
        print '%s written' % json_fn

    json_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', json_fn))
    with open(json_fn, 'w') as f:
        f.write(serializers.serialize('json', l, indent=4))
        print '%s written' % json_fn

    with open(pk_fn, 'w') as f:
        cPickle.dump(l, f)
        print '%s written' % pk_fn

    dest_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', pk_fn))
    with open(dest_fn, 'w') as f:
        cPickle.dump(l, f)
        print '%s written' % dest_fn



if __name__=='__main__':
    main()
