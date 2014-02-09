import logging
from random import random, choice, seed, randrange
from defined_media.models import Compounds

log=logging.getLogger(__name__)

class MockPostDict(dict):
    def __init__(self, mn0, seeder=None):
        ''' 
        Mock up the MediaNames POST dict.  
        Entries: "compN" -> compound name
                 "amountN" -> float (in string form)
        initialize from mn0 
        '''
        if seeder is not None: seed(seeder)

        for field in 'media_name is_defined is_minimal'.split(' '):
            self[field]=getattr(mn0, field)

        for i,mc in enumerate(mn0.mediacompounds_set.all()):
            compkey='comp%d' % i
            self[compkey]=mc.compid.name
            amtkey='amount%d' % i
            self[amtkey]=mc.amount_mm
        
    def random_changes(self, n_changes):
        ''' change some random entries; return a list of amtkey '''
        changed=[]
        n=len(self)/2
        for i in range(n_changes):
            k=randrange(n)
            amtkey='amount%d' % k
            self[amtkey]=2*self[amtkey]*random()
            changed.append(('comp%d'%k,amtkey))
        return changed

    def random_delete(self, n_del):
        ''' delete some random entries '''
        deleted=[]
        for i in range(n_del):
            compkey=choice(self.compkeys())
            amtkey=self.amountkey_for(compkey)
            del self[compkey]
            del self[amtkey]
            deleted.append((compkey, amtkey))
        return deleted

    def random_add(self, n_add):
        ''' add some random entries '''
        added=[]
        for i in range(n_add):
            n=len(self)
            compid=randrange(Compounds.objects.count())
            comp=Compounds.objects.get(compid=compid)
            self['comp%d'%n]=comp.name
            self['amount%d'%n]=random()*10
            added.append(('comp%d'%n, 'amount%d'%n))
        return added

    def compkeys(self):
        return [k for k in self.keys() if k.startswith('comp')]
    
    def comp_from_compkey(self, compkey):
        return Compounds.objects.with_name(self[compkey])

    def amountkey_for(self, compkey):
        return 'amount%d' % int(compkey.split('comp')[1]) # using int() in insure assumption

    def amount_for(self, compkey):
        return self[self.amountkey_for(compkey)]


        
