from .ExportMethod import ExportMethod
from pyscl.SCLLogicNodeZero import SCLLogicNodeZero


class SieyuanSeq(ExportMethod):
    # 类的一些静态对象
    index = 2
    desc = '思源顺序'
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
            # 先对虚端子按照iedname归并
            external_ied_dict = dict()
            ied_index = 0
            for input_ in inputs:
                external_ied_name = input_.getExtRef().split('+')[0]
                if external_ied_name not in external_ied_dict.keys():
                    external_ied_dict[external_ied_name] = ied_index
                    ied_index += 1
            inputs.sort(key=lambda x: external_ied_dict[x.getExtRef().split('+')[0]])

            merge_datasets = list()
            for input_ in inputs:
                ext_ref = input_.getExtRef()
                dataset_reference = scl.getFcdaDatasetReference(ext_ref)
                if dataset_reference and dataset_reference not in merge_datasets:
                    merge_datasets.append(dataset_reference)
            return merge_datasets

        datasets_tuple = tuple(map(mergerInputsToDatasets, inputs_tuple))
        return datasets_tuple
