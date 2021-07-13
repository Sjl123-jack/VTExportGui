class SCLInputs:
    def __init__(self):
        self._ext_ref_list = list()

    def __len__(self):
        return len(self._ext_ref_list)

    def __iter__(self):
        return iter(self._ext_ref_list)

    def addExtRef(self, ext_ref):
        self._ext_ref_list.append(ext_ref)

    def getExtRefList(self):
        return self._ext_ref_list
