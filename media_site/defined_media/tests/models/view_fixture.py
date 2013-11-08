import sys
from django.test import TestCase
import defined_media.models as models
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
        for d in dir(models):
            cls=getattr(models, d)
            try: 
                if not issubclass(cls, Model): continue
            except TypeError: continue

            try:
                count=cls.objects.count()
            except AttributeError:
                continue
            except Exception, dberr:
                print 'caught %s: %s' % (type(dberr), dberr)
                continue

            if count>0:
                print '%s: %d rows' % (d, count) 

    def test_view_fixture(self):
        for d in dir(models):
            cls=getattr(models, d)
            try: 
                if not issubclass(cls, Model): continue
            except TypeError: continue

            try:
                print cls.__name__
                for obj in cls.objects.all():
                    print obj
                print
            except AttributeError:
                continue
            except Exception, dberr:
                print 'caught %s: %s' % (type(dberr), dberr)
                continue


        
