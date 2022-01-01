class SCLSubNetwork:
    def __init__(self, attributes):
        self.name = attributes['name']
        self.desc = attributes.get('desc', '')
        self._type = attributes.get('type', '')
        self._connected_ap_list = list()

    def __iter__(self):
        return iter(self._connected_ap_list)

    def __len__(self):
        return len(self._connected_ap_list)

    def addConnectedAP(self, connected_ap):
        self._connected_ap_list.append(connected_ap)
