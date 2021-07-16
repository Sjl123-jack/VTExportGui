from .SCLCommunication import SCLCommunication
from .SCLSubNetwork import SCLSubNetwork
from .SCLConnectedAP import SCLConnectedAP
from .SCLAddress import SCLAddress
from .SCLSMVAddress import SCLSMVAddress
from .SCLGSEAddress import SCLGSEAddress
from .SCLIED import SCLIED
from .SCLServer import SCLServer
from .SCLLogicDevice import SCLLogicDevice
from .SCLLogicNode import SCLLogicNode
from .SCLLogicNodeZero import SCLLogicNodeZero
from .SCLInputs import SCLInputs
from .SCLExtRef import SCLExtRef
from .SCLDataObject import SCLDataObject
from .SCLDataset import SCLDataset
from .SCLFCDA import SCLFCDA
from .SCLGSEControl import SCLGSEControl
from .SCLSampledValueControl import SCLSampledValueControl
import xml.sax


class SCLHandler(xml.sax.ContentHandler):
    def __init__(self, scl, runtime_function):
        self._cur_reference = None
        self._cur_scl = scl
        self._cur_communication = None
        self._cur_subnetwork = None
        self._cur_connected_ap = None
        self._cur_smv_address = None
        self._cur_gse_address = None
        self._cur_address = None
        self._cur_ied = None
        self._cur_ied_index = 0
        self._cur_server = None
        self._cur_logic_device = None
        self._cur_logic_node = None
        self._cur_data_object = None
        self._cur_dataset = None
        self._cur_fcda = None
        self._cur_gse_control = None
        self._cur_sampled_value_control = None
        self._cur_inputs = None
        self._cur_ext_ref = None
        self._runtime_function = runtime_function

        # 一些标志位
        self._find_du = False
        self._find_val = False
        self._find_smv_address = False
        self._find_gse_address = False
        self._find_address = False
        self._find_ip = False
        self._find_ip_subnet = False
        self._find_mac_address = False
        self._find_vlan_id = False
        self._find_vlan_priority = False
        self._find_appid = False

        # 一些缓存映射，用于快速查询
        self._dataset_control_block_dict = dict()       # <Dataset, Control Block>映射字典
        self._ied_desc_dict = dict()                    # <IED, Description>映射字典
        self._fcda_dataset_dict = dict()                # <FCDA, Dataset>映射字典
        self._data_object_desc_dict = dict()            # <DataObject, Description>映射字典
        self._data_object_unicode_desc_dict = dict()    # <DataObject, UnicodeDescription>映射字典

    def startElement(self, tag, attributes):
        if tag == 'Communication':
            self._cur_communication = SCLCommunication()
        elif tag == 'SubNetwork':
            self._cur_subnetwork = SCLSubNetwork(attributes)
        elif tag == 'ConnectedAP':
            self._cur_connected_ap = SCLConnectedAP(attributes)
        elif tag == 'SMV':
            self._find_smv_address = True
            self._cur_smv_address = SCLSMVAddress(attributes)
        elif tag == 'GSE':
            self._find_gse_address = True
            self._cur_gse_address = SCLGSEAddress(attributes)
        elif tag == 'Address':
            self._find_address = True
            self._cur_address = SCLAddress()
        elif tag == 'P':
            if self._find_smv_address:
                self._cur_address.setType('smv')
            elif self._find_gse_address:
                self._cur_address.setType('gse')
            elif self._find_address:
                self._cur_address.setType('mms')
            p_type = attributes['type']
            if p_type == 'IP':
                self._find_ip = True
            elif p_type == 'IP-SUBNET':
                self._find_ip_subnet = True
            elif p_type == 'MAC-Address':
                self._find_mac_address = True
            elif p_type == 'VLAN-ID':
                self._find_vlan_id = True
            elif p_type == 'VLAN-PRIORITY':
                self._find_vlan_priority = True
            elif p_type == 'APPID':
                self._find_appid = True
        elif tag == 'IED':
            self._cur_ied = SCLIED(attributes)
            self._cur_reference = attributes['name']
            self._cur_scl.setReferenceType(self._cur_reference, 'ied')
            self._cur_ied_index += 1
            self._ied_desc_dict[attributes['name']] = attributes['desc']
            if self._runtime_function:
                cur_ied_info = dict()
                cur_ied_info['name'] = self._cur_ied.name
                cur_ied_info['desc'] = self._cur_ied.desc
                cur_ied_info['index'] = self._cur_ied_index
                self._runtime_function(cur_ied_info)
        elif tag == 'AccessPoint':
            self._cur_server = SCLServer(attributes['name'])
        elif tag == 'LDevice':
            self._cur_reference = '%s+%s' % (self._cur_ied.getReference(), attributes['inst'])
            self._cur_logic_device = SCLLogicDevice(attributes, self._cur_reference)
            self._cur_scl.setReferenceType(self._cur_reference, 'logic_device')
        elif tag == 'LN0' or tag == 'LN':
            ln_prefix = attributes.get('prefix', '')
            ln_name = '%s%s%s' % (ln_prefix, attributes['lnClass'], attributes['inst'])
            self._cur_reference = '%s/%s' % (self._cur_logic_device.getReference(), ln_name)
            self._cur_scl.setReferenceType(self._cur_reference, 'logic_node')
            if tag == 'LN0':
                self._cur_logic_node = SCLLogicNodeZero(attributes, self._cur_reference)
            else:
                self._cur_logic_node = SCLLogicNode(attributes, self._cur_reference)
        elif tag == 'DataSet':
            self._cur_reference = '%s.%s' % (self._cur_logic_node.getReference(), attributes['name'])
            self._cur_dataset = SCLDataset(attributes['name'], attributes['desc'], self._cur_reference)
            self._cur_scl.setReferenceType(self._cur_reference, 'dataset')
        elif tag == 'GSEControl':
            self._cur_reference = '%s.%s' % (self._cur_logic_node.getReference(), attributes['name'])
            self._cur_gse_control = SCLGSEControl(attributes, self._cur_reference)
            self._cur_scl.setReferenceType(self._cur_reference, 'gse_control')
            dataset_reference = self._cur_reference.replace(self._cur_reference.split('.')[-1], attributes['datSet'])
            self._dataset_control_block_dict[dataset_reference] = self._cur_reference
        elif tag == 'SampledValueControl':
            self._cur_reference = '%s.%s' % (self._cur_logic_node.getReference(), attributes['name'])
            self._cur_sampled_value_control = SCLSampledValueControl(attributes, self._cur_reference)
            self._cur_scl.setReferenceType(self._cur_reference, 'sampled_value_control')
            dataset_reference = self._cur_reference.replace(self._cur_reference.split('.')[-1], attributes['datSet'])
            self._dataset_control_block_dict[dataset_reference] = self._cur_reference
        elif tag == 'FCDA':
            self._cur_fcda = SCLFCDA(attributes, self._cur_ied.getReference())
            self._fcda_dataset_dict[repr(self._cur_fcda)] = self._cur_dataset.getReference()
        elif tag == 'DOI':
            self._cur_reference = '%s.%s' % (self._cur_logic_node.getReference(), attributes['name'])
            self._cur_data_object = SCLDataObject(attributes['name'], attributes.get('desc'), self._cur_reference)
            self._cur_scl.setReferenceType(self._cur_reference, 'data_object')
            self._data_object_desc_dict[self._cur_reference] = attributes['name']
        elif tag == 'DAI' and attributes['name'] == 'dU':
            self._find_du = True
        elif self._find_du and tag == 'Val':
            self._find_val = True
        elif tag == 'Inputs':
            self._cur_inputs = SCLInputs()
        elif tag == 'ExtRef':
            self._cur_ext_ref = SCLExtRef(attributes)

    def characters(self, content):
        if self._find_du and self._find_val:
            self._cur_data_object.setUnicodeDesc(content)
        elif self._find_ip:
            self._cur_address.setIP(content)
        elif self._find_ip_subnet:
            self._cur_address.setIPSubnet(content)
        elif self._find_mac_address:
            self._cur_address.setMacAddress(content)
        elif self._find_vlan_id:
            self._cur_address.setVlanId(int(content, base=16))
        elif self._find_vlan_priority:
            self._cur_address.setVlanPriority(int(content))
        elif self._find_appid:
            self._cur_address.setAppid(int(content, base=16))

    def endElement(self, tag):
        if tag == 'DAI':
            self._find_du = False
        elif tag == 'Communication':
            self._cur_scl.setCommunication(self._cur_communication)
        elif tag == 'SubNetwork':
            self._cur_communication.addSubNetwork(self._cur_subnetwork)
        elif tag == 'ConnectedAP':
            self._cur_subnetwork.addConnectedAP(self._cur_connected_ap)
        elif tag == 'SMV':
            self._cur_connected_ap.addSMVAddress(self._cur_smv_address)
            self._find_smv_address = False
        elif tag == 'GSE':
            self._cur_connected_ap.addGSEAddress(self._cur_gse_address)
            self._find_gse_address = False
        elif tag == 'Address':
            self._cur_connected_ap.addAddress(self._cur_address)
            self._find_address = False
            if self._find_smv_address:
                self._cur_smv_address.setAddress(self._cur_address)
            elif self._find_gse_address:
                self._cur_gse_address.setAddress(self._cur_address)
        elif tag == 'Val':
            self._find_du = False
        elif tag == 'P':
            self._find_ip = False
            self._find_ip_subnet = False
            self._find_mac_address = False
            self._find_vlan_id = False
            self._find_vlan_priority = False
            self._find_appid = False
        elif tag == 'IED':
            self._cur_scl.addIed(self._cur_ied)
        elif tag == 'AccessPoint':
            self._cur_ied.addServer(self._cur_server)
        elif tag == 'LDevice':
            self._cur_server.addLogicDevice(self._cur_logic_device)
        elif tag == 'LN0' or tag == 'LN':
            self._cur_logic_device.addLogicNode(self._cur_logic_node)
        elif tag == 'GSEControl':
            self._cur_logic_node.addGseControl(self._cur_gse_control)
        elif tag == 'SampledValueControl':
            self._cur_logic_node.addSampledValueControl(self._cur_sampled_value_control)
        elif tag == 'DataSet':
            self._cur_logic_node.addDataset(self._cur_dataset)
        elif tag == 'FCDA':
            self._cur_dataset.addFCDA(self._cur_fcda)
        elif tag == 'Inputs':
            self._cur_logic_node.setInputs(self._cur_inputs)
        elif tag == 'ExtRef':
            self._cur_inputs.addExtRef(self._cur_ext_ref)
        elif tag == 'DOI':
            self._cur_logic_node.addDataObject(self._cur_data_object)

    def getFcdaDatasetReference(self, fcda_reference):
        return self._fcda_dataset_dict.get(fcda_reference)

    def getDatasetControlBlockReference(self, dataset_reference):
        return self._dataset_control_block_dict.get(dataset_reference)
