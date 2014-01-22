from django.test import TestCase
from defined_media.models import *
from defined_media.tests.snapshot import *

class TestGrowthData(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equals(self):
        gd0=GrowthData.objects.all()[0]
        contributor=Contributor.objects.exclude(id=gd0.contributor_id)[0]
        gd1=gd0.clone_and_save(contributor)
        self.assertFalse(gd0.equals(gd1))
        self.assertFalse(gd1.equals(gd0))

        gd0.medid.media_name=gd1.medid.media_name
        self.assertFalse(gd0.equals(gd1)) # still different
        self.assertFalse(gd1.equals(gd0))

        gd0.medid=gd1.medid
        self.assertFalse(gd0.equals(gd1)) # still different
        self.assertFalse(gd1.equals(gd0))

        gd1.contributor=gd0.contributor
        self.assertTrue(gd0.equals(gd1)) # now they're the same!
        self.assertTrue(gd1.equals(gd0))
        

    def _test_not_equals(self, cls, attr, attr_id=None, sub_id=None):
        gd0=GrowthData.objects.all()[0]
        contributor=Contributor.objects.exclude(id=gd0.contributor_id)[0]
        gd1=gd0.clone_and_save(contributor)

        if attr_id is None: 
            attr_id='%s_id' % attr
        if sub_id is None:
            sub_id=attr

        attr_val=getattr(gd0, attr_id)
        exclude_args={sub_id: attr_val}
        obj=cls.objects.exclude(**exclude_args)[0]
        setattr(gd1, attr, obj) # attr_id was attr
        self.assertFalse(gd0.equals(gd1))
        self.assertFalse(gd1.equals(gd0))

    def test_contributor_not_equals(self):
        return self._test_not_equals(Contributor, 'contributor', attr_id='contributor_id', sub_id='id') # sub_id='id'?

    def test_mn_not_equals(self):
        return self._test_not_equals(MediaNames, 'medid')

    def test_org_not_equals(self):
        return self._test_not_equals(Organisms, 'strainid')

    def test_src_not_equals(self):
        return self._test_not_equals(Sources, 'sourceid')
        pass


    def test_info_not_equals(self):
        pass                    # this is kinda trivial, but tedious



    def test_up_sec_not_equals(self):
        pass                    # not sure we actually care about this

    def test_clone(self):
        ss1=snapshot(self, 'before clone')
        gd0=GrowthData.objects.all()[0]
        contributor=Contributor.objects.exclude(id=gd0.contributor_id)[0]
        gd1=gd0.clone_and_save(contributor)

        self.assertEqual(gd1.contributor_id, contributor.id)
        self.assertEqual(gd0.strainid, gd1.strainid)
        self.assertEqual(gd0.medid.media_name+' (clone)', gd1.medid.media_name)
        self.assertEqual(gd0.sourceid, gd1.sourceid)
        
        for attr in 'growth_rate growth_units ph temperature_c measureid_id'.split(' '):
            self.assertEqual(getattr(gd0, attr), getattr(gd1, attr))

        ss2=snapshot(self, 'after clone')
        deltas={GrowthData: +1, 
                MediaNames: +1, 
                MediaCompounds: gd0.medid.mediacompounds_set.count(),
                SecretionUptake: gd0.secretionuptake_set.count(),
                }
        compare_snapshots(self, 'before clone', 'after clone', debug=False, deltas=deltas)
        

    def test_find_clone(self):
        gd0=GrowthData.objects.all()[0]
        gd1=gd0.find_clone()
        log.debug('gd1: %r' % gd1)
        
