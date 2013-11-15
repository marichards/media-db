import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from defined_media.models import Organisms

class TestOrganismAPI(TestCase):
    fixtures=['fixture.json']
    def setUp(self):
        self.client=Client()

    def tearDown(self):
        pass

    def test_organisms_list_GET(self):
        self._test_organisms_list()
        self._test_organisms_list(genus='Chromohalobacter')
        self._test_organisms_list(genus='Chromohalobacter', species='salexigens')
        self._test_organisms_list(genus='Chromohalobacter', species='salexigens', strain='CHR183')


    def _test_organisms_list(self, **args):
        arg_names=['genus', 'species', 'strain']
        filter_args={}
        url_args=[]
        for arg in arg_names:
            if arg in args:
                filter_args[arg]=args[arg]
                url_args.append(args[arg])

        db_orgs=Organisms.objects.filter(**filter_args)
        url=reverse('organism_api', args=url_args)
        response=self.client.get(url, ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.content)
        self.assertEqual(len(data), len(db_orgs))



        
