newmedia_inputs={
    'minimal_valid': {
        'args': {'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
                 'media_name': 'minimal_valid',
                 'is_minimal': 'on',
                 'first_author': 'Blow J',
                 'journal' : 'People Magazine',
                 'title': "Party like it's ",
                 'year' : 1999,
                 'link' : 'http://www.cnn.com',
                 'comp1':['h2o'], 'amount1': '1.23', 
#                 'growth_rate': '0.5',
#                 'temperature': '37.4',
#                 'ph': 7.1,
                 'contributor_id':1,
                 'additional_notes': '',
#              'uptake_comp1': 'Iron',
#              'uptake_rate1': '0.2',
               },
        'valid': True},
    'full_valid': {
        'args': {'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
                 'media_name': 'full_valid',
                 'is_minimal': 'Y',
                 'first_author': 'Blow J',
                 'journal' : 'People Magazine',
                 'title': "Party like it's ",
                 'year' : 1999,
                 'link' : 'http://www.cnn.com',
                 'comp1': ['h2o'], 
                 'amount1': '1.23', 
                 'growth_rate': '0.5',
                 'temperature': '37.4',
                 'ph': 7.1,
                 'uptake_comp1': ['Iron'],
                 'uptake_rate1': '0.2',
                 'uptake_unit1': '1/h',
                 'uptake_type1': 1,
                 'contributor_id':1,
                 'additional_notes': '',
               },
        'valid': True},
    'missing_amount1': {
        'args': {'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
                 'media_name': 'missing_amount1',
                 'is_minimal': 'on',
                 'first_author': 'Blow J',
                 'journal' : 'People Magazine',
                 'title': "Party like it's ",
                 'year' : 1999,
                 'link' : 'http://www.cnn.com',
                 'comp1':['h2o'],
#                 'amount1': '1.23', 
                 'growth_rate': '0.5',
                 'temperature': '37.4',
                 'ph': 7.1,
                 'uptake_comp1': 'Iron',
                 'uptake_rate1': '0.2',
                 'contributor_id':1,
                 'additional_notes': '',
              }, 
        'valid': False},
    'missing_rate1' : {
        'args': {'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
                 'media_name': 'missing_rate1',
                 'is_minimal': 'on',
                 'first_author': 'Blow J',
                 'journal' : 'People Magazine',
                 'title': "Party like it's ",
                 'year' : 1999,
                 'link' : 'http://www.cnn.com',
                 'comp1':['h2o'],
                 'amount1': '1.23', 
                 'growth_rate': '0.5',
                 'temperature': '37.4',
                 'ph': 7.1,
                 'uptake_comp1': 'Iron',
                 'contributor_id':1,
                 'additional_notes': '',
                 #              'uptake_rate1': '0.2',
                 },
        'valid': False},
    'missing_amount2': {
        'args': {'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
                 'media_name': 'missing_amount2',
                 'is_minimal': 'on',
                 'first_author': 'Blow J',
                 'journal' : 'People Magazine',
                 'title': "Party like it's ",
                 'year' : 1999,
                 'link' : 'http://www.cnn.com',
                 'comp1':['h2o'], 
                 'amount1': '1.23', 
                 'comp2': 'atp',
                 #              'amount2': '4.23',
                 'growth_rate': '0.5',
                 'temperature': '37.4',
                 'ph': 7.1,
                 'uptake_comp1': 'Iron',
                 'uptake_rate1': '0.2',
                 'contributor_id':1,
                 'additional_notes': '',
                 },
        'valid': False},
    'missing_bad_compound': {
        'args': {'genus': 'Acinetobacter', 'species': 'baylyi', 'strain': 'ADP1',
                 'media_name': 'missing_amount2',
                 'is_minimal': 'on',
                 'first_author': 'Blow J',
                 'journal' : 'People Magazine',
                 'title': "Party like it's ",
                 'year' : 1999,
                 'link' : 'http://www.cnn.com',
                 'comp1': 'h2o_blah', 
                 'amount1': '1.23', 
                 'comp2': 'atp',
                 'amount2': '4.23',
                 'growth_rate': '0.5',
                 'temperature': '37.4',
                 'ph': 7.1,
                 'uptake_comp1': 'Iron',
                 'uptake_rate1': '0.2',
                 'contributor_id':1,
                 'additional_notes': '',
                 },
        'valid': False},
}




