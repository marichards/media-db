import logging
from django.test import TestCase
from django.db import transaction

from defined_media.models import *
from defined_media.tests.snapshot import snapshot, compare_snapshots
from .mock_post_dict import MockPostDict

log=logging.getLogger(__name__)

'''
to run:
py manage.py test defined_media.tests.models.media_names
'''

class TestMediaNames(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_trans_save(self):
        mn0=MediaNames.objects.first()
        log.debug('%s: %d medcomp objects' % (mn0, mn0.mediacompounds_set.count()))
        mc8=mn0.mediacompounds_set.all()[8]
        log.debug(str(mc8))
        new_amt=37
        mc8.amount_mm=new_amt;
        ss1=snapshot(self, 'start')
        try:
            with transaction.atomic():
                mn0.mediacompounds_set.add(mc8) # should raise
                log.debug('mc8 added (???)')
        except IntegrityError:
            mc8.save()
            log.debug('mc8 saved')
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {MediaCompounds: 0})

        self.assertEqual(mc8.amount_mm, new_amt, 'new mc8.amount_mm: %s' % mc8.amount_mm)
#        self.fail(str(mc8))


    def _do_changes(self, mn0, comps):
        ''' 
        Implement the changes to the database based on mn0 and comps (comps is a MockPostDict)
        This method will eventually be inserted into views.media.post.
        '''
        gds=mn0.growthdata_set.all()
        try:
            with transaction.atomic():
                # delete mn0, verify it's gone
                medid=mn0.medid
                mn0.delete()    # not sure we want to delete entire mn0; might want to individually delete mc's, becaues we don't want to have to restore mn0.growthdata_set.all()
                
                # restore mn0:
                mn0.medid=medid
                mn0.save()
                for gd in gds:
                    mn0.growthdata_set.add(gd)
                    log.debug('restored gd %s' % gd)

                # rebuild the list of mediacompounds:
                # doesn't really handle errors well; want to keep processing even if there's an error
                # OR, make damn sure form.is_valid() reports all the errors (makes more sense on a separation
                # of purpose approach) (but means form.is_valid() has to look up compounds)
                for key in comps.compkeys():
                    comp=comps.comp_from_compkey(key)
                    amount=comps.amount_for(key)
                    medcomp=MediaCompounds(medid=mn0, compid=comp, amount_mm=amount)
                    mn0.mediacompounds_set.add(medcomp)

        except IntegrityError as e:
            log.exception(e)
            self.fail(str(e))

        return mn0

    def test_delete_and_rebuild(self):
        # init new media compounds: start with mn0.mc_set, add a few random, change a few amounts, delete a few:
        mn0=MediaNames.objects.first()
        gds=mn0.growthdata_set.all()
        log.debug('%d growth_data objects' % len(gds))
        comps=MockPostDict(mn0)
        mc_changed=comps.random_changes(3)
        mc_added=comps.random_add(3)
        mc_deleted=comps.random_delete(3)

        # do the list changes
        ss1=snapshot(self, 'start')
        
        try:
            with transaction.atomic():
                # delete mn0, verify it's gone
                medid=mn0.medid
                mn0.delete()    # not sure we want to delete entire mn0; might want to individually delete mc's, becaues we don't want to have to restore mn0.growthdata_set.all()
                log.debug('after delete: mn0.medid=%s' % mn0.medid)
                ss2=snapshot(self, 'after mn delete')
                
                # restore mn0:
                mn0.medid=medid
                self.assertEqual(mn0.mediacompounds_set.count(), 0)
                mn0.save()
                for gd in gds:
                    mn0.growthdata_set.add(gd)
                    log.debug('restored gd %s' % gd)

                # rebuild the list of mediacompounds:
                for key in comps.compkeys():
                    comp=comps.comp_from_compkey(key)
                    amount=comps.amount_for(key)
                    medcomp=MediaCompounds(medid=mn0, compid=comp, amount_mm=amount)
                    mn0.mediacompounds_set.add(medcomp)

        except IntegrityError as e:
            log.exception(e)
            self.fail(str(e))

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {MediaNames: +0, 
                                                    MediaCompounds: +0, 
                                                    })

        
        # test to make sure actual changes in mediacompounds_set took place:
        name2comp={mc.compid.name:mc.amount_mm for mc in mn0.mediacompounds_set.all()}

        # check deleted:
        for pair in mc_deleted:
            del_name, del_amount=pair
            self.assertTrue(del_name not in name2comp)

        # check added:
        for pair in mc_added:
            add_name, add_amount=pair
            for mc in mn0.mediacompounds_set.all():
                if mc.compid.name==add_name:
                    self.assertEqual(mc.amount_mm, add_amount)
                    break

        # check changed:
        for pair in mc_changed:
            ch_name, ch_amount=pair
            for mc in mn0.mediacompounds_set.all():
                if mc.compid.name==ch_name:
                    self.assertEqual(mc.amount_mm, ch_amount)
                    
        self.fail()
