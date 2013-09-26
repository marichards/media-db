import os, sys

class django_env(object):
    def __init__(self, root_dir, proj_name, app_name, **kwargs):
        if root_dir not in sys.path:
            sys.path.append(root_dir)
            sys.path.append(os.path.join(root_dir, proj_name))

        if 'settings_fn' in kwargs:
            django_dir=os.path.dirname(kwargs['settings_fn'])
            sys.path.append(django_dir)
            settings=os.path.basename(kwargs['settings_fn'])
        else:
            settings=proj_name+'.settings'
        os.environ['DJANGO_SETTINGS_MODULE']=settings


def init_django_env(root_dir, proj_name, app_name, **kwargs):
    return django_env(root_dir, proj_name, app_name, **kwargs)

