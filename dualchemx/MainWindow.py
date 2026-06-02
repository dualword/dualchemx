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
    QApplication, QMainWindow, QStackedWidget,
    QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStyle, QToolBar, QMessageBox, QFileDialog,
    QInputDialog, QLineEdit
)
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtCore import (
    QSize, QSettings, QDir
)
from ScreenBrowse import ScreenBrowse
from ScreenTable import ScreenTable
from ScreenChart import ScreenChart
from DualChemX import IScreen

class MainWindow(QMainWindow, IScreen):
    def __init__(self, p = None):
        super().__init__(p)
        IScreen.__init__(self)
        self.setWindowTitle("DualChemX")
        self.statusBar().setVisible(True)
        if QSettings().value("geom"):
            self.restoreGeometry(QSettings().value("geom"))
        else:
            self.setGeometry(100, 100, 640, 480)
        toolbar = QToolBar("toolbar")
        self.addToolBar(toolbar)
        toolbar.setMovable(False)
        button_action = QAction(self.style().standardIcon(QStyle.SP_FileDialogStart), "Load", self)
        button_action.setToolTip("Load SDF file")
        button_action.triggered.connect(self.loadSdf)
        toolbar.addAction(button_action)
        actEnter = QAction(self.style().standardIcon(QStyle.SP_FileIcon), "Enter", self)
        actEnter.setToolTip("Enter SMILES")
        actEnter.triggered.connect(self.enterSmiles)
        toolbar.addAction(actEnter)
        actEnter = QAction(self.style().standardIcon(QStyle.SP_TrashIcon), "Clear", self)
        actEnter.setToolTip("Delete All")
        toolbar.addAction(actEnter)
        toolbar.addSeparator()
        actAbout = QAction(self.style().standardIcon(QStyle.SP_FileDialogInfoView), "About", self)
        actAbout.setToolTip("About")
        actAbout.triggered.connect ( lambda: QMessageBox.about( self, "DualChemX",
        "&copy; 2026 Alexander Busorgin <br/>"
        "License: GPL-3 (GPL-3.0-only)<br/>"
        "<a href='https://github.com/dualword/dualchemx'>https://github.com/dualword/dualchemx</a><br/>")
        )
        toolbar.addAction(actAbout)
        screen1 = ScreenBrowse(self)
        screen2 = ScreenTable(self)
        screen3 = ScreenChart(self)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(screen1)
        self.stacked_widget.addWidget(screen2)
        self.stacked_widget.addWidget(screen3)
        actEnter.triggered.connect(lambda: (self.db.deleteAll(), self.statusBar().clearMessage(),
        self.stacked_widget.currentWidget().refresh()))
        menu_list = QListWidget()
        menu_list.setViewMode(QListWidget.IconMode)
        menu_list.setIconSize(QSize(64, 64))
        menu_list.setMaximumWidth(80)
        menu_list.addItem(QListWidgetItem(self.style().standardIcon(QStyle.SP_DesktopIcon), "Browse", menu_list))
        menu_list.addItem(QListWidgetItem(self.style().standardIcon(QStyle.SP_DesktopIcon), "Table", menu_list))
        menu_list.addItem(QListWidgetItem(self.style().standardIcon(QStyle.SP_DesktopIcon), "Chart", menu_list))
        menu_list.setStyleSheet("""
            QListWidget {
                width: 200px;
                background-color: #f0f0f0;
                font-size: 16px;
            }
        """)
        menu_list.itemClicked.connect(
            lambda: (index := menu_list.row(menu_list.currentItem()),
            self.stacked_widget.setCurrentIndex(index),
            self.stacked_widget.widget(index).refresh())
        )
        layout = QHBoxLayout()
        layout.addWidget(menu_list, 1)
        layout.addWidget(self.stacked_widget, 5)
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.db.updated.connect(self.stacked_widget.currentWidget().refresh)

    def closeEvent(self, event):
        QSettings().setValue("geom", self.saveGeometry())
        super().closeEvent(event)

    def loadSdf(self):
        f = QSettings().value("lastFile") if QSettings().value("lastFile") else QDir().home().path()
        path, _ = QFileDialog.getOpenFileName(None, "Open SDF", f, "SDF (*.sdf);;All Files (*)")
        if path:
            self._fname = path
            QSettings().setValue("lastFile", self._fname)
            self.db.loadSdf(path)
            self.statusBar().showMessage(path)
            self.stacked_widget.currentWidget().refresh()

    def enterSmiles(self):
        str, ok = QInputDialog.getText(self, '', "Enter SMILES", QLineEdit.Normal);
        if ok and str:
            self.db.addSmiles(str)
        self.stacked_widget.currentWidget().refresh()

