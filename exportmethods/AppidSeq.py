from .ExportMethod import ExportMethod
from pyscl.SCLLogicNodeZero import SCLLogicNodeZero


class AppidSeq(ExportMethod):
    # 类的一些静态对象
    index = 1
    desc = 'APPID顺序'
    visible = True

    @staticmethod
    def generateLinkTable(iedname, scl):
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
                dataset_reference = scl.getFcdaDatasetReference(ext_ref)
                if dataset_reference and dataset_reference not in merge_datasets:
                    merge_datasets.append(dataset_reference)
            return merge_datasets
        datasets_tuple = tuple(map(mergerInputsToDatasets, inputs_tuple))
        for datasets in datasets_tuple:
            datasets.sort(key=lambda x: scl.getAppidByDatasetReference(x))

        return datasets_tuple
