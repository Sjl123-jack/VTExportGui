class SCLAddress:
    def __init__(self):
        self._type = None

        # 当type为ip时的相关参数
        self.ip = None
        self._ip_subnet = None

        # 当type为smv或gse时的相关参数
        self._mac_address = None
        self._vlan_id = None
        self._vlan_priority = None
        self.appid = None

    # 设置Address类型
    def setType(self, address_type):
        self._type = address_type

    # 设置IP地址
    def setIP(self, ip):
        self.ip = ip

    # 设置子网掩码
    def setIPSubnet(self, ip_subnet):
        self._ip_subnet = ip_subnet

    # 设置MAC地址
    def setMacAddress(self, mac_address):
        self._mac_address = mac_address

    # 设置VLAN ID
    def setVlanId(self, vlan_id):
        self._vlan_id = vlan_id

    # 设置VLAN PRIORITY
    def setVlanPriority(self, vlan_priority):
        self._vlan_priority = vlan_priority

    # 设置APPID
    def setAppid(self, appid):
        self.appid = appid
