from django.core.management.base import BaseCommand, CommandError
from django.db import models
from defined_media.models import *
import json

class Command(BaseCommand):
    help='write a .js file containing data needed for the newmedia form page'

    stats={}

    def handle(self, *args, **options):
        try:
            try: out_fn=args[0]
            except: out_fn='defined_media/static/defined_media/js/data.js'

            data={'secretion_uptake_units': self.export_secretion_uptake_units()}
            
            with open(out_fn, 'w') as f:
                f.write('document.data=%s\n' % json.dumps(data, indent=2))
                print '%s written' % out_fn

        except Exception, e:
            import traceback
            print 'caught(%s): %s' % (type(e), e)
            traceback.print_exc()
        


    def export_secretion_uptake_units(self):
        return list(set([u.units for u in SecretionUptake.objects.all()]))

