import logging
import copy
from django.test import TestCase
from defined_media.models import *
from defined_media.forms import NewMediaForm
from defined_media.views.contributors import NewMediaView
from defined_media.tests.snapshot import snapshot, compare_snapshots


log=logging.getLogger(__name__)

class TestGetOrganism(TestCase):
    '''
    This tests the functionality that gets the organism name.  That code 
    should have originally been written in the forms.NewMediaForm, where it 
    now lives, but originally it wasn't and I'm too lazy to move this test 
    under test.forms.
    '''

    fixtures=['fixture.json']
    def setUp(self):
        pass
    def tearDown(self):
        pass

    args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
          'new_genus': '', 'new_species': '', 'new_strain': '',
          'new_org_type': '1'}

    def test_empty_form(self):
        args=copy.copy(self.args)
        args['genus']=''
        args['species']=''
        args['strain']=''
        self._test_get_organism(args, False, Organisms.DoesNotExist)

########################################################################

    def test_no_new(self):
        self._test_get_organism(self.args, True, Organisms, deltas={})

    def test_new_strain(self):
        args=copy.copy(self.args)
        args['new_strain']='somenewstrain'
        self._test_get_organism(args, True, Organisms)

    def test_new_species_strain(self):
        args=copy.copy(self.args)
        args['new_species']='somenewspecies'
        args['new_strain']='somenewstrain'
        self._test_get_organism(args, True, Organisms)

    def test_new_genus_species_strain(self):
        args=copy.copy(self.args)
        args['new_genus']='somenewgenus'
        args['new_species']='somenewspecies'
        args['new_strain']='somenewstrain'
        self._test_get_organism(args, True, Organisms)

########################################################################

    def test_new_genus_old_species(self):
        args=copy.copy(self.args)
        args['new_genus']='somenewgenus'
        self._test_get_organism(args, False, Organisms.DoesNotExist,
                                {'new_species': 'New genus requires new species',
                                 'new_strain' : 'New genus requires new strain'})

    def test_new_species_old_strain(self):
        args=copy.copy(self.args)
        args['new_species']='somenewspecies'
        self._test_get_organism(args, False, Organisms.DoesNotExist, 
                                {'new_strain': 'New species requires new strain'})

    def test_new_genus_strain_old_species(self):
        args=copy.copy(self.args)
        args['new_genus']='somenewgenus'
        args['new_strain']='somenewstrain'
        self._test_get_organism(args, False, Organisms.DoesNotExist,
                                {'new_species': 'New genus requires new species'})

    def test_new_genus_species_old_strain(self):
        args=copy.copy(self.args)
        args['new_genus']='somenewgenus'
        args['new_species']='somenewspecies'
        self._test_get_organism(args, False, Organisms.DoesNotExist,
                                {'new_strain': 'New genus requires new strain'})

########################################################################

    def _test_get_organism(self, formargs, expect_success, expected_class, errors={}, deltas=None):
        form=NewMediaForm(formargs)
        self.assertFalse(form.is_valid())
        try:
            cd=form.cleaned_data
            self.assertTrue(True)
            for k,v in form.cleaned_data.items():
                log.debug('newmedia_get_organism: cleaned_data[%s]: %s' % (k,v))
        except AttributeError:
            self.fail('form.cleaned_data not properly initialized')

        view=NewMediaView()
        ss1=snapshot(self, 'before')

        if expect_success:
            try: 
                org=view.get_organism(form)
                self.assertEqual(org.__class__, expected_class)
            except Exception as e:
                log.debug('test_get_organism: caught %s: %s' % (type(e), e))
                self.fail(str(e))
        else:
            self.assertRaises(expected_class, view.get_organism, form)

        ss2=snapshot(self, 'after')
        if deltas is None:
            deltas={Organisms: +1} if expect_success else {}
        compare_snapshots(self, 'before', 'after', deltas=deltas)

        # check error messages:
        for field, err in errors.items():
            self.assertEqual(form.errors[field], err)
