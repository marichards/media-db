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
    d={cls: cls.objects.count() for cls in model_classes()}
    setattr(test, name, d)
    return d
            
def compare_snapshots(test, name1, name2, deltas={}, debug=False):
    ss1=getattr(test, name1)
    ss2=getattr(test, name2)
    errors={}
    for cls in model_classes():
        before=ss1[cls]
        after=ss2[cls]
        expected=ss1[cls]+deltas[cls] if cls in deltas else ss1[cls]
        msg='%s: before=%d, after=%d, expected=%d' % (cls.__name__, before, after, expected)
        try:
            test.assertEquals(after, expected, msg)
            if debug: log.debug('%s: yay!' % cls.__name__)
        except AssertionError:
            errors[cls]=msg
            if debug: log.debug('%s: boo!' % msg)
    if debug: log.debug('errors: %s' % errors)
    test.assertEquals(len(errors), 0, str(errors))
