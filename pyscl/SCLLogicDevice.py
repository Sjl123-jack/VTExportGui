class SCLLogicDevice:
    def __init__(self, attributes, reference):
        self.name = attributes['inst']
        self.desc = attributes.get('desc', '')
        self.reference = reference
        self._logic_node_list = list()

    def __iter__(self):
        return iter(self._logic_node_list)

    def __len__(self):
        return len(self._logic_node_list)

    def __repr__(self):
        return '%s:%s' % (self.reference, self.desc)

    def addLogicNode(self, logic_node):
        self._logic_node_list.append(logic_node)

    def getReference(self):
        return self.reference
