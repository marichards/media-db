
import defined_media.models as models

def test_sort_compounds():
    print '%d compounds' % models.Compounds.objects.count()

    compounds=list(models.Compounds.objects.all())
    assert len(compounds)==20

#    print 'pre-sort: %s' % [str(c.compid) for c in compounds]
    compounds.sort(key=lambda c: c.keywords()[0])
#    print 'post-sort: %s' % [str(c.compid) for c in compounds]

    
    expected_ids=[20, 2, 33, 31, 39, 44, 37, 41, 49, 25, 47, 34, 3, 6, 9, 22, 46, 42, 29, 38]
    sorted_ids=[x.compid for x in compounds]
#    print ', '.join([str(x) for x in sorted_ids])
    assert sorted_ids==expected_ids

