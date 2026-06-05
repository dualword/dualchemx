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
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtSvgWidgets import QSvgWidget
from DualChemX import IScreen
from rdkit import Chem
from rdkit.Chem import Draw
import math

class TableModel(QAbstractTableModel):
    def __init__(self, db, p=None):
        super().__init__(p)
        self.db = db
        self.cols = 3
        self.imgw = 200
        self.imgh = 200

    def rowCount(self, parent=QModelIndex()):
        return math.ceil(len(self.db._mols) / self.cols)

    def columnCount(self, parent=QModelIndex()):
        return self.cols

    def getPixmap(self, smiles):
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                img = Draw.MolToImage(mol, size=(self.imgw, self.imgh)).convert("RGBA")
                qimage = QImage(img.tobytes("raw", "RGBA"), self.imgw, self.imgh, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimage)
            else:
                pixmap = self.getEmpty("Invalid SMILES")
        except Exception:
            pixmap = self.getEmpty("Render Error")

        return pixmap

    def getEmpty(self, text):
        pix = QPixmap(self.imgw, self.imgh)
        pix.fill(Qt.lightGray)
        return pix

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        idx = (index.row() * self.cols) + index.column()

        if idx >= len(self.db._mols):
            return None

        if role == Qt.DecorationRole:
            return self.getPixmap(self.db.getSmiles(idx))

        if role == Qt.DisplayRole:
            return f"{idx+1}"

        if role == Qt.TextAlignmentRole:
            return Qt.AlignHCenter | Qt.AlignBottom

        return None

    def refresh(self):
        self.beginResetModel()
        self.endResetModel()

class ScreenGrid(QWidget, IScreen):
    def __init__(self, p = None):
        super().__init__(p)
        IScreen.__init__(self)
        layout = QVBoxLayout()
        self.tbl = QTableView(self)
        self.tbl.horizontalHeader().hide()
        self.tbl.verticalHeader().hide()
        self.tbl.setShowGrid(False)
        self.tbl.setVerticalScrollMode(QTableView.ScrollPerPixel)
        self.tbl.setHorizontalScrollMode(QTableView.ScrollPerPixel)
        self.tbl.setIconSize(QSize(200, 200))
        self.tbl.horizontalHeader().setDefaultSectionSize(220)
        self.tbl.verticalHeader().setDefaultSectionSize(240)
        self.model = TableModel(self.db, self.tbl)
        self.tbl.setModel(self.model)
        layout.addWidget(self.tbl, 1)
        self.setLayout(layout)

    def refresh(self):
        self.model.refresh()
