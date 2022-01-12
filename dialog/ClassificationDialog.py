from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from functools import partial
import os
import json


class AddManufacturerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.manufacturer_label = QLabel("厂家名称")
        self.manufacturer_lineedit = QLineEdit()
        self.manufacturer_label.setBuddy(self.manufacturer_lineedit)
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(partial(self.setVisible, False))
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.close)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.manufacturer_label)
        top_layout.addWidget(self.manufacturer_lineedit)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.ok_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.cancel_button)
        bottom_layout.addStretch()
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("添加厂家")
        self.setWindowIcon(QIcon('./img/add.png'))
        self.setMinimumSize(150, 50)

    def getManufacturerName(self):
        return self.manufacturer_lineedit.text()

    def closeEvent(self, event):
        self.manufacturer_lineedit.clear()
        event.accept()


class ManufacturerTreeWidget(QTreeWidget):
    delete_manufacturer = pyqtSignal([list])

    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["厂家名称"])
        self.manufacturer_list = []
        self.manufacturer_data = {}
        self.insertTopLevelItems(0, [])

        self.pop_menu = QMenu()
        self.add_manufacturer_action = QAction("增加厂家名称")
        self.add_manufacturer_action.setIcon(QIcon("./img/add.png"))
        self.add_manufacturer_action.triggered.connect(self.addManufacturer)
        self.delete_manufacturer_action = QAction("删除厂家名称")
        self.delete_manufacturer_action.setIcon(QIcon("./img/delete.png"))
        self.delete_manufacturer_action.triggered.connect(self.deleteManufacturer)
        self.pop_menu.addActions([self.add_manufacturer_action, self.delete_manufacturer_action])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popContextMenu)

    def popContextMenu(self, pos):
        screen_pos = self.mapToGlobal(pos)
        self.pop_menu.popup(screen_pos)

    def addManufacturer(self):
        add_manufacturer_dialog = AddManufacturerDialog()
        add_manufacturer_dialog.exec()
        manufacturer_name = add_manufacturer_dialog.getManufacturerName()
        if manufacturer_name and manufacturer_name not in self.manufacturer_data.keys():
            manufacturer_item = QTreeWidgetItem([manufacturer_name])
            self.addTopLevelItem(manufacturer_item)

    def deleteManufacturer(self):
        current_item = self.currentItem()
        if current_item:
            manufacturer_list = []
            if current_item.parent() is None:
                for item_index in range(current_item.childCount()):
                    manufacturer_list.append(current_item.child(item_index).text(0))
                self.takeTopLevelItem(self.indexOfTopLevelItem(current_item))
            else:
                current_item_parent = current_item.parent()
                current_item_index = current_item_parent.indexOfChild(current_item)
                current_item_parent.takeChild(current_item_index)
                manufacturer_list.append(current_item.text(0))
            self.delete_manufacturer.emit(manufacturer_list)

    def addItemToManufacturer(self, manufacturer_item):
        current_item = self.currentItem()
        if current_item:
            if current_item.parent() is None:
                current_item.addChild(QTreeWidgetItem([manufacturer_item]))
                return True
            return False

    def dumpManufacturerData(self):
        self.manufacturer_data.clear()
        for manufacturer_index in range(self.topLevelItemCount()):
            manufacturer = self.topLevelItem(manufacturer_index)
            self.manufacturer_list.append(manufacturer.text(0))
            for manufacturer_item_index in range(manufacturer.childCount()):
                manufacturer_item = manufacturer.child(manufacturer_item_index)
                self.manufacturer_data[manufacturer_item.text(0)] = manufacturer.text(0)


