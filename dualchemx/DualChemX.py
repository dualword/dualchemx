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

import sys
from PySide6.QtWidgets import QApplication
from Backend import Backend

class DualChemX(QApplication):

    def __init__(self, args):
        super().__init__(args)
        self.setOrganizationName("dualword")
        self.setOrganizationDomain("dualword");
        self.setApplicationName("DualChemX")
        self.db = Backend(self)

class IScreen:
    def __init__(self):
        self.db = QApplication.instance().db
