import reprlib


class SCLExtRef:
    def __init__(self, attributes):
        # 从XML文件中读取原始值并拼接一些常用字符串
        self.daName = attributes.get('daName')     # 数据属性 Data Attribute 名称
        self.doName = attributes['doName']         # 数据对象 Data Object 名称
        self.iedName = attributes['iedName']       # 智能电子设备 Intelligent Electric Device 名称
        self.ldInst = attributes['ldInst']         # 逻辑设备 Logic Device 名称
        self.lnClass = attributes['lnClass']       # 逻辑节点 Logic Node 类型
        self.lnInst = attributes['lnInst']         # 逻辑节点 Logic Node 实例
        self.prefix = attributes['prefix']         # 逻辑节点 Logic Node 前缀
        # 生成逻辑节点 Logic Node 名称
        self.lnName = '%s%s%s' % (self.prefix, self.lnClass, self.lnInst)
        self.intAddr = attributes['intAddr']       # 内部地址 Internal Address 参引
        # 判断是否配置接受端口，如果配置将其剥离出来
        if ':' in self.intAddr:
            self.recvPort = self.intAddr.split(':')[0]
            self.intAddr = self.intAddr.split(':')[1]
        else:
            self.recvPort = None

    # 获取外部设备的参引
    def getExtRef(self):
        if self.daName is None:
            return '%s+%s/%s.%s' % (self.iedName, self.ldInst, self.lnName, self.doName)
        else:
            return '%s+%s/%s.%s.%s' % (self.iedName, self.ldInst, self.lnName, self.doName, self.daName)

    def __repr__(self):
        return '%s -> %s' % (reprlib.repr(self.getExtRef()), reprlib.repr(self.intAddr))
