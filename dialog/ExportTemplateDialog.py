from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class ExportTemplateDialog(QDialog):
    def __init__(self, export_type_list):
        super().__init__()
        self.export_type_set = export_type_list

        # 设置对话框属性
        self.setWindowTitle('编辑导出模板')

        self.template_table = QTableWidget()
        self.createTemplateTable()

        self.check_button = QPushButton('检查')
        self.export_button = QPushButton('导出')

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

    def createTemplateTable(self):
        self.template_table.setColumnCount(5)
        self.template_table.setRowCount(len(self.export_type_set))
        self.template_table.setHorizontalHeaderLabels(['生产厂商', '装置型号,', '站控层GOOSE模板', '过程层SV模板',
                                                       '过程层GOOSE模板'])
        self.template_table
        for index, ied_type in enumerate(self.export_type_set):
            self.template_table.setItem(index, 0, QTableWidgetItem(ied_type))
