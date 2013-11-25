from django.test import TestCase
from defined_media.models import *

class TestGrowthData(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fixture_integrity_compounds(self):
        ''' 
        check existance/integrity of associated MediaCompound and Compunds objects
        '''
        for gd in GrowthData.objects.all():
            for d in gd.media_compounds_dicts():
                try:
                    comp=Compounds.objects.with_name(d['comp'])
                    amount=float(d['amount'])
                except:
                    self.fail()
        self.assertTrue(True)
                

    def test_fixture_integrity_uptakes(self):
        for gd in GrowthData.objects.all():
            for d in gd.uptake_dicts():
                try:
                    comp=Compounds.objects.with_name(d['comp'])
                    rate=float(d['rate'])
                    units=d['units']
                    typ=int(d['type'])
                except Exception as e:
                    self.fail(str(e))
        self.assertTrue(True)

    def test_delete_cascade(self):
        '''
        exploring the behavior of the delete cascade:
        Deleting a growthdata object deletes the objects itself, but doesn't appear to delete any 
        of Organism, Source, or MediaNames
        '''
        gd=GrowthData.objects.all()[0]
        old_growthid=gd.growthid
        n_gd=GrowthData.objects.count()
        print 'using GrowthData growthid=%s %d gd objects' % (gd.growthid, GrowthData.objects.count())

        # check for existing sub-objects in db:
        for attrname, cls in [('strainid',Organisms), 
                              ('medid', MediaNames), # shouldn't this one actually be deleted?
                              ('sourceid', Sources),
                              ]:

            try:
                args={attrname: getattr(gd,attrname+'_id')}
                obj=cls.objects.get(**args)
                print '%s %s found in db' % (cls.__name__, obj)
            except cls.DoesNotExist as e:
                self.fail('no %s for %s=%d' % (cls.__name__, attrname, getattr(gd,attrname+'_id')))

        # delete the gd object and verify count goes down by one:
        gd.delete()             
        self.assertEqual(n_gd-1, GrowthData.objects.count())
        print 'after delete: gd.growthid=%s, count=%d' % (gd.growthid, GrowthData.objects.count())

        # make sure the gd object was deleted:
        try:
            gd2=GrowthData.objects.get(growthid=old_growthid)
            self.fail('found deleted growthdata object %s' % gd2)
        except GrowthData.DoesNotExist:
            print 'GrowthData object growthid=%s no longer exists' % old_growthid
            self.assertTrue(True)

        # repeat check for sub-objects: they're all still there:
        for attrname, cls in [('strainid',Organisms), 
                              ('medid', MediaNames), # shouldn't this one actually be deleted?
                              ('sourceid', Sources),
                              ]:
            try:
                args={attrname: getattr(gd,attrname+'_id')}
                obj=cls.objects.get(**args)
                print '%s %s still in db' % (cls.__name__, obj)
            except cls.DoesNotExist as e:
                self.fail('no %s for %s=%d' % (cls.__name__, attrname, getattr(gd,attrname+'_id')))


    def test_full_delete(self):
        '''
        GrowthData.full_delete should delete:
        - the growth_data object
        - all associated MediaNames object and all associated MediaCompound objects
        - all associated SecretionUptake objects
        BUT
        - none of the Organisms, Sources, or associated compounds objects
        '''
        for gd in GrowthData.objects.all():
            # snapshot0:
            n_gd0=GrowthData.objects.count()
            n_mn0=MediaNames.objects.count()
            n_mc0=MediaCompounds.objects.count()
            n_su0=SecretionUptake.objects.count()
            n_srcs0=Sources.objects.count()
            n_orgs0=Organisms.objects.count()
            n_comps0=Compounds.objects.count()

            # record number of MediaCompounds/SecretionUptakes to be deleted:
            n_mc=gd.medid.mediacompounds_set.count()
            n_su=gd.secretionuptake_set.count()
            
            gd.full_delete()
            
            # snapshot1:
            n_gd1=GrowthData.objects.count()
            n_mn1=MediaNames.objects.count()
            n_mc1=MediaCompounds.objects.count()
            n_su1=SecretionUptake.objects.count()
            n_srcs1=Sources.objects.count()
            n_orgs1=Organisms.objects.count()
            n_comps1=Compounds.objects.count()
            
            # Assertions:
            self.assertEqual(n_gd0-1, n_gd1)
            self.assertEqual(n_mn0-1, n_mn1)
            
            self.assertEqual(n_mc0-n_mc, n_mc1, 'MediaCompounds: %d -> %d' % (n_mc0, n_mc1))
            self.assertEqual(n_su0-n_su, n_su1, 'SecretionUptakes: %d -> %d' % (n_su0, n_su1))
            
            self.assertEqual(n_srcs0, n_srcs1, 'Sources: %d -> %d' % (n_srcs0, n_srcs1))
            self.assertEqual(n_orgs0, n_orgs1, 'Organisms: %d -> %d' % (n_orgs0, n_orgs1))
            self.assertEqual(n_comps0, n_comps1, 'Compounds: %d -> %d' % (n_comps0, n_comps1))

