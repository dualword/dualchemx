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

from PySide6.QtCore import (
    Qt, QObject, Slot, Property, Signal, QSettings, QDir, QByteArray
)

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import Descriptors

class MolCls:
    pass

class Backend(QObject):
    updated = Signal()
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, p = None):
        if self._initialized:
            return
        super().__init__(p)
        self._initialized = True
        self._mols = []
        self._index = -1
        self._smiles = ''
        self._fname = ''

    @Property(str, notify=updated)
    def fileName(self):
        if not self._fname: return ""
        return self._fname

    @Property(str, notify=updated)
    def currentSmiles(self):
        if not self._smiles: return ""
        return self._smiles

    def getSmiles(self, idx):
        return Chem.MolToSmiles(self._mols[idx].mol, isomericSmiles=True)

    @Property(int, notify=updated)
    def currentIndex(self): return self._index

    @Property(int, notify=updated)
    def totalCount(self): return len(self._mols)

    @Slot()
    def deleteAll(self):
        self._mols.clear()
        self._index = -1
        self._smiles = ''
        self._fname = ''
        self.updated.emit()

    @Slot()
    def loadSdf(self, path):
        self._mols.clear()
        #self._fname = fname
        supplier = Chem.SDMolSupplier(path)
        for mol in supplier:
            if mol is not None:
                m = MolCls()
                self.updateMol(mol, m)
                self._mols.append(m)

        self._index = 0
        self._smiles = Chem.MolToSmiles(self._mols[self._index].mol, isomericSmiles=True)
        self.updated.emit()

    @Slot()
    def addSmiles(self, str):
        mol = Chem.MolFromSmiles(str)
        if mol is not None:
            m = MolCls()
            m.mol = mol
            self.updateMol(mol, m)
            self._mols.append(m)
            self._index = len(self._mols) - 1
            self._smiles = Chem.MolToSmiles(self._mols[self._index].mol, isomericSmiles=True)
            self.updated.emit()

    @Slot()
    def nextMol(self):
        if self._index < len(self._mols) - 1:
            self._index += 1
            self._smiles = Chem.MolToSmiles(self._mols[self._index].mol, isomericSmiles=True)
            self.updated.emit()

    @Slot()
    def prevMol(self):
        if self._index > 0:
            self._index -= 1
            self._smiles = Chem.MolToSmiles(self._mols[self._index].mol, isomericSmiles=True)
            self.updated.emit()

    @Slot()
    def first(self):
        self._index = 0
        self._smiles = Chem.MolToSmiles(self._mols[self._index].mol, isomericSmiles=True)
        self.updated.emit()

    @Slot()
    def last(self):
        self._index = len(self._mols) - 1
        self._smiles = Chem.MolToSmiles(self._mols[self._index].mol, isomericSmiles=True)
        self.updated.emit()

    @Slot()
    def getMol(self):
        if self._index >= 0:
            return self._mols[self._index]

    def updateMol(self, mol, m):
        m.mol = mol
        m.formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
        m.atoms = mol.GetNumAtoms()
        m.hatoms = mol.GetNumHeavyAtoms()
        m.hetatoms = Descriptors.NumHeteroatoms(mol)
        m.bonds = mol.GetNumBonds()
        m.abonds = Descriptors.NumAmideBonds(mol)
        m.rbonds = Descriptors.NumRotatableBonds(mol)
        m.mw = Descriptors.MolWt(mol)
        m.tpsa = Descriptors.TPSA(mol)

    def getSvg(self, w, h):
        if not self._mols: return QByteArray("")
        drawer = rdMolDraw2D.MolDraw2DSVG(w, h)
        drawer.DrawMolecule(self._mols[self._index].mol)
        drawer.FinishDrawing()
        return drawer.GetDrawingText().encode('utf-8')
