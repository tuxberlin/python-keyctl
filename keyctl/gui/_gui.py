
# -*- coding: utf-8 -*-

import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QDialog
from PySide6.QtGui import QGuiApplication

from keyctl import Key


# -------------------------------------------------------------------


class AddkeyDialog(QDialog):
    def __init__(self):
        super(AddkeyDialog, self).__init__()
        here = os.path.abspath(os.path.dirname(__file__))
        uifile = os.path.join(here, 'addkey.ui')
        self.ui = QUiLoader().load(uifile)

    def get_input(self):
        return [
            self.ui.input_name.text(),
            self.ui.input_content.toPlainText()
        ]


# -------------------------------------------------------------------


class KeyringApp(QMainWindow):
    def __init__(self):
        super(KeyringApp, self).__init__()

        here = os.path.abspath(os.path.dirname(__file__))
        uifile = os.path.join(here, 'keylist.ui')
        self.ui = QUiLoader().load(uifile)

        self._init_gui_items()

        self._keylist = []
        self._refresh_table()

    def center_window(self):
        coords = QGuiApplication.primaryScreen().availableGeometry().center()
        fg = self.ui.frameGeometry()
        fg.moveCenter(coords)
        self.ui.move(fg.topLeft())

    def _init_gui_items(self):
        self.ui.btn_selectall.clicked.connect(self._selectall)
        self.ui.btn_add.clicked.connect(self._open_add_dialog)
        self.ui.btn_delete.clicked.connect(self._btn_delete)
        self.ui.btn_refresh.clicked.connect(self._refresh_table)

    def _selectall(self):
        self.ui.table1.selectAll()

    def _open_add_dialog(self):
        dialog = AddkeyDialog()
        ret = dialog.ui.exec_()
        if ret == 0:
            # cancel
            return
        elif ret == 1:
            # OK
            name, content = dialog.get_input()
            Key.add(name, content)
        else:
            print('ERROR')

        self._refresh_table()

    def _btn_delete(self):
        selected = self.ui.table1.selectionModel()
        rows = selected.selectedRows()

        for row in rows:
            idx = row.row()
            key = self._keylist[idx]
            key.delete()

        self._refresh_table()

    def _refresh_table(self):
        self._keylist = Key.list()

        self.ui.table1.setRowCount(len(self._keylist))

        for row, key in enumerate(self._keylist):
            self.ui.table1.setItem(row, 0, QTableWidgetItem(str(key.id)))
            self.ui.table1.setItem(row, 1, QTableWidgetItem(key.name))
            self.ui.table1.setItem(row, 2, QTableWidgetItem(key.data_hex))

        self.ui.table1.resizeColumnsToContents()

        self.ui.table1.clearSelection()


# -------------------------------------------------------------------
