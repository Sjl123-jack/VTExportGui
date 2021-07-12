class SCLIED:
    def __init__(self, attributes):
        self.name = attributes['name']
        self.desc = attributes['desc']
        self.manufacturer = attributes.get('manufacturer', '')
        self.type = attributes.get('type', '')
        self._config_version = attributes.get('configVersion', '')
        self._server_list = list()
        self.reference = self.name

    def __iter__(self):
        return iter(self._server_list)

    def __repr__(self):
        return '%s:%s' % (self.reference, self.desc)

    def addServer(self, server):
        self._server_list.append(server)

    def getReference(self):
        return self.reference
