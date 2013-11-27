import logging, re
log=logging.getLogger('defined_media')

class ReformatsErrors(object):
    def reformat_errors(self):
        '''
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
