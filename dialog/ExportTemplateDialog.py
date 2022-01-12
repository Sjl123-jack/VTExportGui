from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
import re
import os
import json
from functools import partial


class ExportTemplateDialog(QDialog):
    def __init__(self, export_type_list, type_mask_dict, ied_example_dict, scd_file_path):
        super().__init__()
        self.export_type_list = export_type_list
        self.type_mask_dict = type_mask_dict
        self.ied_example_dict = ied_example_dict
        self.scd_file_path = scd_file_path

        # 设置对话框属性
        self.setWindowTitle('编辑导出模板')

        self.template_table = QTableWidget()
        self.createTemplateTable()

        self.check_button = QPushButton('检查')
        self.check_button.clicked.connect(self.checkTemplateStr)
        self.export_button = QPushButton('导出')
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.saveTemplateCache)
        self.export_button.clicked.connect(partial(self.setResult, True))
        self.export_button.clicked.connect(partial(self.setVisible, False))
        self.template_table.itemChanged.connect(partial(self.export_button.setEnabled, False))

        self.initUI()

    def initUI(self):
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.check_button)
        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.template_table)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowIcon(QIcon("./img/edit.png"))
        self.setMinimumHeight(500)

    def createTemplateTable(self):
        self.template_table.setColumnCount(5)
        self.template_table.setRowCount(len(self.export_type_list))
        self.template_table.setHorizontalHeaderLabels(['装置指纹', '示例IED', '站控层GOOSE模板', '过程层SV模板',
                                                       '过程层GOOSE模板'])
        self.template_table.horizontalHeader().setStretchLastSection(True)
        column_mask = 0
        for index, ied_type in enumerate(self.export_type_list):
            self.template_table.setItem(index, 0, QTableWidgetItem(ied_type))
            current_item = self.template_table.item(index, 0)
            current_item.setFlags(current_item.flags() & ~Qt.ItemIsEditable)
            self.template_table.setItem(index, 1, QTableWidgetItem(self.ied_example_dict[ied_type]))
            current_item = self.template_table.item(index, 1)
            current_item.setFlags(current_item.flags() & ~Qt.ItemIsEditable)
            for column_index in range(2, 5):
                self.template_table.setItem(index, column_index, QTableWidgetItem(''))
            unzip_type_mask = tuple(map(lambda x: self.type_mask_dict[ied_type] & x, [0x04, 0x02, 0x01]))
            column_mask |= self.type_mask_dict[ied_type]
            for column_index, editable_flag in enumerate(unzip_type_mask):
                current_item = self.template_table.item(index, column_index+2)
                if not editable_flag:
                    current_item.setBackground(QColor("lightGray"))
                    current_item.setFlags(current_item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsEnabled)
        self.loadTemplateCache()
        unzip_column_mask = tuple(map(lambda x: column_mask & x, [0x04, 0x02, 0x01]))
        column_count = 3
        for column_index, column_hide_flag in enumerate(unzip_column_mask):
            self.template_table.setColumnHidden(column_index+2, not column_hide_flag)
            if not column_hide_flag:
                column_count -= 1
        dialog_width = 1100 - (3 - column_count) * 200
        self.setMinimumWidth(dialog_width)
        column_width = (dialog_width - 410) // column_count
        self.template_table.setColumnWidth(0, 250)
        self.template_table.setColumnWidth(1, 100)
        self.template_table.setColumnWidth(2, column_width)
        self.template_table.setColumnWidth(3, column_width)
        self.template_table.setColumnWidth(4, column_width)

    def getTemplateDict(self):
        template_dict = dict()
        row_count = self.template_table.rowCount()
        for row_index in range(row_count):
            ied_fingerprint = self.template_table.item(row_index, 0).text()
            template_tuple = tuple(map(lambda x: self.template_table.item(row_index, x).text(), [1, 2, 3]))
            template_dict[ied_fingerprint] = template_tuple
        return template_dict

    def checkTemplateStr(self):
        all_replace_str_valid = True
        for row_index in range(self.template_table.rowCount()):
            replace_pattern = re.compile(r"\[.*\]")
            for column_index in range(1, self.template_table.columnCount()):
                current_item = self.template_table.item(row_index, column_index)
                current_item_text = current_item.text()
                replace_str_list = replace_pattern.findall(current_item_text)
                if current_item_text and replace_str_list:
                    for replace_str in replace_str_list:
                        is_replace_str_valid = re.match(r"\[num,[01],[1-4]\]", replace_str)
                        if not is_replace_str_valid:
                            self.template_table.item(row_index, column_index).setBackground(QColor("red"))
                            all_replace_str_valid = False
                        else:
                            self.template_table.item(row_index, column_index).setBackground(QColor("white"))
        if all_replace_str_valid:
            QMessageBox.information(None, "校验成功", "校验成功，请点击导出按钮!")
            self.export_button.setEnabled(True)
        else:
            QMessageBox.critical(None, "校验错误", "存在模板字符串错误，请检查红色单元格!")

    def closeEvent(self, event):
        if QMessageBox.question(None, "确认退出", "是否确认退出导出断链信息表？") == QMessageBox.Yes:
            self.setResult(False)
            event.accept()
        else:
            event.ignore()

    # 保存模板缓存
    def saveTemplateCache(self):
        template_dict = {}
        for row_index in range(self.template_table.rowCount()):
            ied_fingerprint = self.template_table.item(row_index, 0).text()
            template_tuple = tuple(map(lambda x: self.template_table.item(row_index, x).text(), range(2, 5)))
            template_dict[ied_fingerprint] = template_tuple
        scd_file_name = os.path.basename(self.scd_file_path)
        with open('scd_cache/%s_template.json' % scd_file_name, 'w', encoding='utf8') as regular_cache:
            json.dump(template_dict, regular_cache, indent=True, ensure_ascii=False)

    # 加载模板缓存
    def loadTemplateCache(self):
        scd_file_name = os.path.basename(self.scd_file_path)
        cache_file_path = "scd_cache/%s_template.json" % scd_file_name
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r', encoding='utf8') as template_cache:
                template_dict = json.load(template_cache)
            for row_index in range(self.template_table.rowCount()):
                ied_fingerprint = self.template_table.item(row_index, 0).text()
                if ied_fingerprint in template_dict.keys():
                    self.template_table.item(row_index, 2).setText(template_dict[ied_fingerprint][0])
                    self.template_table.item(row_index, 3).setText(template_dict[ied_fingerprint][1])
                    self.template_table.item(row_index, 4).setText(template_dict[ied_fingerprint][2])
