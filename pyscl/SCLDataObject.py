class SCLDataObject:
    def __init__(self, name, desc, reference):
        self._name = name
        self.desc = desc
        self.reference = reference
        self._unicode_desc = None

    def setUnicodeDesc(self, unicode_desc):
        self._unicode_desc = unicode_desc

    def __repr__(self):
        return '%s:%s' % (self.reference, self.desc)
