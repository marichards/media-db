import sys
from django.test import TestCase
import defined_media.models as models
from django.db.models import Model

class ViewFixture(TestCase):
    def test_view_fixtures(self):
        '''
        loop through classes defined in models.py, report number of rows in table for that class
        '''
        for d in dir(models):
            cls=getattr(models, d)
            try: 
                if not issubclass(cls, Model): continue
            except TypeError: continue

            count=cls.objects.count()
            if count>0:
                print '%s: %d rows' % (d, count) 
