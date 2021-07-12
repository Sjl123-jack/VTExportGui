class SCLSMVAddress:
    def __init__(self, attributes):
        self.cb_name = attributes['cbName']
        self.ld_inst = attributes['ldInst']
        self.address = None

    def setAddress(self, address):
        self.address = address
