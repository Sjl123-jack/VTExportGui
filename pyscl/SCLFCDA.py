class SCLFCDA:
    def __init__(self, attributes, ied_name):
        self._ld_inst = attributes['ldInst']
        self._ln_prefix = attributes.get('prefix', '')
        self._ln_class = attributes['lnClass']
        self._ln_inst = attributes.get('lnInst', '')
        self._ln_name = '%s%s%s' % (self._ln_prefix, self._ln_class, self._ln_inst)
        self._do_name = attributes['doName']
        self._fc = attributes['fc']
        self._reference = '%s+%s/%s.%s' % (ied_name, self._ld_inst, self._ln_name, self._do_name)

    def __repr__(self):
        return self._reference
