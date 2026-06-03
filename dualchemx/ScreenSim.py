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
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTableWidget, QLineEdit,QSpacerItem,QSizePolicy,
    QHeaderView, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtCore import (
    Qt, QSize, QSettings, QDir
)
from PySide6.QtSvgWidgets import QSvgWidget
from DualChemX import IScreen

class ScreenSim(QWidget, IScreen):
    def __init__(self, p = None):
        super().__init__(p)
        IScreen.__init__(self)
        layout = QVBoxLayout()
        self.txtSmiles = QLineEdit()
        self.txtSmiles.setReadOnly(True)
        self.txtSmiles.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.txtSmiles)
        hlayout = QHBoxLayout()
        self.svg = QSvgWidget()
        hlayout.addWidget(self.svg,1)
        self.tbl = QTableWidget(self)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list1 = ['Property', 'Value']
        self.tbl.setColumnCount(len(self.list1))
        self.tbl.setHorizontalHeaderLabels(self.list1);
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        hlayout.addWidget(self.tbl, 1)
        self.btnFirst = QPushButton("<<")
        self.btnPrev = QPushButton("<")
        self.txtNum = QLineEdit()
        self.txtNum.setReadOnly(True)
        self.txtNum.setMaxLength(10)
        self.txtNum.setAlignment(Qt.AlignHCenter)
        self.btnNext = QPushButton(">")
        self.btnLast = QPushButton(">>")
        self.btnFirst.clicked.connect(self.db.first)
        self.btnPrev.clicked.connect(self.db.prevMol)
        self.btnNext.clicked.connect(self.db.nextMol)
        self.btnLast.clicked.connect(self.db.last)
        btnLayout = QHBoxLayout()
        btnLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        btnLayout.addWidget(self.btnFirst)
        btnLayout.addWidget(self.btnPrev)
        btnLayout.addWidget(self.txtNum)
        btnLayout.addWidget(self.btnNext)
        btnLayout.addWidget(self.btnLast)
        btnLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addLayout(hlayout)
        layout.addLayout(btnLayout)
        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        self.txtSmiles.setText(self.db.currentSmiles)
        self.txtNum.setText(str(self.db.currentIndex + 1) + '/' + str(self.db.totalCount))
        self.svg.load(self.db.getSvg(self.svg.width(), self.svg.height()))
        self.btnFirst.setEnabled(self.db.currentIndex > 0)
        self.btnPrev.setEnabled(self.db.currentIndex > 0)
        self.btnNext.setEnabled(self.db.currentIndex < self.db.totalCount - 1)
        self.btnLast.setEnabled(self.db.currentIndex < self.db.totalCount - 1)
        self.updateTable()

    def updateTable(self):
        self.tbl.setRowCount(0)
        mol = self.db.getMol()
        if not mol:
            return
        self.createRow("Formula", mol.formula)
        self.createRow("Atoms", str(mol.atoms))
        self.createRow("Heavy Atoms", str(mol.hatoms))
        self.createRow("Heteroatoms", str(mol.hetatoms))
        self.createRow("Bonds", str(mol.bonds))
        self.createRow("Amide Bonds", str(mol.abonds))
        self.createRow("Rotatable Bonds", str(mol.rbonds))
        self.createRow("Mol. weight", f"{mol.mw:.2f}")
        self.createRow("TPSA", f"{mol.tpsa:.2f}")

    def createRow(self, col, val):
        row = self.tbl.rowCount()
        self.tbl.insertRow(row)
        self.tbl.setItem(row, 0, QTableWidgetItem(col))
        self.tbl.setItem(row, 1, QTableWidgetItem(val))


