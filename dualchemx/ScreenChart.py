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
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy, QComboBox

)
from PySide6.QtCore import (
    Qt, QSize, QSettings, QDir
)
from PySide6.QtGui import QPainter
from DualChemX import IScreen
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis, QScatterSeries

class ScreenChart(QWidget, IScreen):
    def __init__(self, p = None):
        super().__init__(p)
        IScreen.__init__(self)
        layout = QVBoxLayout()
        self.desc = None
        self.descriptors = {
                    "Molecular Weight (MW)": lambda m: m.mw,
                    "Total Polar Surface Area (TPSA)": lambda m: m.tpsa
        }
        self.dropdown = QComboBox()
        self.dropdown.addItems(list(self.descriptors.keys()))
        self.dropdown.currentIndexChanged.connect(self.onDescriptorChanged)
        self.chart_view = QChartView(QChart())
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.chart_view, 1)
        self.setLayout(layout)

    def refresh(self):
        self.onDescriptorChanged(self.dropdown.currentIndex())

    def onDescriptorChanged(self, idx):
        self.desc = self.dropdown.itemText(idx)
        self.createChart()

    def createChart(self):
        self.chart_view.setChart(QChart())
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        ext = self.descriptors[self.desc]
        data = [ext(m) for m in self.db._mols]
        if not data:
            return

        series = QScatterSeries()
        series.setName(self.desc);
        series.setMarkerShape(QScatterSeries.MarkerShapeCircle);
        series.setMarkerSize(5.0);

        for index, weight in enumerate(data):
            series.append(index + 1, weight)

        chart.addSeries(series)
        axis_x = QValueAxis()
        axis_x.setTitleText("Molecule Index")
        axis_x.setLabelFormat("%d")
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText(self.desc)
        axis_y.setLabelFormat("%.2f")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        self.chart_view.setChart(chart)

