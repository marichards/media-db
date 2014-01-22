'''
- get a growth_data (gd) record
- clone it
- try to save it (without altering any fields)
- veryify that "This record resembles this other record" message appears
'''

import logging, copy, json
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.tests.forms.test_cases import newmedia_inputs
from defined_media.models import *
from defined_media.forms import NewMediaForm
from defined_media.tests.snapshot import *


class TestMediaForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        username='vcassen'
        if not self.client.login(username=username, password='Bsa441_md'):
            raise RuntimeError("Can't login")
        log.debug('logged in as %s' % username)

    def tearDown(self):
        pass

    def test_clone_dup(self):
        gd0=GrowthData.objects.all()[0]
        log.debug('gd0: %r' % gd0)
        log.debug('gd0.contributor_id: %s' % gd0.contributor_id)
        url=reverse('new_media_form', args=(gd0.growthid,))
        args=gd0.as_dict()
        del args['growthid']
#        for k in sorted(args.keys()):
#            v=args[k]
#            log.debug('args[%s]: %s' % (k,v))
        response=self.client.post(url, args)
        log.debug('content: %s' % response)

        # We should get the same form back, with an error message about "unable to
        # save duplicate growth record"...
        # If we get a redirect to a new newmedia page, it means we successfully created the new record, which is bad
        self.assertEqual(response.status_code, 200, response.content)

        
        
        
