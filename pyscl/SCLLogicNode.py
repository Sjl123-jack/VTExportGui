class SCLLogicNode:
    def __init__(self, attributes, reference):
        self._prefix = attributes.get('prefix', '')
        self._ln_class = attributes.get('lnClass')
        self._inst = attributes['inst']
        self._name = '%s%s%s' % (self._prefix, self._ln_class, self._inst)
        self.desc = attributes.get('desc', '')
        self.reference = reference
        self._data_object_list = list()

    def __iter__(self):
        return iter(self._data_object_list)

    def __repr__(self):
        return '%s:%s' % (self.reference, self.desc)

    def addDataObject(self, data_object):
        self._data_object_list.append(data_object)

    def getReference(self):
        return self.reference
