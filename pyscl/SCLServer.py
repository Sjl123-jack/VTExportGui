class SCLServer:
    def __init__(self, name):
        self.name = name
        self._logic_device_list = list()

    def __iter__(self):
        return iter(self._logic_device_list)

    def __len__(self):
        return len(self._logic_device_list)

    def addLogicDevice(self, logic_device):
        self._logic_device_list.append(logic_device)
