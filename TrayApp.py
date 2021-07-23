from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dialog.IedSelectDialog import IedSelectDialog
from dialog.SettingDialog import SettingDialog
from GlobalConfig import GlobalConfig


class TrayApp(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        # 初始化全局设置
        GlobalConfig.readConfigFile()
        GlobalConfig.readDeviceDatabase()

        # 一些静态属性
        self.scd_file_path = ''

        # 设置任务栏图标
        self.setIcon(QIcon('img/icon.png'))
        self.setVisible(True)

        # 创建Actions
        self.importScdAction = QAction('打开SCD', self)
        self.importScdAction.triggered.connect(self.importScd)
        self.importScdAction.setIcon(QIcon('img/open.png'))
        self.settingAction = QAction('设置', self)
        self.settingAction.triggered.connect(self.setting)
        self.settingAction.setIcon(QIcon('img/setting.png'))
        self.helpAction = QAction('帮助', self)
        self.helpAction.setIcon(QIcon('img/help.png'))
        self.aboutAction = QAction('关于VTExportGui', self)
        self.aboutAction.triggered.connect(self.about)
        self.aboutAction.setIcon(QIcon('img/help.png'))
        self.quitAction = QAction('退出', self)
        self.quitAction.setIcon(QIcon('img/quit.png'))

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
                        _, ied_info['regular'] = GlobalConfig.queryDeviceDatabase(ied_info['manufacturer'],
                                                                                  ied_info['type'])
                        ied_list.append(ied_info)
                        progress_dialog.setLabelText('正在解析%s...' % ied_info['name'])
                        QApplication.processEvents()
                    elif not has_inputs and '<Inputs' in line:
                        has_inputs = True
                if not has_inputs:
                    ied_list.pop()
            progress_dialog.destroy()
            ied_select_dialog = IedSelectDialog(ied_list, self.scd_file_path, ied_count)
            ied_select_dialog.exec_()

    def setting(self):
        setting_dialog = SettingDialog()
        setting_dialog.apply_config.connect(GlobalConfig.refreshConfig)
        setting_dialog.exec_()

    def about(self):
        pass
