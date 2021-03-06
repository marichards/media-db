from django.test import TestCase
from defined_media.models import *

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

    def test_delete_media_compounds(self):
        ''' verify the behavior of the delete cascade:
            when a MediaName object is deleted, all of its MediaCompound objects are also deleted
            However, no Compounds objects are deleted
        '''
        n_comps0=Compounds.objects.count()

        mn=MediaNames.objects.all()[0]
        mc_ids=[x.medcompid for x in mn.mediacompounds_set.all()]
        for mc_id in mc_ids:
            try:
                mc=MediaCompounds.objects.get(medcompid=mc_id)
                self.assertTrue(mc != None)
            except MediaCompounds.DoesNotExist:
                self.fail('MediaCompounds %d does not exist???' % mc_id)

        mn.delete()
        for mc_id in mc_ids:
            try:
                mc=MediaCompounds.objects.get(medcompid=mc_id)
                self.fail('MediaCompound  %d not deleted' % mc_id)
            except MediaCompounds.DoesNotExist:
                self.assertTrue(True)

        n_comps1=Compounds.objects.count()
        self.assertEqual(n_comps0, n_comps1, 'Compounds were deleted: %d -> %d' % (n_comps0, n_comps1))
