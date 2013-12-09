import logging, re
log=logging.getLogger('defined_media')

class ReformatsErrors(object):
    def reformat_errors(self):
        '''
        mixin class
        self.errors is a dict() that packages each value as a <ul>...</ul>
        grrrrr...
        We strip away everything between the <ul ...>...</ul>
        '''
        log.debug('reformatting %d errors' % len(self.errors))
        errors={}
        pattern=r'<ul[^>]+><li>(.*)</li></ul>'
        rep=r'\1'
        log.debug('reformatting %d errors' % len(self.errors))
        for k,v in self.errors.items():
            errors[k]=re.sub(pattern, rep, str(v))
            log.debug('reformat[%s]: %s' % (k, errors[k]))
        self.my_errors=errors
        return self

class Gets1(object):
    '''
    mixin class: handles ambiguity with cleaned_data, where we don't know if it's a string or a list
    '''
    def get1(self, key, cls=None):
        ''' I cannot fucking figure out when form.cleaned_data[some_key] is a list or not: 
            This should not raise any exceptions other than KeyError, or a TypeError/ValueError 
            when cls != None
        '''
        maybe_a_list=self.cleaned_data[key] # this can throw
        try:
            is_scalar=type(maybe_a_list)==type(maybe_a_list[0]) # no lol's, I hope
        except TypeError:
            is_scalar=True
        except IndexError as e: # could be an empty string...
            log.debug('caught %s: %s; maybe_a_list(%s) is "%s"' % (type(e), e, type(maybe_a_list), maybe_a_list))
#            if maybe_a_list=="": return ""
#            if maybe_a_list==None: return None
            is_scalar=True      # this is untrue, but makes the logic below work...
        # ...especially as pertains to the cast with cls, which will generally barf (correctly?)

        val=maybe_a_list if is_scalar else maybe_a_list[0]

        # cast to class (eg, int) if cls provided:
        if cls:
            return cls(val)     # this can also throw
        else:
            return val