class ClassificationDialog(QDialog):
    associate_complete = pyqtSignal(bool)

    def __init__(self, manufacturer_list, scd_file_path):
        super().__init__()
        self.manufacturer_list_table = QTableWidget()
        self.manufacturer_list_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.manufacturer_list_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.manufacturer_list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.manufacturer_list_table.setRowCount(len(manufacturer_list))
        self.manufacturer_list_table.setColumnCount(1)
        self.manufacturer_list_table.setHorizontalHeaderLabels(["厂家列表"])
        self.manufacturer_list_table.horizontalHeader().setStretchLastSection(True)
        for row in range(len(manufacturer_list)):
            self.manufacturer_list_table.setItem(row, 0, QTableWidgetItem(manufacturer_list[row]))

        self.scd_file_path = scd_file_path

        self.select_button = QPushButton(' >> ')
        self.select_button.clicked.connect(self.associateToManufacturer)
        self.deselect_button = QPushButton(' << ')
        self.deselect_button.clicked.connect(self.cancelAssociateFromManufacturer)

        self.classification_tree = ManufacturerTreeWidget()
        self.classification_tree.delete_manufacturer.connect(self.setManufacturerListVisible)

        self.ok_button = QPushButton("确定")
        self.ok_button.setEnabled(False)
        self.associate_complete.connect(self.ok_button.setEnabled)
        self.ok_button.clicked.connect(self.saveManufacturerCache)
        self.ok_button.clicked.connect(self.classification_tree.dumpManufacturerData)
        self.ok_button.clicked.connect(partial(self.setResult, True))
        self.ok_button.clicked.connect(partial(self.setVisible, False))

        self.initUI()
        self.loadRegularCache()

    def initUI(self):
        button_layout = QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.select_button)
        button_layout.addStretch()
        button_layout.addWidget(self.deselect_button)
        button_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.manufacturer_list_table)
        top_layout.addLayout(button_layout)
        top_layout.addWidget(self.classification_tree)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.ok_button)
        bottom_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.setMinimumHeight(500)
        self.setFixedWidth(600)
        self.setWindowIcon(QIcon("./img/classification.png"))
        self.setWindowTitle("厂家分组")

    def associateToManufacturer(self):
        current_row = self.manufacturer_list_table.currentRow()
        manufacturer_item = self.manufacturer_list_table.item(current_row, 0).text()
        if self.classification_tree.addItemToManufacturer(manufacturer_item):
            self.manufacturer_list_table.setRowHidden(current_row, True)
            self.isAssociateComplete()

    def cancelAssociateFromManufacturer(self):
        current_item = self.classification_tree.currentItem()
        if current_item is not None and current_item.parent() is not None:
            self.classification_tree.deleteManufacturer()

    def setManufacturerListVisible(self, manufacturer_list):
        for manufacturer_index in range(self.manufacturer_list_table.rowCount()):
            if self.manufacturer_list_table.item(manufacturer_index, 0).text() in manufacturer_list:
                self.manufacturer_list_table.setRowHidden(manufacturer_index, False)
                self.isAssociateComplete()

    def getManufacturerData(self):
        return self.classification_tree.manufacturer_list, self.classification_tree.manufacturer_data

    def isAssociateComplete(self):
        for row in range(self.manufacturer_list_table.rowCount()):
            if not self.manufacturer_list_table.isRowHidden(row):
                self.associate_complete.emit(False)
                return
        self.associate_complete.emit(True)

    def closeEvent(self, event):
        if QMessageBox.question(None, "确认退出", "是否确认退出导出断链信息表？") == QMessageBox.Yes:
            self.setResult(False)
            event.accept()
        else:
            event.ignore()

    # 保存厂家分类缓存
    def saveManufacturerCache(self):
        scd_file_name = os.path.basename(self.scd_file_path)
        with open('scd_cache/%s_manufacturer.json' % scd_file_name, 'w', encoding='utf8') as manufacturer_cache:
            json.dump(self.classification_tree.manufacturer_data, manufacturer_cache, indent=True, ensure_ascii=False)

    # 加载规则缓存
    def loadRegularCache(self):
        scd_file_name = os.path.basename(self.scd_file_path)
        cache_file_path = "scd_cache/%s_manufacturer.json" % scd_file_name
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r', encoding='utf8') as regular_cache:
                self.classification_tree.manufacturer_data = json.load(regular_cache)
