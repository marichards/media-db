import os, cPickle, shutil, sys

from django_env import init_django_env
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
init_django_env(root_dir, 'media_site', 'defined_media')
import django

from defined_media.models import *
from django.core import serializers
from django.contrib.auth.models import User

def add_contributors(media_objs):
    media_objs['Contributor']=[]
    for con in Contributor.objects.all(): 
        media_objs['Contributor'].append(con)

def add_100_compounds_with_formulas(media_objs):

    c100s=list([c for c in Compounds.objects.exclude(formula__isnull=True)[:100]])
    try:
        media_objs['Compounds'].extend(c100s)
    except KeyError:
        media_objs['Compounds']=c100s
        


def add_growth_data(media_objs):
    growth_ids=[254, 265, 210, 258]  # one for each unit type, and one that is ref'd by a sec-uptake
    gd_objs=set()
    bad_gds=[]
    attrs=['strainid', 'medid', 'sourceid', 'measureid']
    for gid in growth_ids:
        gd=GrowthData.objects.get(growthid=gid)
        gd_objs.add(gd)
        add_related(gd, media_objs)

        for attr in attrs:
            a=getattr(gd, attr)
            if a: 
                print 'gd %d: adding %s: %s' % (gid, attr, a)
                add_obj(a, media_objs)
                if attr=='medid':
                    add_related(a, media_objs, True)

    media_objs['GrowthData']=gd_objs

def add_secretion_uptakes(media_objs):
    growth_ids=[254, 265, 210]  # one for each unit type
    sec_uptakes=set()
    for gid in growth_ids:
        sec_uptakes.update(set(SecretionUptake.objects.filter(growthid=gid)))
    media_objs['SecretionUptake']=sec_uptakes

    for su in sec_uptakes:
        add_related(su, media_objs, debug=True)
        comp=Compounds.objects.get(compid=su.compid)
        if comp: add_obj(comp, media_objs)

def add_secretion_uptake_keys(media_objs):
    media_objs['SecretionUptakeKey']=set(SecretionUptakeKey.objects.all())
    

def add_biomass(media_objs):
    all_biomass=Biomass.objects.all()
    media_objs['Biomass']=set(all_biomass)
    source_ids=[x.sourceid_id for x in all_biomass]
    sources=[Sources.objects.get(sourceid=id) for id in source_ids]
    media_objs['Sources']=set(sources)
        

def add_organisms(media_objs):
    ''' add, I dunno, 25 organisms to the fixture: '''
    media_objs['Organisms']=set(Organisms.objects.all()[:25])
    media_objs['TypesOfOrganisms']=set(TypesOfOrganisms.objects.all()) # all 3 of them
        
def add_search_results(media_objs):
    media_objs['SearchResult']=set()
    srs=SearchResult.objects.filter(keyword='Acinetobacter')
    media_objs['SearchResult']=set(srs)
    for sr in srs:
        o=sr.get_obj()
        if not o:
            print 'sr: no object for %r' % sr
            continue
        add_obj(o, media_objs)

def add_media_names(media_objs, compounds):
    mednames=set()
    for comp in compounds:
        for mc in comp.mediacompounds_set.all():
            mednames.add(mc.medid)
    media_objs['MediaNames']=set(mednames)

def add_reactants(media_objs):
    reactants=set()
    for p in media_objs['Products']:
        reactants.add(p.rxntid)
    media_objs['Reactants']=set(reactants)

def add_contributor(media_objs):
    media_objs['Contributor']=set(Contributor.objects.all())
    media_objs['Lab']=set(Lab.objects.all())
    media_objs['User']=set(User.objects.all())


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

        for classname,objs in related.items():
            try:
                media_objs[classname].update(set(objs))
            except KeyError:
                media_objs[classname]=set(objs)



    print 'sorting compounds...'
    compounds=sorted(compounds, key=lambda c: c.n_related)
    print 'done sorting'

    add_secretion_uptakes(media_objs)
    add_secretion_uptake_keys(media_objs)
    add_biomass(media_objs)
    add_organisms(media_objs)
    add_search_results(media_objs)
    add_media_names(media_objs, compounds)
    add_growth_data(media_objs)
    add_contributor(media_objs)

#    add_reactants(media_objs)

    write_fixture(media_objs)
    report(media_objs, bad_compounds)

def report(media_objs, bad_compounds):
    print
    for k in sorted(media_objs.keys()):
        v=media_objs[k]
        print '%s(%s): %d' % (k,type(v),len(v))
    print '%d bad compounds' % len(bad_compounds)

def write_fixture(media_objs):
    json_fn='fixture.json'
    pk_fn='fixture.pk'

    # collect everything in one big list:
    l=[]
    for v in media_objs.values():
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




def all_related(obj, related={}):
    ''' find all the related objects to an object, ie, all objects ref'd by foreign keys.  recursive '''
    n=0
    manager_names=[a for a in dir(obj) if a.endswith('_set')]
    if 'seedcompounds_set' in manager_names: 
        manager_names.remove('seedcompounds_set')
    if 'products_set' in manager_names:
        manager_names.remove('products_set')

    
    for mn in manager_names:
        manager=getattr(obj, mn)
        objs=manager.all()
        n+=len(objs)
        if len(objs)==0:
            continue
        classname=objs[0].__class__.__name__
        related[classname]=objs

        for o in objs:
            all_related(o, related)
    return (related, n)

def add_related(obj, media_objs, debug=False):
    if debug:
        print 'add_related(%s) entered' % obj

    bad_objs=[]
    try:
        (related,n)=all_related(obj)
    except Exception, e:
        bad_objs.append(obj)
    obj.related=related
    obj.n_related=n

    always_add_these={'MediaCompounds': [('Compounds', 'compid')]}
    
    for classname,objs in related.items():
        if debug:
            print 'related: %d %s objects' % (len(objs), classname)
        try:
            media_objs[classname].update(set(objs))
        except KeyError:
            media_objs[classname]=set(objs)

        if classname in always_add_these:
            for obj in objs:
                for tupl in always_add_these[classname]:
                    (subclassname, attrname)=tupl
                    pk=getattr(obj, attrname).pk
                    subobj=get_obj(subclassname, pk)
                    add_obj(subobj, media_objs)
                    print 'always: added %s %s' % (subclassname, subobj)

def add_obj(a, media_objs):
    classname=a.__class__.__name__
    try:
        media_objs[classname].add(a)
    except KeyError:
        try:
            media_objs[classname]=set(a)
        except TypeError as e:
            print 'warning: unable to add %s: %s: %s' % (classname, a, e)
            pass


if __name__=='__main__':
    main()
