from .SCLLogicNode import SCLLogicNode


class SCLLogicNodeZero(SCLLogicNode):
    def __init__(self, attributes, reference):
        super().__init__(attributes, reference)
        self._dataset_list = list()
        self._gse_control_list = list()
        self._sampled_value_control_list = list()
        self._inputs = None

    def addDataset(self, dataset):
        self._dataset_list.append(dataset)

    def addGseControl(self, gse_control):
        self._gse_control_list.append(gse_control)

    def addSampledValueControl(self, sampled_value_control):
        self._sampled_value_control_list.append(sampled_value_control)

    def getDatasetList(self):
        return self._dataset_list

    def getGseControlList(self):
        return self._gse_control_list

    def getSampledValueControlList(self):
        return self._sampled_value_control_list

    def setInputs(self, inputs):
        self._inputs = inputs

    def getExtRefList(self):
        if self._inputs:
            return self._inputs.getExtRefList()
        else:
            return list()
