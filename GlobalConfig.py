import json
import csv


class GlobalConfig:
    config_dict = dict()
    manufacturer_dict = dict()
    device_dict = dict()

    @staticmethod
    def readConfigFile():
        with open('cfg/config.json', 'r', encoding='utf8') as configFile:
            GlobalConfig.config_dict = json.load(configFile)

    @staticmethod
    def readDeviceDatabase():
        with open('cfg/devicecfg.csv', encoding='utf8') as device_cfg:
            device_cfg_csv = csv.reader(device_cfg)
            for row in device_cfg_csv:
                if row[0] != '厂家标识':
                    device_fingerprint = '[%s]-[%s]' % (row[0], row[1])
                    GlobalConfig.device_dict[device_fingerprint] = tuple(row[2:4])

        with open('cfg/manufacturercfg.csv', encoding='utf8') as manufacturer_cfg:
            manufacturer_cfg_csv = csv.reader(manufacturer_cfg)
            for row in manufacturer_cfg_csv:
                if row[0] != '厂家标识':
                    GlobalConfig.manufacturer_dict[row[0]] = row[1]

    @staticmethod
    def queryDeviceDatabase(manufacturer, type_):
        device_fingerprint = '[%s]-[%s]' % (manufacturer, type_)
        if GlobalConfig.device_dict.get(device_fingerprint) is not None:
            return GlobalConfig.device_dict.get(device_fingerprint)
        elif GlobalConfig.manufacturer_dict.get(manufacturer) is not None:
            return ('', '', ''), GlobalConfig.manufacturer_dict.get(manufacturer)
        else:
            return ('', '', ''), GlobalConfig.manufacturer_dict.get('Default')

    @staticmethod
    def refreshConfig():
        pass
