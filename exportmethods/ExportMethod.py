import abc


class ExportMethod(metaclass=abc.ABCMeta):
    index = None
    desc = None

    @staticmethod
    @abc.abstractmethod
    def generateLinkTable(iedname, scl):
        pass
