from .ExportMethod import ExportMethod
from functools import reduce


class SieyuanSeq(ExportMethod):
    # 类的一些静态对象
    index = 2
    desc = '思源顺序'
    visible = True

    @staticmethod
    def generateLinkTable(iedname, scl):
        all_inputs = reduce(lambda x, y: x.extend(y), iedname)
        dataset_list = list()
        for input_ in all_inputs:
            pass
