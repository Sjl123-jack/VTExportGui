from .ExportMethod import ExportMethod
from pyscl.SCLLogicNodeZero import SCLLogicNodeZero
from PyQt5.QtWidgets import QApplication


class AppidSeq(ExportMethod):
    # 类的一些静态对象
    index = 1
    desc = 'APPID顺序'
    visible = True

    @staticmethod
    def generateLinkTable(iedname, scl):
        # TODO: 完善APPID排序的相关算法
        ied = scl.getObjectByReference(iedname)
        inputs_tuple = (list(), list(), list())
        server_type_dict = {'S1': 0, 'M1': 1, 'G1': 2}
        for server in ied:
            server_type = server.name
            for logic_device in server:
                for logic_node in logic_device:
                    if isinstance(logic_node, SCLLogicNodeZero):
                        inputs_tuple[server_type_dict.get(server_type, 0)].extend(logic_node.getExtRefList())

        def mergerInputsToDatasets(inputs):
            merge_datasets = list()
            for input_ in inputs:
                ext_ref = input_.getExtRef()
                logic_node_ref = ext_ref.split('/')[0] + '/LLN0'
                logic_node_zero = scl.getObjectByReference(logic_node_ref)
                for dataset in logic_node_zero.getDatasetList():
                    for fcda in dataset:
                        if dataset.getReference() not in merge_datasets and ext_ref == repr(fcda):
                            merge_datasets.append(dataset.getReference())
                QApplication.processEvents()
            return merge_datasets

        datasets_tuple = tuple(map(mergerInputsToDatasets, inputs_tuple))
        print(ied)
        for datasets in datasets_tuple:
            print(datasets)
