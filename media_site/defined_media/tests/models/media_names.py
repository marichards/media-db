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
        

    def test_mn277(self):
        try:
            mn277=MediaNames.objects.get(medid=277)
            self.assertTrue(isinstance(mn277, MediaNames))
            print mn277.sorted_compounds() # this barfs
        except MediaNames.DoesNotExist:
            log.debug('MediaNames.objects.get(medid=277) does not exist')
            

    def test_as_dict(self):
        args={'media_name': 'some name',
              'is_defined': 'Y',
              'is_minimal': 'Y',
              }
        mn=MediaNames(**args)
        d=mn.as_dict()
        self.assertTrue(d, args)

        args['medid']=-3
        mn=MediaNames(**args)
        d=mn.as_dict()
        self.assertTrue(d, args)
        self.fail(str(d))


