from django.test import TestCase
from defined_media.forms import NewMediaForm
from defined_media.models import Organisms

class TestNewmedia_Form(TestCase):
    fixtures=['fixture.json']
    def setUp(self):

        pass
    def tearDown(self):
        pass

    def test_missing_uptake(self): # is still valid
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'pmid': '10238329',
              'comp1': 'h2o', 'amount1': '1.23', 
              'growthrate': '0.5',
              'temperature': '37.4',
              'ph': 7.1,
#              'uptake_comp1': 'Iron',
#              'uptake_rate1': '0.2',
              }
        self.valid(args)

    def test_full(self):
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'pmid': '10238329',
              'comp1': 'h2o', 'amount1': '1.23', 
              'growthrate': '0.5',
              'temperature': '37.4',
              'ph': 7.1,
              'uptake_comp1': 'Iron',
              'uptake_rate1': '0.2',
              }
        self.valid(args)

    def test_missing_pmid(self):
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'comp1': 'h2o', 'amount1': '1.23', 
              'growthrate': '0.5',
              'temperature': '37.4',
              'ph': 7.1,
              }
        self.invalid(args)

    def test_missing_amount1(self):
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'pmid': '10238329',
              'comp1': 'h2o',
#              'amount1': '1.23', 
              'growthrate': '0.5',
              'temperature': '37.4',
              'ph': 7.1,
              'uptake_comp1': 'Iron',
              'uptake_rate1': '0.2',
              }
        self.invalid(args)

    def test_missing_rate1(self):
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'pmid': '10238329',
              'comp1': 'h2o',
              'amount1': '1.23', 
              'growthrate': '0.5',
              'temperature': '37.4',
              'ph': 7.1,
              'uptake_comp1': 'Iron',
#              'uptake_rate1': '0.2',
              }
        self.assertTrue('uptake_rate1' not in args)
        self.invalid(args)


    def test_missing_amount2(self):
        args={'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
              'pmid': '10238329',
              'comp1': 'h2o', 
              'amount1': '1.23', 
              'comp2': 'atp',
#              'amount2': '4.23',
              'growthrate': '0.5',
              'temperature': '37.4',
              'ph': 7.1,
              'uptake_comp1': 'Iron',
              'uptake_rate1': '0.2',
              }
        self.invalid(args)



    def valid(self, args):
        form=NewMediaForm(args)
        self.assertTrue(form.is_valid())
    
    def invalid(self, args):
        form=NewMediaForm(args)
        self.assertFalse(form.is_valid())
