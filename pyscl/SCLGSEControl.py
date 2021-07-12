class SCLGSEControl:
    def __init__(self, attributes, reference):
        self._name = attributes['name']
        self._dataset = attributes['datSet']
        self._reference = reference
        self._dataset_reference = reference.replace(self._name, self._dataset)

    def __repr__(self):
        return self._reference
