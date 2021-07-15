import xml.sax
from .SCLLogicNodeZero import SCLLogicNodeZero
from .SCLHandler import SCLHandler


class SCL:
    def __init__(self, ied_file_path, runtime_function=None):
        self._communication = None
        self._ied_list = list()
        self._reference_type_dict = dict()
        parser = xml.sax.make_parser()
        self.handler = SCLHandler(self, runtime_function)
        parser.setContentHandler(self.handler)
        parser.parse(ied_file_path)

    def __iter__(self):
        return iter(self._ied_list)

    def __len__(self):
        return len(self._ied_list)

    def addIed(self, ied):
        self._ied_list.append(ied)

    def setCommunication(self, communication):
        self._communication = communication

    def setReferenceType(self, reference, reference_type):
        reference_type_list = ['ied', 'logic_device', 'logic_node', 'dataset', 'sampled_value_control',
                               'gse_control', 'data_object']
        if reference_type in reference_type_list:
            self._reference_type_dict[reference] = reference_type
            return True
        else:
            return False

    def queryReferenceType(self, reference):
        return self._reference_type_dict.get(reference)

    def queryIedInfoByName(self, ied_name):
        for ied in self._ied_list:
            if ied.name == ied_name:
                return ied.name, ied.desc, ied.type, ied.manufacturer

    def queryDescriptionByReference(self, reference):
        reference_type = self.queryReferenceType(reference)
        if not reference_type:
            return False
        else:
            for ied in self._ied_list:
                if reference_type == 'ied':
                    if ied.reference == reference:
                        return ied.desc
                else:
                    for server in ied:
                        for logic_device in server:
                            if reference_type == 'logic_device':
                                if logic_device.reference == reference:
                                    return ied.desc, logic_device.desc
                            for logic_node in logic_device:
                                if reference_type == 'logic_node':
                                    if logic_node.reference == reference:
                                        return ied.desc, logic_device.desc, logic_node.desc
                                for data_object in logic_node:
                                    if reference_type == 'data_object':
                                        if data_object.reference == reference:
                                            return ied.desc, logic_device.desc, logic_node.desc, data_object.desc
                                if type(logic_node) == SCLLogicNodeZero:
                                    for dataset in logic_node.getDatasetList():
                                        if reference_type == 'dataset':
                                            if dataset.reference == reference:
                                                return ied.desc, logic_device.desc, logic_node.desc, dataset.desc
                                    for sampled_value_control in logic_node.getSampledValueControlList():
                                        if reference_type == 'sampled_value_control':
                                            if sampled_value_control.reference == reference:
                                                return ied.desc, logic_device.desc, logic_node.desc, \
                                                       sampled_value_control.desc
                                    for gse_control in logic_node.getGseControlList():
                                        if reference_type == 'gse_control':
                                            if gse_control.reference == reference:
                                                return ied.desc, logic_device.desc, logic_node.desc, gse_control.desc

    def queryControlBlockCommunicationParameter(self, reference):
        if self.queryReferenceType(reference) == 'sampled_value_control':
            pass
        elif self.queryReferenceType(reference) == 'gse_control':
            pass

    def getObjectByReference(self, reference):
        reference_type = self.queryReferenceType(reference)
        if not reference_type:
            return False
        else:
            for ied in self._ied_list:
                if reference_type == 'ied':
                    if ied.reference == reference:
                        return ied
                else:
                    for server in ied:
                        for logic_device in server:
                            if reference_type == 'logic_device':
                                if logic_device.reference == reference:
                                    return logic_device
                            for logic_node in logic_device:
                                if reference_type == 'logic_node':
                                    if logic_node.reference == reference:
                                        return logic_node
                                for data_object in logic_node:
                                    if reference_type == 'data_object':
                                        if data_object.reference == reference:
                                            return data_object
                                if type(logic_node) == SCLLogicNodeZero:
                                    for dataset in logic_node.getDatasetList():
                                        if reference_type == 'dataset':
                                            if dataset.reference == reference:
                                                return dataset
                                    for sampled_value_control in logic_node.getSampledValueControlList():
                                        if reference_type == 'sampled_value_control':
                                            if sampled_value_control.reference == reference:
                                                return sampled_value_control
                                    for gse_control in logic_node.getGseControlList():
                                        if reference_type == 'gse_control':
                                            if gse_control.reference == reference:
                                                return gse_control

    def getFcdaDatasetReference(self, fcda_reference):
        return self.handler.getFcdaDatasetReference(fcda_reference)
