import logging
from django.test import TestCase
from defined_media.models import *
from defined_media.forms import NewMediaForm

log=logging.getLogger(__name__)

class TestForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_required(self):
        form=NewMediaForm()
        required='genus species strain media_name is_defined is_minimal first_author journal year title link comp1 amount1'.split(' ')

        for field in form.visible_fields():
            log.debug('testing %s: expecting %s' % (field.name, field.name in required))
            self.assertEqual(form.is_required(field.name), field.name in required, field.name)
