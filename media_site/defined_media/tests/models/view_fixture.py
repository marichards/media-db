import sys
from django.test import TestCase
import defined_media.models as models
from defined_media.tests.snapshot import *
from django.db.models import Model

'''
can call as:
py manage.py test defined_media.tests.models.view_fixture
py manage.py test defined_media.tests.models.view_fixture:ViewFixture
py manage.py test defined_media.tests.models.view_fixture:ViewFixture.test_view_fixtures
'''

class ViewFixture(TestCase):
    fixtures=['fixture.json']
    def test_view_summary(self):
        '''
        loop through classes defined in models.py, report number of rows in table for that class
        '''
        ss=snapshot()
        for cls in sorted(ss.keys()):
            count=ss[cls]
            if count>0:
                print '%-20s: %d rows' % (cls.__name__, count) 

    def test_view_fixture(self):
        for cls in snapshot().keys():
            print cls.__name__
            n=0
            for obj in cls.objects.all():
                try:
                    print '%d. %r' % (n, obj)
                    n+=1
                except Exception as e:
                    print 'caught %s: %s' % (type(e), e)

            print

        
    def test_model_classes(self):
        for cls in model_classes():
            print 'cls is %s' % cls.__name__


    def test_snapshot(self):
        for cls, count in snapshot().items():
            print '%s -> %s' % (cls, count)
