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

    def test_mn277(self):
        try:
            mn277=MediaNames.objects.get(medid=277)
            self.assertTrue(isinstance(mn277, MediaNames))
            print mn277.sorted_compounds() # this barfs
        except MediaNames.DoesNotExist:
            log.debug('MediaNames.objects.get(medid=277) does not exist')
