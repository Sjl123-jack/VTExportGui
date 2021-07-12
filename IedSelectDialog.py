from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyscl.SCL import SCL
from exportmethods import *
import xlsxwriter
from functools import reduce


class IedSelectDialog(QDialog):
    def __init__(self, ied_list, scd_file_path, ied_count, process_event=None):
        super().__init__()
        self.ied_list = ied_list
        self.scd_file_path = scd_file_path
        self.ied_count = ied_count
        self.process_event = process_event
        self.ied_table = QTableWidget()

        self.filter_item_label = QLabel("过滤选项")
        self.filter_item_combobox = QComboBox()
        self.filter_item_combobox.addItem("装置名称")
        self.filter_item_combobox.addItem("装置描述")
        self.filter_item_combobox.addItem("装置型号")
        self.filter_item_combobox.addItem("生产厂商")
        self.filter_item_combobox.currentIndexChanged.connect(self.refreshFilter)
        self.filter_item_label.setBuddy(self.filter_item_combobox)
        self.filter_lineedit = QLineEdit()
        self.filter_lineedit.setPlaceholderText("过滤器")
        self.filter_lineedit.textChanged.connect(self.refreshFilter)

        self.process_unchecked_item_btn = QPushButton("隐藏非选中项")
        self.process_unchecked_item_btn.clicked.connect(self.processUncheckedRow)
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.clicked.connect(self.selectAllVisibleRow)
        self.cancel_select_all_btn = QPushButton("取消全选")
        self.cancel_select_all_btn.clicked.connect(self.cancelSelectAllVisibleRow)
        self.export_btn = QPushButton("导出")
        self.export_btn.clicked.connect(self.exportLinkTable)
        self.quit_btn = QPushButton("退出")
        self.quit_btn.clicked.connect(self.close)

        self.statusBar = QStatusBar()
        self.current_item_count_label = QLabel("当前选中项目个数: ")
        self.current_item_count_label.setFrameShape(QFrame.WinPanel)
        self.current_item_count_label.setFrameShadow(QFrame.Sunken)
        self.statusBar.addWidget(self.current_item_count_label)
        self.checked_item_count = QLabel("0")
        self.checked_item_count.setFixedWidth(40)
        self.checked_item_count.setAlignment(Qt.AlignCenter)
        self.checked_item_count.setFrameShape(QFrame.WinPanel)
        self.checked_item_count.setFrameShadow(QFrame.Sunken)
        self.statusBar.addWidget(self.checked_item_count)
        self.operate_str = QLabel("等待")
        self.operate_str.setFrameShape(QFrame.WinPanel)
        self.operate_str.setFrameShadow(QFrame.Sunken)
        self.statusBar.addWidget(self.operate_str, 1)
        self.operate_progress = QProgressBar()
        self.operate_progress.setTextVisible(False)
        operate_progress_style = """
        QProgressBar::chunk {
            background-color: #3333FF;
            width: 10px;
            margin: 1px;
        }
        """
        self.operate_progress.setStyleSheet(operate_progress_style)
        self.operate_progress.setFixedWidth(200)
        self.statusBar.addWidget(self.operate_progress)

        self.initUI()

    def initUI(self):
        self.createIedTable()

        # 设置UI布局
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_item_label)
        filter_layout.addWidget(self.filter_item_combobox)
        filter_layout.addWidget(self.filter_lineedit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.process_unchecked_item_btn)
        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.cancel_select_all_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.quit_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.ied_table)
        main_layout.addLayout(filter_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.statusBar)

        self.setLayout(main_layout)

        # 设置对话框的一些属性
        self.setWindowTitle('导出断链表-[%s]' % self.scd_file_path)
        self.setMinimumWidth(1200)
        self.setMinimumHeight(700)

    def createIedTable(self):
        self.ied_table.setColumnCount(6)
        self.ied_table.setRowCount(len(self.ied_list))
        self.ied_table.setHorizontalHeaderLabels(['', '装置名称', '装置描述', '装置型号', '生产厂商', '排序规则'])
        self.ied_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ied_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ied_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ied_table.setColumnWidth(0, 20)
        self.ied_table.setColumnWidth(2, 360)
        self.ied_table.setColumnWidth(3, 240)

        row_num = 0
        regular_combobox_items = [export_method_class.desc for export_method_class in ExportMethod.__subclasses__()]
        for ied in self.ied_list:
            check = QTableWidgetItem()
            check.setCheckState(Qt.Unchecked)
            self.ied_table.setItem(row_num, 0, check)
            self.ied_table.setItem(row_num, 1, QTableWidgetItem(ied['name']))
            self.ied_table.setItem(row_num, 2, QTableWidgetItem(ied['desc']))
            self.ied_table.setItem(row_num, 3, QTableWidgetItem(ied['type']))
            self.ied_table.setItem(row_num, 4, QTableWidgetItem(ied['manufacturer']))
            regular_combobox = QComboBox()
            regular_combobox.addItems(regular_combobox_items)
            for export_method_class in ExportMethod.__subclasses__():
                if ied['regular'] == export_method_class.__name__:
                    regular_combobox.setCurrentIndex(export_method_class.index)
            self.ied_table.setCellWidget(row_num, 5, regular_combobox)
            row_num += 1

        self.ied_table.cellChanged.connect(self.refreshCheckedItemCount)

    def adjustSameTypeRegular(self):
        pass

    def processUncheckedRow(self):
        if self.process_unchecked_item_btn.text() == "隐藏非选中项":
            for row_num in range(self.ied_table.rowCount()):
                if not self.ied_table.item(row_num, 0).checkState():
                    self.ied_table.setRowHidden(row_num, True)
            self.process_unchecked_item_btn.setText("展开非选中项")
        else:
            for row_num in range(self.ied_table.rowCount()):
                if not self.ied_table.item(row_num, 0).checkState():
                    self.ied_table.setRowHidden(row_num, False)
            self.refreshFilter()
            self.process_unchecked_item_btn.setText("隐藏非选中项")

    def refreshFilter(self):
        column_num = self.filter_item_combobox.currentIndex() + 1
        filter_word = self.filter_lineedit.text()
        for row_num in range(self.ied_table.rowCount()):
            if filter_word != '':
                if self.ied_table.item(row_num, column_num).text().find(filter_word):
                    self.ied_table.setRowHidden(row_num, True)
                else:
                    self.ied_table.setRowHidden(row_num, False)
            else:
                self.ied_table.setRowHidden(row_num, False)

    def selectAllVisibleRow(self):
        for row_num in range(self.ied_table.rowCount()):
            if not self.ied_table.isRowHidden(row_num):
                self.ied_table.item(row_num, 0).setCheckState(Qt.Checked)
        self.refreshCheckedItemCount()

    def cancelSelectAllVisibleRow(self):
        for row_num in range(self.ied_table.rowCount()):
            if not self.ied_table.isRowHidden(row_num):
                self.ied_table.item(row_num, 0).setCheckState(Qt.Unchecked)
        self.refreshCheckedItemCount()

    def exportLinkTable(self):
        # 选择导出位置
        scd_file_name = self.scd_file_path.split('/')[-1]
        scd_file_dir = self.scd_file_path.replace(scd_file_name, '')
        default_table_file_name = scd_file_name.replace('.scd', '断链信息表.xlsx')
        default_table_file_name = default_table_file_name.replace('.scd', '断链信息表.xlsx')
        table_filepath = QFileDialog.getSaveFileName(None, "请选择导出路径", default_table_file_name,
                                                     "Microsoft Excel文件(*.xlsx)", scd_file_dir)[0]
        if table_filepath != '':
            # 解析整个个SCD获取必要的信息
            def runtime_function(ied_info):
                progress_percent = int(ied_info['index'] / self.ied_count * 80)
                progress_description = '正在解析%s...' % ied_info['name']
                self.operate_progress.setValue(progress_percent)
                self.operate_str.setText(progress_description)
                if self.process_event:
                    self.process_event()

            scl = SCL(self.scd_file_path, runtime_function)
            # 所需要导出的IED列表
            export_result = dict()
            for row_num in range(self.ied_table.rowCount()):
                if self.ied_table.item(row_num, 0).checkState():
                    iedname = self.ied_table.item(row_num, 1).text()
                    export_method_index = self.ied_table.cellWidget(row_num, 5).currentIndex()
                    for export_method_class in ExportMethod.__subclasses__():
                        if export_method_class.index == export_method_index:
                            export_result[iedname] = export_method_class.generateLinkTable(iedname, scl)

    def export_table(self, export_result, table_filepath):
        self.operate_str.setText("导出至%s..." % table_filepath)
        self.operate_progress.setValue(95)
        # 导出至Excel表格
        workbook = xlsxwriter.Workbook(table_filepath)

        # 单元格样式
        header_format = workbook.add_format({
            'align': 'center',
            'bold': 'true',
            'fg_color': '#D1D1D1'
        })
        field_format = workbook.add_format({
            'align': 'center'
        })

        for ied in export_result.values():
            worksheet = workbook.add_worksheet(ied['iedname'])
            worksheet.set_column(0, 0, width=30)
            worksheet.set_column(1, 1, width=60)
            row = 0
            for accesspoint in ied['accesspoints']:
                header = '过程层GOOSE断链表'
                linktype = 'GOOSE'
                if accesspoint['name'] == 'S1':
                    header = '站控层GOOSE断链表'
                elif accesspoint['name'] == 'M1':
                    header = '过程层SV断链表'
                    linktype = 'SV'
                worksheet.merge_range('A%s:B%s' % (row + 1, row + 1), header, header_format)
                worksheet.write(row + 1, 0, '模型源描述', field_format)
                worksheet.write(row + 1, 1, '断链信息描述', field_format)
                row += 2
                for dataset in accesspoint['extdsrefs']:
                    ex_iedname = dataset[0].split('+')[0]
                    ex_ieddesc = self.iedname_desc_map[ex_iedname]
                    replace_tuple_list = [self.export_template_lineedit.text(),
                                          ('[InIedname]', ied['iedname']),
                                          ('[InIedDesc]', ied['description']),
                                          ('[ExIedname]', ex_iedname),
                                          ('[ExIedDesc]', ex_ieddesc),
                                          ('[LinkType]',  linktype),
                                          ('[Appid]',     dataset[1])]
                    link_desc = reduce(lambda x, y: x.replace(y[0], y[1]), replace_tuple_list)
                    worksheet.write(row, 1, link_desc)
                    row += 1
                row += 1
        try:
            workbook.close()
        except Exception:
            self.refreshOperateStatus("导出失败", 95)
            QMessageBox.critical(None, "导出失败", "断链表导出至 %s 失败" % (table_filepath))
            self.operate_str.setText("等待")
            self.operate_progress.setValue(0)
            return

        QMessageBox.information(None, "导出成功", "断链表导出至 %s 成功" % (table_filepath))
        self.operate_str.setText("等待")
        self.operate_progress.setValue(0)

    def refreshCheckedItemCount(self, row=-1, column=-1):
        if column == 0:
            checked_item_count = 0
            for row_num in range(self.ied_table.rowCount()):
                if self.ied_table.item(row_num, 0).checkState() == 2:
                    checked_item_count += 1
            self.checked_item_count.setText(str(checked_item_count))

    def refreshOperateStatus(self, operate_str="等待", operate_percent=0.0):
        self.operate_str.setText(operate_str)
        self.operate_progress.setValue(int(operate_percent))
