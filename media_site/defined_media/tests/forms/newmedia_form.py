import logging
log=logging.getLogger(__name__)

from django.test import TestCase
from defined_media.forms import NewMediaForm
from defined_media.models import Organisms
from defined_media.tests.forms.test_cases import newmedia_inputs

class TestNewmedia_Form(TestCase):
    fixtures=['fixture.json']
    def setUp(self):

        pass
    def tearDown(self):
        pass

    def test_missing_uptake(self): # is still valid
        self._test_valid('minimal_valid')

    def test_full(self):
        self._test_valid('full_valid')

    def test_missing_amount1(self):
        self._test_valid('missing_amount1')

    def test_missing_rate1(self):
        self._test_valid('missing_rate1')


    def test_missing_amount2(self):
        self._test_valid('missing_amount2')

    def _test_valid(self, input_key):
        input=newmedia_inputs[input_key]
        form=NewMediaForm(input['args'])
        valid=form.is_valid()
        look_at_me='****bad bad bad****' if valid != input['valid'] else ''
        log.debug('%s valid?: expected %s, got %s %s' % (input_key, valid, input['valid'], look_at_me))
        self.assertEqual(valid, input['valid'])
