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
#        self.fail(str(d))


