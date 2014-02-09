import logging
import django.forms as forms
from defined_media.models import MediaNames, Compounds

log=logging.getLogger(__name__)

class MediaNamesForm(forms.Form):
    @classmethod                # why can't we just MediaNamesForm(gd)?  Because we need to follow lists
    def from_media_name(self, mn):
        return MediaNamesForm(mn.as_dict())
            
    medid=forms.IntegerField(required=False, widget=forms.HiddenInput)
    media_name=forms.CharField(label='Name', required=True)
    is_defined=forms.CharField(label='Is defined?', widget=forms.CheckboxInput)
    is_minimal=forms.CharField(label='Is minimal?', widget=forms.CheckboxInput) # we don't actually display this in the template, because it's always 'Y'

    def __init__(self, *args, **kwargs):
        super(MediaNamesForm,self).__init__(*args, **kwargs)
        self.media_compounds_list=[]

        # attempt to add form fields if args[0] is a MediaNames object:
        try:
            try:
                mn=args[0]
                d=mn.as_dict()
                self.mn=mn
                log.debug('got args from mn %s' % mn)
            except AttributeError:
                d=args[0]
                log.debug('got args from args[0]')
            n=1
            for k,v in d.items():
                if k.startswith('comp'):
                    comp_name=v
                    amount_key=re.sub('comp', 'amount', k)
                    try: amount=d[amount_key]
                    except KeyError: amount=''
                    self._add_medcomp_field(n, comp_name, amount)
                    n+=1

        except Exception as e:  # nevermind, maybe args[0] wasn't a MediaNames object or something
            log.debug('MediaNamesForm.__init__(): ignoring %s: %s' % (type(e), e))
            log.exception(e)

        # if nothing happened, we need to at least create the first compound/amount CharFields:
        if 'comp1' not in self.fields:
            self._add_medcomp_field(1, '', '')

    def _add_medcomp_field(self, n, comp_name, amount):
        ''' add a form field for a comp/amount pair '''
        self.fields['comp%d' % n]=forms.CharField(label='Compound %d' % n, required=False, initial=comp_name)
        self.media_compounds_list.append({'comp': comp_name, 'amount': amount})
        self.fields['amount%d' % n]=forms.FloatField(label='Amount', required=False, initial=amount)
        log.debug('form.medcomp field added: %s-%s' %(comp_name, amount))
        

    def is_valid(self):
        valid=super(MediaNamesForm, self).is_valid()

        def _compkeys(self):
            return [k for k in self.cleaned_data.keys() if k.startswith('comp')]
            
        # check that compounds are known
        # for each compound that exists, make sure it has an amount field
        for compkey in _compkeys(self):
            comp_name=self.cleaned_data.get(compkey)
            if comp_name is None or len(comp_name)==0:
                continue
            try:
                comp=Compounds.objects.with_name(comp_name)
            except Compounds.DoesNotExist:
                self.errors[compkey]='Unknown compound "%s"' % comp_name
                log.debug('%s: Unknown compound "%s"' % (compkey, comp_name))
                valid=False

            amt_key='amount'+compkey.split('comp')[1]
            amount=self.cleaned_data.get(amt_key)
            if amount is None:
                err_msg='%s: missing or invalid amount for compound "%s"' % (compkey, comp_name)
                self.errors[amt_key]=err_msg
                log.debug(err_msg)
                valid=False

        log.debug('form.is_valid() returning %s' % valid)
        for k,v in self.errors.items():
            log.debug('form.errors[%s]=%s' % (k,v))
        return valid
