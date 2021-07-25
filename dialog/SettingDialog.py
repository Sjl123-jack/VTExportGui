from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSignal
import json
from functools import partial
from GlobalConfig import GlobalConfig
import re


class SettingDialog(QDialog):
    # 应用配置信号
    apply_config = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle('设置')
        self.setWindowIcon(QIcon('../img/setting.png'))

        # 创建Widget
        self.isExportSourceDescLabel = QLabel('是否导出源描述')
        self.isExportSourceDescCheckBox = QCheckBox()
        self.isExportSourceDescLabel.setBuddy(self.isExportSourceDescCheckBox)

        self.isRelateClassRegularLabel = QLabel('是否关联类规则')
        self.isRelateClassRegularCheckBox = QCheckBox()
        self.isRelateClassRegularLabel.setBuddy(self.isRelateClassRegularCheckBox)

        self.exportModeLabel = QLabel('导出模式      ')
        self.exportModeComboBox = QComboBox()
        self.exportModeComboBox.addItem('每个IED一个工作表')
        self.exportModeComboBox.addItem('每个厂家一个工作表')
        self.exportModeComboBox.addItem('所有IED一个工作表')
        self.exportModeLabel.setBuddy(self.exportModeComboBox)

        self.linkDescTemplateLabel = QLabel('导出模板      ')
        self.linkDescTemplateLineEdit = QLineEdit()
        self.linkDescTemplateLabel.setBuddy(self.linkDescTemplateLineEdit)

        self.checkLinkDescValidLabel = QLabel('检查导出模板是否合法')
        self.checkLinkDescValidButton = QPushButton('检查')
        self.checkLinkDescValidButton.setEnabled(False)
        self.checkLinkDescValidButton.clicked.connect(self.checkLinkDescValid)

        self.restoreDefaultConfigLabel = QLabel('恢复复默认设置      ')
        self.restoreDefaultConfigButton = QPushButton('恢复')
        self.restoreDefaultConfigButton.clicked.connect(self.restoreDefaultConfig)

        self.applyButton = QPushButton('应用')
        self.applyButton.clicked.connect(self.applyButton.setEnabled)
        self.applyButton.clicked.connect(self.applyConfig)
        self.saveButton = QPushButton('保存')
        self.saveButton.clicked.connect(self.writeConfigFile)
        self.saveButton.clicked.connect(self.saveButton.setEnabled)
        self.cancelButton = QPushButton('取消')
        self.cancelButton.clicked.connect(self.close)

        self.refreshWidget()

        # 当各个widget的内容发生改变的时候使能 应用 和 保存 按钮
        self.isExportSourceDescCheckBox.stateChanged.connect(partial(self.enableApplyAndSave, True))
        self.isRelateClassRegularCheckBox.stateChanged.connect(partial(self.enableApplyAndSave, True))
        self.exportModeComboBox.currentIndexChanged.connect(partial(self.enableApplyAndSave, True))
        self.linkDescTemplateLineEdit.textChanged.connect(partial(self.enableApplyAndSave, False))
        self.linkDescTemplateLineEdit.textChanged.connect(partial(self.checkLinkDescValidButton.setEnabled, True))

        self.applyButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        # 初始化UI
        self.initUI()

    def initUI(self):
        isExportSourceDescLayout = QHBoxLayout()
        isExportSourceDescLayout.addWidget(self.isExportSourceDescLabel)
        isExportSourceDescLayout.addWidget(self.isExportSourceDescCheckBox)
        isExportSourceDescLayout.addStretch()

        isRelateClassRegularLayout = QHBoxLayout()
        isRelateClassRegularLayout.addWidget(self.isRelateClassRegularLabel)
        isRelateClassRegularLayout.addWidget(self.isRelateClassRegularCheckBox)
        isRelateClassRegularLayout.addStretch()

        exportModeLayout = QHBoxLayout()
        exportModeLayout.addWidget(self.exportModeLabel)
        exportModeLayout.addWidget(self.exportModeComboBox)
        exportModeLayout.addStretch()

        linkDescTempalteLayout = QHBoxLayout()
        linkDescTempalteLayout.addWidget(self.linkDescTemplateLabel)
        linkDescTempalteLayout.addWidget(self.linkDescTemplateLineEdit)

        checkLinkDescValidLayout = QHBoxLayout()
        checkLinkDescValidLayout.addWidget(self.checkLinkDescValidLabel)
        checkLinkDescValidLayout.addWidget(self.checkLinkDescValidButton)
        checkLinkDescValidLayout.addStretch()

        restoreDefaultConfigLayout = QHBoxLayout()
        restoreDefaultConfigLayout.addWidget(self.restoreDefaultConfigLabel)
        restoreDefaultConfigLayout.addWidget(self.restoreDefaultConfigButton)
        restoreDefaultConfigLayout.addStretch()

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(isExportSourceDescLayout)
        mainLayout.addLayout(isRelateClassRegularLayout)
        mainLayout.addLayout(exportModeLayout)
        mainLayout.addLayout(linkDescTempalteLayout)
        mainLayout.addLayout(checkLinkDescValidLayout)
        mainLayout.addLayout(restoreDefaultConfigLayout)
        mainLayout.addStretch()
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def refreshWidget(self):
        # 根据config_dict设置各个widget属性
        if GlobalConfig.config_dict.get('isExportSourceDesc'):
            self.isExportSourceDescCheckBox.setCheckState(Qt.Checked)
        else:
            self.isExportSourceDescCheckBox.setCheckState(Qt.Unchecked)

        if GlobalConfig.config_dict.get('isRelateClassRegular'):
            self.isRelateClassRegularCheckBox.setCheckState(Qt.Checked)
        else:
            self.isRelateClassRegularCheckBox.setCheckState(Qt.Unchecked)

        self.exportModeComboBox.setCurrentIndex(GlobalConfig.config_dict.get('exportMode'))
        self.linkDescTemplateLineEdit.setText(GlobalConfig.config_dict.get('linkDescTemplate'))

    def enableApplyAndSave(self, is_enable):
        self.applyButton.setEnabled(is_enable)
        self.saveButton.setEnabled(is_enable)

    def refreshConfigDict(self):
        GlobalConfig.config_dict['isExportSourceDesc'] = self.isExportSourceDescCheckBox.isChecked()
        GlobalConfig.config_dict['isRelateClassRegular'] = self.isRelateClassRegularCheckBox.isChecked()
        GlobalConfig.config_dict['exportMode'] = self.exportModeComboBox.currentIndex()
        GlobalConfig.config_dict['linkDescTemplate'] = self.linkDescTemplateLineEdit.text()

    def checkLinkDescValid(self):
        keyword_pattern = re.compile(r'\[\w+\]')
        keyword_list = ['[InIedname]', '[InIedDesc]', '[ExIedname]', '[ExIedDesc]', '[LinkType]', '[Appid]']
        find_keyword_list = keyword_pattern.findall(self.linkDescTemplateLineEdit.text())
        if all(map(lambda x: x in keyword_list, find_keyword_list)):
            self.enableApplyAndSave(True)
        else:
            invalid_keyword_list = [keyword for keyword in find_keyword_list if keyword not in keyword_list]
            msgBox = QMessageBox()
            msgBox.setWindowTitle('警告')
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('%s均为非法字符串' % '、'.join(invalid_keyword_list))
            msgBox.exec_()

    def applyConfig(self):
        self.refreshConfigDict()
        self.apply_config.emit(GlobalConfig.config_dict)

    def writeConfigFile(self):
        self.refreshConfigDict()
        with open('cfg/config.json', 'w', encoding='utf8') as configFile:
            json.dump(GlobalConfig.config_dict, configFile, indent=True, ensure_ascii=False)

    def restoreDefaultConfig(self):
        GlobalConfig.config_dict['isExportSourceDesc'] = False
        GlobalConfig.config_dict['isRelateClassRegular'] = True
        GlobalConfig.config_dict['exportMode'] = 0
        GlobalConfig.config_dict['linkDescTemplate'] = '接收[ExIedDesc][LinkType]链路中断(0x[Appid])'
        self.refreshWidget()
        self.checkLinkDescValidButton.setEnabled(False)
        self.enableApplyAndSave(False)
        self.applyConfig()
        self.writeConfigFile()
