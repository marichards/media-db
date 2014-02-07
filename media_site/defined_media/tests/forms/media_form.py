import logging, copy, json
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.models import *
from defined_media.forms import MediaNamesForm
#from defined_media.tests.snapshot import *

class TestMediaNamesForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        self.logged_in=self.client.login(username='vcassen', password='Bsa441_md')

    def tearDown(self):
        pass

    def test_medid_field(self):
        ''' why isn't {{ form.medid }} including the value of mn.medid? '''
        mn=MediaNames.objects.first()
        self.assertTrue(mn.medid > 0)
        form=MediaNamesForm(mn.as_dict())
        self.assertTrue(form.is_valid())
        field=form.fields['medid']
        widget=field.widget
#        for d in dir(widget):
#            log.debug('%s: %s' % (d, type(getattr(widget, d))))
        self.fail(widget.render())

    def test_add_medcomp_fields(self):
        mn=MediaNames.objects.first()
        form=MediaNamesForm(mn)
        self.assertEqual(len(form.medcomp_fields()), mn.mediacompounds_set.count())
        log.debug('medcomp_values: %s' % form.medcomp_values())

        log.debug('%d form.fields' % len(form.fields))
        log.debug('form.fields(%s): %s' % (type(form.fields), form.fields))
        for k,v in form.fields.items():
            log.debug('form.fields[%s]: %s' % (k,v.label))

        self.fail()             # just to insure we see the output

