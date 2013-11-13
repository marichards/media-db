import logging, copy
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from defined_media.tests.forms.test_cases import newmedia_inputs
from defined_media.models import *

class TestMediaForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_media_form_get_empty(self):
        log.debug('\n*** test_media_form_get_empty ***')
        response=self.client.get(reverse('new_media_form'))

        self.assertEqual(response.status_code, 200)
        content=response.content
        self.assertIn('<h2>Enter Media Information:</h2>', content)
        self.assertIn("<input type='hidden' name='csrfmiddlewaretoken'", content)
        self.assertIn("<table id='id_medianames_table'>", content, "'id='id_medianames_table' not found'")


    def test_media_form_get_id(self):
        log.debug('\n*** test_media_form_get_empty ***')
        response=self.client.get(reverse('new_media_form'))

        self.assertEqual(response.status_code, 200)
        content=response.content
        self.assertIn('<h2>Enter Media Information:</h2>', content)
        self.assertIn("<input type='hidden' name='csrfmiddlewaretoken'", content)
        self.assertIn("<table id='id_medianames_table'>", content, "'id='id_medianames_table' not found'")


    def test_media_form_is_valid(self):
        log.debug('\n*** test_media_form_is_valid ***')
        url=reverse('new_media_form')
        for name, data in newmedia_inputs.items():
            log.debug('name is %s' % name)
            args=data['args']
            expected_valid=data['valid']
            response=self.client.post(url, args)
            expected_code=302 if expected_valid else 200
            log.debug('code (%s, ev=%s): expected %s, got %s' % (name,
                                                                 expected_valid, 
                                                                 expected_code, 
                                                                 response.status_code))
            self.assertEqual(response.status_code, expected_code)


    def test_media_form_post(self):
        log.debug('\n*** test_media_form_post ***')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['minimal_valid']['args'])
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(GrowthData.objects.count(), n_gd+1)
        self.assertEqual(Sources.objects.count(), n_src+1)
        self.assertEqual(MediaNames.objects.count(), n_mn+1)
        
    def test_media_form_post_four_compounds_two_uptakes(self):
        log.debug('\n*** test_media_form_four_compounds_two_uptakes ***')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        n_uptake=SecretionUptake.objects.count()

        url=reverse('new_media_form')

        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['comp2']='atp'
        args['amount2']='0.48'
        args['comp3']='UDP-N-acetyl-D-glucosamine'
        args['amount3']='0.148'
        args['comp4']='Manganese'
        args['amount4']='0.348'
        
        args['uptake_comp1']='2-Oxoglutarate'
        args['uptake_rate1']='-0.2'
        args['uptake_unit1']='1/h'
        args['uptake_type1']=1
        args['uptake_comp2']='S-Adenosyl-L-methionine'
        args['uptake_rate2']='0.2'
        args['uptake_unit2']='1/h'
        args['uptake_type2']=1
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(GrowthData.objects.count(), n_gd+1)
        self.assertEqual(Sources.objects.count(), n_src+1)
        self.assertEqual(MediaNames.objects.count(), n_mn+1)
        self.assertEqual(SecretionUptake.objects.count(), n_uptake+2)

    def test_bad_compound(self):
        log.debug('\n*** test_bad_compound ***')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        n_uptake=SecretionUptake.objects.count()

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['comp1']='fred'
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 200) # form_invalid(form) returns 200
        content=response.content
        mg=re.search(r'errors start(.*)errors end', content)
        if mg:
            log.debug(mg.groups(0))
        else:
            log.debug('no match')

        self.assertIn('1 Error', content, 'not found: "1 Error"')
        expected='Compound 1: Unknown compound &quot;fred'
        self.assertIn(expected, content, expected)

        self.assertEqual(GrowthData.objects.count(), n_gd)
        self.assertEqual(Sources.objects.count(), n_src)
        self.assertEqual(MediaNames.objects.count(), n_mn)
        self.assertEqual(SecretionUptake.objects.count(), n_uptake)
        

    def test_bad_amount(self):
        log.debug('\n*** test_bad_amount ***')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        n_uptake=SecretionUptake.objects.count()

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['amount1']='fred'
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 200) # form_invalid(form) returns 200
        content=response.content
        
        self.assertIn('1 Error', content, 'not found: "1 Error"')
        self.assertIn('amount1: Enter a number', content, 'not found: "amount1: Enter a number"')

        self.assertEqual(GrowthData.objects.count(), n_gd)
        self.assertEqual(Sources.objects.count(), n_src)
        self.assertEqual(MediaNames.objects.count(), n_mn)
        self.assertEqual(SecretionUptake.objects.count(), n_uptake)


    def get_errors(self, content):
        mg=re.search(r'errors start -->(.*)<!-- errors end', content, flags=re.DOTALL)
        if mg:
            return mg.groups(0)[0]
        else:
            return None

    def test_missing_fields(self):
        url=reverse('new_media_form')
        for f in newmedia_inputs['full_valid']['args'].keys():
            if f.startswith('uptake'): 
                continue        # uptakes aren't required
            if f.startswith('is_'):
                continue        # likewise
            args=copy.copy(newmedia_inputs['full_valid']['args'])
            del args[f]
            response=self.client.post(url, args)
            self.assertEqual(response.status_code, 200) # form_invalid(form) returns 200

            errors=self.get_errors(response.content)
            self.assertIn('1 Errors', errors)
            self.assertIn('%s: This field is required' % f, errors)

    def test_missing_amount(self):
        log.debug('\n*** test_missing_amount ***')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        n_uptake=SecretionUptake.objects.count()

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        del args['amount1']
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 200) # form_invalid(form) returns 200
        content=response.content

        self.assertIn('1 Error', content, 'not found: "1 Error"')
        expected='amount1: This field is required'
        self.assertIn(expected, content, 'not found: "%s"' % expected)

        self.assertEqual(GrowthData.objects.count(), n_gd)
        self.assertEqual(Sources.objects.count(), n_src)
        self.assertEqual(MediaNames.objects.count(), n_mn)
        self.assertEqual(SecretionUptake.objects.count(), n_uptake)

    
    def check_compounds(self, args):
        log.debug('%d compounds in test db' % Compounds.objects.count())
        errors=[]
        for key in [c for c in args.keys() if 'comp' in c]:
            try: comp_name=args[key][0]
            except TypeError: comp_name=args[key]
            try:
                comp=Compounds.objects.with_name(comp_name)
                log.debug('found compounds %s' % comp_name)
            except Compounds.DoesNotExist:
                errors.append('missing needed compound: %s' % comp_name)
        if len(errors)>0:
            for err in errors:
                log.debug('+++ %s +++' % err)
            self.fail()

    def test_two_uptakes(self):
        log.debug('\n*** test_two_uptakes ***')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        n_uptake=SecretionUptake.objects.count()

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['uptake_comp1']=['Orthophosphate']
        args['uptake_rate1']='2.3'
        args['uptake_unit1']='1/h'
        args['uptake_type1']=1
        args['uptake_comp2']=['Diphosphate']
        args['uptake_rate2']='3.3'
        args['uptake_unit2']='1/h'
        args['uptake_type2']=1
        
        self.check_compounds(args)

        response=self.client.post(url, args)
        self.assertEqual(response.status_code, 302)
        content=response.content

        self.assertEqual(GrowthData.objects.count(), n_gd+1)
        self.assertEqual(Sources.objects.count(), n_src+1)
        self.assertEqual(MediaNames.objects.count(), n_mn+1)
        self.assertEqual(SecretionUptake.objects.count(), n_uptake+2)


    def test_missing_uptake_compounds(self):
        pass

    def test_missing_uptake_rate(self):
        pass

    def test_bad_media_name(self):
        pass
