class SCLCommunication:
    def __init__(self):
        self._subnetwork_list = list()

    def __iter__(self):
        return iter(self._subnetwork_list)

    def __len__(self):
        return len(self._subnetwork_list)

    def addSubNetwork(self, subnetwork):
        self._subnetwork_list.append(subnetwork)

    def queryIPByIedname(self, ied_name):
        result_list = list()
        for subnetwork in self._subnetwork_list:
            for connected_ap in subnetwork:
                for address in connected_ap.getAddressList():
                    if connected_ap.ied_name == ied_name:
                        result_list.append((subnetwork.name, subnetwork.desc, address.ip))
        return result_list

    def queryAppidByControlBlockReference(self, control_block_reference):
        ied_name = control_block_reference.split('+')[0]
        ld_inst = control_block_reference.split('+')[1].split('/')[0]
        cb_name = control_block_reference.split('.')[-1]
        for subnetwork in self._subnetwork_list:
            for connected_ap in subnetwork:
                if connected_ap.ied_name == ied_name:
                    for smv_address in connected_ap.getSMVAddressList():
                        if smv_address.ld_inst == ld_inst and smv_address.cb_name == cb_name:
                            return smv_address.address.appid
                    for gse_address in connected_ap.getGSEAddressList():
                        if gse_address.ld_inst == ld_inst and gse_address.cb_name == cb_name:
                            return gse_address.address.appid
