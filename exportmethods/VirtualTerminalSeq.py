from .ExportMethod import ExportMethod
from functools import reduce


class VirtualTerminalSeq(ExportMethod):
    # 类的一些静态对象
    index = 0
    desc = '虚端子顺序'
    visible = True

    @staticmethod
    def generateLinkTable(iedname, scl):
        # TODO: 完善虚端子排序的相关算法
        ied = scl.getObjectByReference(iedname)
        print(ied)
