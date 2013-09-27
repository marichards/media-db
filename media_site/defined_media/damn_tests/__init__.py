import unittest
print 'fart2'

#from media_site.defined_media.tests import media_names
import media_names

def suite():
    print 'suite called'
    tests_loader = unittest.TestLoader().loadTestsFromModule
    test_suites = []
    test_suites.append(tests_loader(media_names))
    return unittest.TestSuite(test_suites)
