class SCLConnectedAP:
    def __init__(self, attributes):
        self._name = attributes['apName']
        self.ied_name = attributes['iedName']
        self._desc = attributes.get('desc', '')
        self._address_list = list()
        self._smv_address_list = list()
        self._gse_address_list = list()

    def addAddress(self, address):
        self._address_list.append(address)

    def addSMVAddress(self, smv_address):
        self._smv_address_list.append(smv_address)

    def addGSEAddress(self, gse_address):
        self._gse_address_list.append(gse_address)

    def getAddressList(self):
        return self._address_list

    def getSMVAddressList(self):
        return self._smv_address_list

    def getGSEAddressList(self):
        return self._gse_address_list
