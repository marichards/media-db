import sys, os, subprocess, time, django
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
import defined_media.models as models
import media_site.settings as settings

class Command(BaseCommand):
    help='Take a snapshot of the database and store it in the statics section so it can be downloaded.'

    def handle(self, *args, **options):
        ss=self.create_dump()
        self.copy_dump_to_static()


    def create_dump(self):
        ''' effect a 'mysqldump media_database  >dump_dir/media_database.<ts>.sql '''
        #cmd=['mysqldump', settings.DATABASES['default']['NAME']]
	if settings.DATABASES['default']['PASSWORD']:
            cmd=['mysqldump', settings.DATABASES['default']['NAME'], '-u', settings.DATABASES['default']['USER'], '-p', settings.DATABASES['default']['PASSWORD']]	
	else:
            cmd=['mysqldump', settings.DATABASES['default']['NAME'], '-u', settings.DATABASES['default']['USER']]	
        clss=[]
        forbidden=[models.User, models.DatabaseSnapshot, models.Lab]
        for attr in dir(models):
            try:
                cls=getattr(models, attr)
                if issubclass(cls, django.db.models.Model) and cls not in forbidden:
                    cmd.append(cls._meta.db_table)
            except TypeError as e:
                pass
#                print '%s is not a class, skipping' % attr

        with open(self.dump_path(), 'w') as new_stdout:
            mysqldump=subprocess.Popen(cmd, stdout=subprocess.PIPE)
            retcode=subprocess.call(('gzip',), stdin=mysqldump.stdout, stdout=new_stdout)
            if retcode==0:
                print '%s created (%s)' % (self.dump_path(), retcode)
                try:
                    ss=models.DatabaseSnapshot()
                    ss.save()
                except IntegrityError as e:
                    ss=models.DatabaseSnapshot.objects.latest('timestamp')
                return ss
            else:
                print 'failed: %s' % ' '.join(cmd)
                sys.exit(retcode)


    def copy_dump_to_static(self):
        src_file=self.dump_path()
        dst_file=self.static_path()
        cmd=['cp', src_file, dst_file]
        retcode=subprocess.call(cmd)
        if retcode==0:
            print '%s created (%s)' % (dst_file, retcode)
        else:
            print 'failed: %s' % ' '.join(cmd)
            sys.exit(retcode)


    def dump_dir(self):
        return os.path.join(settings.SITE_ROOT, 'dumps')

    def static_dir(self):
        return os.path.join(settings.SITE_ROOT, 'media_site/defined_media/static/defined_media/downloads')

    def static_path(self):
        return os.path.join(self.static_dir(), self.dump_fn())

    def dump_fn(self):
        return 'media_database.%s.sql.gz' % time.strftime('%d%b%Y')

    def dump_path(self):
        return os.path.join(self.dump_dir(), self.dump_fn())

