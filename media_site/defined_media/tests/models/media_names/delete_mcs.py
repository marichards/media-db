from django.test import TestCase
from defined_media.models import *
from defined_media.tests.snapshot import snapshot, compare_snapshots

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

    def test_delete_mcs(self):
        args={'media_name': 'some name',
              'is_defined': 'Y',
              'is_minimal': 'Y',
              }
        ss1=snapshot(self, 'start')
        mn=MediaNames(**args)
        mn.save()
        self.assertTrue(mn.medid>0)
        log.debug('saved %s' % mn)

        n=5
        for comp in Compounds.objects.all()[:n]:
            mc=MediaCompounds(compid=comp, amount_mm=3.0)
            mn.mediacompounds_set.add(mc)
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', { MediaNames: +1, MediaCompounds: +n})

        mn.mediacompounds_set.all().delete()
        ss2=snapshot(self, 'after delete')
        compare_snapshots(self, 'start', 'after delete', { MediaNames: +1, MediaCompounds: +0})
