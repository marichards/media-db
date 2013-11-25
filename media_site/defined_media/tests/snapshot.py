import inspect
from django.db.models import Model
import defined_media.models as models

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

def snapshot():
    ''' dict: k=cls, v=count '''
    self.ss={cls: cls.objects.count() for cls in model_classes()}


