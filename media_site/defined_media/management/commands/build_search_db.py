from django.core.management.base import BaseCommand, CommandError
from django.db import models
import defined_media.models as dm_models

class Command(BaseCommand):
    help='Rebuild the search database'

    stats={}

    def handle(self, *args, **options):
        # delete all existing objects
        # for every class in models, see if it defines keywords(self)
        dm_models.SearchResult.objects.all().delete()

        for d in dir(dm_models):
            cls=getattr(dm_models, d)
            try: 
                if not issubclass(cls, models.Model): continue
            except TypeError: continue

            try: kw_method=cls.keywords
            except AttributeError: 
                self.stdout.write('no %s.keywords() defined' % d)
                continue
            
            self.stdout.write('processing %s...' % cls.__name__)
            self.stats[d]=0

            for obj in cls.objects.all():
                for kw in obj.keywords():
                    sr=dm_models.SearchResult(keyword=kw, classname=cls.__name__, obj_id=obj.pk)
                    sr.clean().save()
                    self.stats[d]+=1

        print self.stats

