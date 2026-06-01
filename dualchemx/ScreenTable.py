# ###
# Copyright (C) 2026 Alexander Busorgin
# This file is part of DualChemX (https://github.com/dualword/dualchemx)
# License: GPL-3 (GPL-3.0-only)
#
# DualChemX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DualChemX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DualChemX.  If not, see <http://www.gnu.org/licenses/>.
# ###

from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTableView, QLineEdit,QSpacerItem,QSizePolicy,
    QHeaderView, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtCore import (
    Qt, QSize, QSettings, QDir, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
)
from PySide6.QtSvgWidgets import QSvgWidget
from DualChemX import IScreen

class TableModel(QAbstractTableModel):
    def __init__(self, db, p = None):
        super().__init__(p)
        self._headers = ['Num', 'Formula', 'Mol. Weight', 'TPSA']
        self.db = db

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None

    def rowCount(self, parent=QModelIndex()):
        return self.db.totalCount

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0: return index.row()+1
            if index.column() == 1: return self.db._mols[index.row()].formula
            if index.column() == 2: return self.db._mols[index.row()].mw
            if index.column() == 3: return self.db._mols[index.row()].tpsa
        return None

    def sort(self, col, ord):
        pass

    def roleNames(self):
        return {Qt.DisplayRole: b"display"}

    def refresh(self):
        self.beginResetModel()
        self.endResetModel()

class ScreenTable(QWidget, IScreen):
    def __init__(self, p = None):
        super().__init__(p)
        IScreen.__init__(self)
        layout = QVBoxLayout()
        self.tbl = QTableView(self)
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.model = TableModel(self.db, self.tbl)
        self.proxy = QSortFilterProxyModel(self.tbl)
        self.proxy.setSourceModel(self.model);
        self.tbl.setModel(self.proxy)
        layout.addWidget(self.tbl, 1)
        self.tbl.setSortingEnabled(True)
        self.tbl.sortByColumn(0, Qt.AscendingOrder)
        self.setLayout(layout)

    def refresh(self):
        self.model.refresh()

