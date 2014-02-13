import logging, argparse, copy
log=logging.getLogger(__name__)

from django.test import TestCase
from defined_media.old_forms import NewCompoundMediaForm
from defined_media.models import Organisms, Compounds
from defined_media.tests.forms.test_cases import newmedia_inputs


class TestNewmedia_Form(TestCase):
    fixtures=['fixture.json']
    _ran={}

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all(self):
        for k in newmedia_inputs.keys():
            self._test_valid(k)

    def test_missing_uptake(self): # is still valid
        for k,v in newmedia_inputs['minimal_valid']['args'].items():
            log.debug('minimal: %s=%s' % (k,v))
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
        log.debug('_test_valid(%s) entered' % input_key)
        if input_key in self._ran: return
        self._ran[input_key]=True

        input_d=newmedia_inputs[input_key]
        form=NewCompoundMediaForm(input_d['args'])
        self._test_form(form, input_key, input_d['valid'])

    def _test_form(self, form, input_key, expected_valid):
        got_valid=form.is_valid()
        look_at_me='****bad bad bad****' if got_valid != expected_valid else 'ok'
        log.debug('%s valid?: expected %s, got %s %s' % (input_key, expected_valid, got_valid, look_at_me))
        self.assertEqual(got_valid, expected_valid, 'expecting %s' % expected_valid)


    def test_incomplete_uptake(self):
        for part in ['rate', 'type', 'unit']:
            args=copy.copy(newmedia_inputs['full_valid']['args'])
            key='uptake_%s1' % part
            del args[key]
            form=NewCompoundMediaForm(args)
            self._test_form(form, 'incomplete_uptake: %s' % part, False)
            self.assertIn('uptake1', form.errors)
            expected='Uptake 1: These fields are required: %s' % part
            self.assertEqual(form.errors['uptake1'], expected, expected)


    def _check_fixture_compounds(self, *comp_names):
        self.assertTrue(Compounds.objects.count() >= 50)
        for comp_name in comp_names:
            try:
                comp=Compounds.objects.with_name(comp_name)
            except Compounds.DoesNotExist:
                self.fail()


    def test_unknown_comp(self):
        self._check_fixture_compounds()
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['comp2']=['unobtanium']
        args['amount2']=1.0
        form=NewCompoundMediaForm(args)
        self._test_form(form, 'unknown_compound', False)

        self.assertEqual(len(form.errors), 1, 'got %d errors (should be 1)' % len(form.errors))
        self.assertIn('comp2', form.errors)
        expected='Compound 2: Unknown compound "unobtanium"'
        got=form.errors['comp2']
        self.assertEqual(expected, got, got)
        




    def test_unknown_uptake_comp(self):
        self._check_fixture_compounds()

        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['uptake_comp2']=['unobtanium']
        args['uptake_rate2']=1.0
        args['uptake_type2']=1
        args['uptake_unit2']='1/h'

        form=NewCompoundMediaForm(args)
        self._test_form(form, 'unknown_uptake_comp', False)

        self.assertEqual(len(form.errors), 1, 'got %d errors (should be 1)' % len(form.errors))
        self.assertIn('uptake2', form.errors)
        expected='Uptake 2: Unknown compound "unobtanium"'
        got=form.errors['uptake2']
        self.assertEqual(expected, got, got)
        
    def test_two_uptakes(self):
        self._check_fixture_compounds('Orthophosphate', 'Diphosphate')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['uptake_comp1']=['Orthophosphate']
        args['uptake_rate1']='2.3'
        args['uptake_unit1']='1/h'
        args['uptake_type1']=1
        args['uptake_comp2']=['Diphosphate']
        args['uptake_rate2']='3.3'
        args['uptake_unit2']='1/h'
        args['uptake_type2']=1

        form=NewCompoundMediaForm(args)
        self._test_form(form, 'two_uptakes', True)
        self.assertEqual(len(form.errors), 0, 'got %d errors (should be 0)' % len(form.errors))
