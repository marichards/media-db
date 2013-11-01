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
        print '%d organisms in db' % Organisms.objects.count()
        self._test_valid('minimal_valid')

    def test_full(self):
        self._test_valid('full_valid')

    def test_missing_pmid(self):
        self._test_valid('missing_pmid')

    def test_missing_amount1(self):
        self._test_valid('missing_amount1')

    def test_missing_rate1(self):
        self._test_valid('missing_rate1')


    def test_missing_amount2(self):
        self._test_valid('missing_amount2')

    def _test_valid(self, input_key):
        input=newmedia_inputs[input_key]
        form=NewMediaForm(input['args'])
        self.assertEqual(form.is_valid(), input['valid'])
