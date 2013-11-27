import logging 
from django.db.models import Model
import defined_media.models as models

log=logging.getLogger(__name__)

# Should make this a TestCase mixin
# would have to resolve hard-coded import of defined_media.models; replace with
# a module from which to extract classes

def model_classes():
    clss=[]
    for d in dir(models):
        cls=getattr(models, d)
        try: 
            if not issubclass(cls, Model): continue
        except TypeError: 
            continue
        clss.append(cls)
    return clss

def snapshot(test, name):
    ''' dict: k=cls, v=count '''
    setattr(test, name, {cls: cls.objects.count() for cls in model_classes()})
            
def compare_snapshots(test, name1, name2, deltas={}, debug=False):
    ss1=getattr(test, name1)
    ss2=getattr(test, name2)
    for cls in model_classes():
        if debug:
            log.debug('%s: %s=%d, %s=%d' % (cls.__name__, name1, ss1[cls], name2, ss2[cls]))
        if cls in deltas:
            test.assertEqual(ss1[cls], ss2[cls]+delta[cls])
        else:
            test.assertEqual(ss1[cls], ss2[cls])
                             

