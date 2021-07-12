class SCLDataset:
    def __init__(self, name, desc, reference):
        self._name = name
        self.desc = desc
        self.reference = reference
        self._fcda_list = list()

    def __len__(self):
        return len(self._fcda_list)

    def __iter__(self):
        return iter(self._fcda_list)

    def __repr__(self):
        return '%s:%s' % (self.reference, self.desc)

    def addFCDA(self, fcda):
        self._fcda_list.append(fcda)

    def getReference(self):
        return self.reference
