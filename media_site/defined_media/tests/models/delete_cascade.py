import logging
from django.test import TestCase
from defined_media.models import *
from ..snapshot import snapshot, compare_snapshots

log=logging.getLogger(__name__)

class TestSomething(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_biomass_biomasscompounds(self):
        ss1=snapshot(self, 'begin')
        bm=Biomass.objects.all()[0]
        log.debug('%s: %d biomass objects' % (bm, bm.biomasscompounds_set.count()))
        bm.delete()
        ss2=snapshot(self, 'end')
        deltas={Biomass: -1, BiomassCompounds: -23}
        compare_snapshots(self, 'begin', 'end', debug=False, deltas=deltas)

    def test_source_biomass(self):
        '''
        deleting a source deletes its biomass object, which deletes its biomasscompounds
        '''
        src=Sources.objects.get(pk=99)
        log.debug('%r' % src)
        bm_count=src.biomass_set.count()
        log.debug('count is %s' % bm_count)
        self.assertTrue(bm_count > 0)

        bmc_count=sum(bm.biomasscompounds_set.count() for bm in src.biomass_set.all())
        log.debug('bmc_count: %d' % bmc_count)

        ss1=snapshot(self, 'begin')
        src.delete()
        ss2=snapshot(self, 'end')
        deltas={Sources: -1, Biomass: -bm_count, BiomassCompounds: -bmc_count}
        compare_snapshots(self, 'begin', 'end', deltas=deltas)

    def test_source_growthdata(self):
        '''
        deleting a source deletes its growthdata objects, which deletes its secretionuptakes:
        '''
        src=Sources.objects.get(pk=37)
        gd_count=src.growthdata_set.count()
        self.assertTrue(gd_count > 0)
        sec_count=sum(gd.secretionuptake_set.count() for gd in src.growthdata_set.all())

        ss1=snapshot(self, 'begin')
        src.delete()
        ss2=snapshot(self, 'end')
        deltas={Sources: -1, GrowthData: -gd_count, SecretionUptake: -sec_count}
        compare_snapshots(self, 'begin', 'end', deltas=deltas)

    def test_source_organism(self):
        ''' same deal '''
        pass

        

