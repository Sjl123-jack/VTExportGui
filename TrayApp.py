from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json
from IedSelectDialog import IedSelectDialog
from SettingDialog import SettingDialog

config = dict()


class TrayApp(QSystemTrayIcon):
    def __init__(self, process_event=None):
        super().__init__()

        # 一些静态属性
        self.scd_file_path = ''
        self.process_event = process_event

        with open('./config.json', 'r', encoding='utf8') as configFile:
            global config
            config = json.load(configFile)

        # 设置任务栏图标
        self.setIcon(QIcon('./img/icon.png'))
        self.setVisible(True)

        # 创建Actions
        self.importScdAction = QAction('打开SCD', self)
        self.importScdAction.triggered.connect(self.importScd)
        self.settingAction = QAction('设置', self)
        self.settingAction.triggered.connect(self.setting)
        self.settingAction.setIcon(QIcon('./img/setting.png'))
        self.aboutAction = QAction('关于VTExportGui', self)
        self.aboutAction.triggered.connect(self.about)
        self.quitAction = QAction('退出', self)

        # 设置任务栏图标菜单
        tray_menu = QMenu()
        tray_menu.addAction(self.importScdAction)
        tray_menu.addAction(self.settingAction)
        tray_menu.addAction(self.aboutAction)
        tray_menu.addAction(self.quitAction)

        self.setContextMenu(tray_menu)

    # 导入SCD文件,读取SCD中的所有设备信息并提出不包含虚端子的设备
    def importScd(self):
        self.scd_file_path = QFileDialog.getOpenFileName(None, "请选择SCD文件", "", "scd文件(*.scd)")[0]
        if self.scd_file_path:
            progress_dialog = QProgressDialog('解析SCD', '取消', 0, 0)
            progress_dialog.show()
            ied_list = list()
            ied_count = 0
            with open(self.scd_file_path, encoding='utf8') as scl_file:
                has_inputs = False
                for line in scl_file:
                    if '<IED' in line:
                        ied_count += 1
                        ied_info = dict()
                        if has_inputs:
                            has_inputs = False
                        elif ied_list:
                            ied_list.pop()

                        def getItemContent(split_item):
                            return split_item.split('"')[1].strip('"')

                        for ied_info_item in line.split(' '):
                            if 'name' in ied_info_item:
                                ied_info['name'] = getItemContent(ied_info_item)
                            elif 'desc' in ied_info_item:
                                ied_info['desc'] = getItemContent(ied_info_item)
                            elif 'manufacturer' in ied_info_item:
                                ied_info['manufacturer'] = getItemContent(ied_info_item)
                            elif 'type' in ied_info_item:
                                ied_info['type'] = getItemContent(ied_info_item)
                            ied_info['regular'] = 'AppidSeq'
                        ied_list.append(ied_info)
                        progress_dialog.setLabelText('正在解析%s...' % ied_info['name'])
                        self.process_event()
                    elif not has_inputs and '<Inputs' in line:
                        has_inputs = True
                if not has_inputs:
                    ied_list.pop()
            progress_dialog.destroy()
            ied_select_dialog = IedSelectDialog(ied_list, self.scd_file_path, ied_count, self.process_event)
            ied_select_dialog.exec_()

    def setting(self):
        setting_dialog = SettingDialog()
        setting_dialog.apply_config.connect(self.refreshGlobalConfig)
        setting_dialog.exec_()

    def refreshGlobalConfig(self, config_dict):
        self.global_config = config_dict

    def about(self):
        pass
