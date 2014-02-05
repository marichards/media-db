import logging, copy, json
log=logging.getLogger(__name__)

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from defined_media.tests.forms.test_cases import newmedia_inputs
from defined_media.models import *
from defined_media.forms import NewMediaForm
from defined_media.tests.snapshot import *

SUCCESS=302
FAILURE=200

class TestMediaForm(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()
        self.logged_in=self.client.login(username='vcassen', password='Bsa441_md')

    def tearDown(self):
        pass

        
    def test_media_form_get_empty(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_media_form_get_empty ***')
        response=self.client.get(reverse('new_media_form'))

        self.assertEqual(response.status_code, FAILURE)
        content=response.content
        self.assertIn('<h2>Enter Media Information:</h2>', content)
        self.assertIn("<input type='hidden' name='csrfmiddlewaretoken'", content)
        self.assertIn("<table id='id_medianames_table'>", content, "'id='id_medianames_table' not found'")


    def test_media_form_get_populated(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_media_form_get_populated ***')
        gd=GrowthData.objects.all()[0]
        log.debug(repr(gd))
        url=reverse('new_media_form', args=(gd.growthid,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, FAILURE)
        # tests to see if various form fields are populated?
        

    def test_media_form_get_id(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_media_form_get_empty ***')
        response=self.client.get(reverse('new_media_form'))

        self.assertEqual(response.status_code, FAILURE)
        content=response.content
        self.assertIn('<h2>Enter Media Information:</h2>', content)
        self.assertIn("<input type='hidden' name='csrfmiddlewaretoken'", content)
        self.assertIn("<table id='id_medianames_table'>", content, "'id='id_medianames_table' not found'")


    def test_media_form_is_valid(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_media_form_is_valid ***')
        url=reverse('new_media_form')
        for name, data in newmedia_inputs.items():
            log.debug('name is %s' % name)
            args=data['args']
            expected_valid=data['valid']
            response=self.client.post(url, args)
            expected_code=SUCCESS if expected_valid else FAILURE
            log.debug('code (%s, ev=%s): expected %s, got %s' % (name,
                                                                 expected_valid, 
                                                                 expected_code, 
                                                                 response.status_code))
            self.assertEqual(response.status_code, expected_code, name)



    def test_media_form_post(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_media_form_post ***')
        ss1=snapshot(self, 'start')

        url=reverse('new_media_form')
        log.debug('url is %s' % url)
        args=copy.copy(newmedia_inputs['minimal_valid']['args'])
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, SUCCESS)
        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {GrowthData: +1, 
                                                    Sources: +1, 
                                                    MediaNames: +1, 
                                                    MediaCompounds: +1})

    def test_media_form_post_four_compounds_two_uptakes(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_media_form_four_compounds_two_uptakes ***')
        
        url=reverse('new_media_form')
        ss1=snapshot(self, 'start')

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
        self.assertEqual(response.status_code, SUCCESS)

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', {
                GrowthData: +1,
                Sources: +1,
                MediaNames: +1,
                SecretionUptake: +2, # normally would be +2, but fixture singularity
                MediaCompounds: +4,
                })

    def test_bad_compound(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_bad_compound ***')
        ss1=snapshot(self, 'start')

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['comp1']='fred'
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, FAILURE) # form_invalid(form) returns 200
        content=response.content
        mg=re.search(r'errors start(.*)errors end', content)
        if mg:
            log.debug(mg.groups(0))
        else:
            log.debug('no match')

        self.assertIn('1 Error', content, 'not found: "1 Error"')
        expected='Compound 1: Unknown compound &quot;fred'
        self.assertIn(expected, content, expected)

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish')

    def test_bad_uptake_compound(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_bad_uptake_compound ***')
        ss1=snapshot(self, 'start')

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['uptake_comp1']='fred'
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, FAILURE) # form_invalid(form) returns 200
        content=response.content
        mg=re.search(r'errors start(.*)errors end', content)
        if mg:
            log.debug(mg.groups(0))
        else:
            log.debug('no match')

        self.assertIn('1 Error', content, 'not found: "1 Error"')
        expected='Uptake 1: Unknown compound &quot;fred'
        log.debug('errors: %s' % self.get_errors(content))
        self.assertIn(expected, content, expected)

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish')

        

    def test_bad_amount(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_bad_amount ***')
        ss1=snapshot(self, 'start')
        n_gd=GrowthData.objects.count()
        n_src=Sources.objects.count()
        n_mn=MediaNames.objects.count()
        n_uptake=SecretionUptake.objects.count()

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        args['amount1']='fred'
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, FAILURE) # form_invalid(form) returns 200
        content=response.content
        
        self.assertIn('1 Error', content, 'not found: "1 Error"')
        self.assertIn('amount1: Enter a number', content, 'not found: "amount1: Enter a number"')

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish')


    def get_errors(self, content):
        ''' extract the error messages  '''
        mg=re.search(r'errors start -->(.*)<!-- errors end', content, flags=re.DOTALL)
        if mg:
            return mg.groups(0)[0]
        else:
            return None

    def test_missing_fields(self):
        self.verify_fresh_fixture()
        '''
        delete one necessary field at a time, make sure 
        '''
        form=NewMediaForm()

        for f in newmedia_inputs['full_valid']['args'].keys():
            if f.startswith('uptake'): 
                continue        # uptakes aren't required
            if f.startswith('is_'):
                continue        # likewise
            if not form.is_required(f):
                continue        # never mind
            self._test_missing_field(f)
    '''
    def test_missing_amount1(self):
    self.verify_fresh_fixture()
        self._test_missing_field('amount1')

    def test_missing_title(self):
    self.verify_fresh_fixture()
        self._test_missing_field('title')

    def test_missing_comp1(self):
    self.verify_fresh_fixture()
        self._test_missing_field('comp1')
    '''

    def _test_missing_field(self, f):
        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        log.debug('deleting %s' % f)
        del args[f]

        response=self.client.post(url, args)
        self.assertEqual(response.status_code, FAILURE) # form_invalid(form) returns 200
        
        errors=self.get_errors(response.content)
#        self.assertIn('1 Errors', '%s %s' % (f, errors))
        # may be other errors....
        self.assertIn('%s: This field is required' % f, '%s %s' % (f, errors))

    def test_missing_amount(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_missing_amount ***')
        ss1=snapshot(self, 'start')

        url=reverse('new_media_form')
        args=copy.copy(newmedia_inputs['full_valid']['args'])
        del args['amount1']
        response=self.client.post(url, args)
        self.assertEqual(response.status_code, FAILURE) # form_invalid(form) returns 200
        content=response.content

        self.assertIn('1 Error', content, 'not found: "1 Error"')
        expected='amount1: This field is required'
        self.assertIn(expected, content, 'not found: "%s"' % expected)

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish')

    
    def check_compounds(self, args):
        errors=[]
        for key in [c for c in args.keys() if 'comp' in c]:
            try: comp_name=args[key][0]
            except TypeError: comp_name=args[key]
            try:
                comp=Compounds.objects.with_name(comp_name)
            except Compounds.DoesNotExist:
                errors.append('missing needed compound: %s' % comp_name)
        if len(errors)>0:
            for err in errors:
                log.debug('check_compounds: error=%s' % err)
            self.fail()


    def test_two_uptakes(self):
        self.verify_fresh_fixture()
        log.debug('\n*** test_two_uptakes ***')
        ss1=snapshot(self, 'start')

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
        self.assertEqual(response.status_code, SUCCESS)
        content=response.content

        ss2=snapshot(self, 'finish')
        compare_snapshots(self, 'start', 'finish', 
                          {GrowthData: +1, 
                           Sources: +1, 
                           MediaNames: +1, 
                           SecretionUptake: +2, # Normally this would be +2, but there's a weirdness in the fixture
                           MediaCompounds: +1})


    def test_good_update(self):
        self.verify_fresh_fixture()
        ''' 
        Alters as many fields as possible while still allowing a successful update.
        '''
        log.debug('\*** test_good_update ***')

        ss0=snapshot(self, 'before')
        gd0=GrowthData.objects.get(growthid=265)
        log.debug('gd0: %s' % gd0)
        form_dict=gd0.as_dict()
#        log.debug('post args: %s' % json.dumps(form_dict, indent=4))

        # make changes to form_dict (don't add any new records) (yet):
        form_dict['media_name']='new media name'     # was something else
        form_dict['temperature_c']=38.0     # was 37.0

        form_dict['genus']='Porphyromonas'
        form_dict['species']='gingivalis'
        form_dict['strain']='W83'

#        form_dict['first_author']='Cheng' # was peng
        # this causes an IntegrityError: Duplicate title
        
        form_dict['amount1']=45.4 # was 55.506, goes with beta-D-glucose
        form_dict['comp5']='water' # was MgSO4

        form_dict['uptake_type2']=2 # was 1
        form_dict['uptake_unit2']='1/h' # was 'mmol/gDW/h'


        # post the updated gd0 (via the dict)
        url=reverse('new_media_form')
        response=self.client.post(url, form_dict)
        log.debug('status_code: %d' % response.status_code)
#        log.debug('content: %s' % response.content)
        msg='status: %d (should be 302 on success, 200 on error)' % response.status_code
        self.assertEqual(response.status_code, SUCCESS, msg)

        # nothing new should be created:
        ss2=snapshot(self, 'after')
        compare_snapshots(self, 'before', 'after')

        # pull out the new records: growth data, organism, source, medcomps, uptakes, compare to dict
        gd1=GrowthData.objects.get(growthid=265)
        log.debug('gd1: %s' % gd1)
        self.assertEqual(gd1.medid.media_name, form_dict['media_name'])
        self.assertEqual(gd1.temperature_c,    form_dict['temperature_c'])
        self.assertEqual(gd1.strainid.genus,   form_dict['genus'])
        self.assertEqual(gd1.strainid.species, form_dict['species'])
        self.assertEqual(gd1.strainid.strain,  form_dict['strain'])
        msg='was %s, now %s, should be %s' % (gd0.sourceid.first_author, gd1.sourceid.first_author, form_dict['first_author'])
        self.assertEqual(gd1.sourceid.first_author, form_dict['first_author'], msg)

        # these are trickier:
        # find the media comp record with the correct medid and compid for amount1:
        medcomp1=MediaCompounds.objects.get(medid=gd1.medid, compid__name=form_dict['comp1'])
        self.assertEqual(medcomp1.amount_mm, form_dict['amount1'])

        comp5=Compounds.objects.with_name(form_dict['comp5']) # 'water' is a synonym
        medcomp5=MediaCompounds.objects.get(medid=gd1.medid, compid__name=comp5.name)
        self.assertEqual(medcomp5.amount_mm, form_dict['amount5'])

#        self.assertEqual(gd1.medid.)=form_dict['uptake_type2n']
        uptake_comp2=Compounds.objects.with_name(form_dict['uptake_comp2'])
        try:
            su=SecretionUptake.objects.get(growthid=gd1.growthid, 
                                           compid=uptake_comp2.compid)
            self.assertEqual(su.units, form_dict['uptake_unit2'])
            self.assertEqual(su.rate, form_dict['uptake_rate2'])
            self.assertEqual(su.rateid_id, form_dict['uptake_type2'])
                             
        except SecretionUptake.DoesNotExist:
            msg='No (modified) SecrtionUptake found for su.growthid=%d, compid=%s' % (gd1.growthid, uptake_comp2.name)
            self.fail(msg)


        # verify no other records were deleted (Compounds, etc)

    def verify_fresh_fixture(self):
        for cls, expected in {GrowthData: 4,
                              Compounds: 78,
                              MediaNames: 187,
                              MediaCompounds: 375,
                              Sources: 8,
                              Organisms: 30,
                              SecretionUptake: 13}.items():
            self.assertEqual(cls.objects.count(), expected)
