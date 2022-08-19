# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :: Welcome to PipeCAD!                                      ::
# ::  ____                        ____     ______  ____       ::
# :: /\  _`\   __                /\  _`\  /\  _  \/\  _`\     ::
# :: \ \ \L\ \/\_\  _____      __\ \ \/\_\\ \ \L\ \ \ \/\ \   ::
# ::  \ \ ,__/\/\ \/\ '__`\  /'__`\ \ \/_/_\ \  __ \ \ \ \ \  ::
# ::   \ \ \/  \ \ \ \ \L\ \/\  __/\ \ \L\ \\ \ \/\ \ \ \_\ \ ::
# ::    \ \_\   \ \_\ \ ,__/\ \____\\ \____/ \ \_\ \_\ \____/ ::
# ::     \/_/    \/_/\ \ \/  \/____/ \/___/   \/_/\/_/\/___/  ::
# ::                  \ \_\                                   ::
# ::                   \/_/                                   ::
# ::                                                          ::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# PipeCAD - Piping Design Software.
# Copyright (C) 2021 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 11:43 2021-09-25

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *


class SpwlDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Create Specification World"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel("Name")
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelPurpose = QLabel("Purpose")
        self.comboPurpose = QComboBox()
        #self.comboPurpose.setEditable(True)
        self.comboPurpose.addItem("PIPE")
        self.comboPurpose.addItem("STL")
        self.comboPurpose.addItem("NOZZ")
        self.comboPurpose.addItem("BOLT")
        self.comboPurpose.addItem("EQUI")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        try:
            PipeCad.StartTransaction("Create SPWL")
            PipeCad.CreateItem("SPWL", aName)
            aSpwlItem = PipeCad.CurrentItem()
            aSpwlItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# SpwlDialog

# Singleton Instance.
aSpwlDlg = SpwlDialog(PipeCad)

def CreateSpwl():
    aSpwlDlg.show()
# CreateSpwl

class CreateDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Create Specification"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel("Name")
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelPurpose = QLabel("Purpose")
        self.comboPurpose = QComboBox()
        self.comboPurpose.setEditable(True)
        self.comboPurpose.addItem("PIPE")
        self.comboPurpose.addItem("STL")
        self.comboPurpose.addItem("NOZZ")
        self.comboPurpose.addItem("EQUI")
        self.comboPurpose.addItem("BOLT")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        try:
            PipeCad.StartTransaction("Build Spec")

            PipeCad.CreateItem("SPEC", aName)
            aSpecItem = PipeCad.CurrentItem()
            aSpecItem.Purpose = aPurpose
            
            aDatabase = QSqlDatabase.addDatabase("QSQLITE", "PipeStd_SPEC")
            aDatabase.setDatabaseName("catalogues/PipeStd.db")
            aDatabase.open()

            self.queryModel = QSqlQueryModel()
            self.queryModel.setQuery("SELECT type, name FROM HEAD WHERE purpose='" + aPurpose + "'", aDatabase)

            for i in range(self.queryModel.rowCount()):
                aRecord = self.queryModel.record(i)
                aGtype = aRecord.value("type")
                aType = aRecord.value("name")

                PipeCad.SetCurrentItem(aSpecItem)
                PipeCad.CreateItem("SELE", aName + "/" + aGtype)
                aSeleItem = PipeCad.CurrentItem()
                aSeleItem.Description = aType
                aSeleItem.Question = "TYPE"
                aSeleItem.Answer = aGtype

            PipeCad.CommitTransaction()            
        except Exception as e:
            raise e
        # try

        self.textName.setText("")

        QDialog.accept(self)
    # accept

# Singleton Instance.
aCreateDlg = CreateDialog(PipeCad)

def CreateSpec():
    aCreateDlg.show()
# Create

class ModifyDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(800, 600)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Specification"))
        
        self.verticalLayout = QVBoxLayout(self)
        
        self.horizontalLayout = QHBoxLayout()

        self.buttonSpec = QPushButton("SPEC")
        self.buttonSpec.clicked.connect(self.setSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.comboBoxSpec = QComboBox()
        self.comboBoxSpec.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.horizontalLayout.addWidget(self.comboBoxSpec)

        self.labelHeadings = QLabel("Headings")
        self.horizontalLayout.addWidget(self.labelHeadings)

        self.comboBoxHeadings = QComboBox()
        self.comboBoxHeadings.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.comboBoxHeadings.currentIndexChanged.connect(self.headingsChanged)

        self.horizontalLayout.addWidget(self.comboBoxHeadings)

        self.labelSkey = QLabel("Skey")
        self.comboBoxSkey = QComboBox()
        self.comboBoxSkey.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.comboBoxSkey.activated.connect(self.skeyChanged)

        self.horizontalLayout.addWidget(self.labelSkey)
        self.horizontalLayout.addWidget(self.comboBoxSkey)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidgetSpec = QTableWidget()

        self.tableWidgetSpec.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetSpec.setAlternatingRowColors(True)
        self.tableWidgetSpec.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidgetSpec.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetSpec.setGridStyle(Qt.SolidLine)
        self.tableWidgetSpec.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetSpec.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidgetSpec.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetSpec.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetSpec.setContextMenuPolicy(Qt.ActionsContextMenu)

        aActionDelSpco = QAction("Delete", self.tableWidgetSpec)
        aActionDelSpco.triggered.connect(self.delSpco)

        self.tableWidgetSpec.addAction(aActionDelSpco)
        
        self.verticalLayout.addWidget(self.tableWidgetSpec)

        self.tableWidgetCate = QTableWidget()
        self.tableWidgetCate.setColumnCount(7)
        self.tableWidgetCate.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetCate.setAlternatingRowColors(True)
        self.tableWidgetCate.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidgetCate.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetCate.setGridStyle(Qt.SolidLine)
        self.tableWidgetCate.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetCate.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidgetCate.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetCate.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetCate.setContextMenuPolicy(Qt.ActionsContextMenu)

        aActionSetSdte = QAction("Set Detail", self.tableWidgetCate)
        aActionAddSpec = QAction("Add Spec", self.tableWidgetCate)

        aActionSetSdte.triggered.connect(self.setSdte)
        aActionAddSpec.triggered.connect(self.addSpec)

        self.tableWidgetCate.addAction(aActionSetSdte)
        self.tableWidgetCate.addAction(aActionAddSpec)

        aHeaderItem = QTableWidgetItem("CATREF")
        self.tableWidgetCate.setHorizontalHeaderItem(0, aHeaderItem)

        aHeaderItem = QTableWidgetItem("BORE")
        self.tableWidgetCate.setHorizontalHeaderItem(1, aHeaderItem)

        aHeaderItem = QTableWidgetItem("DETREF")
        self.tableWidgetCate.setHorizontalHeaderItem(2, aHeaderItem)

        aHeaderItem = QTableWidgetItem("SKEY")
        self.tableWidgetCate.setHorizontalHeaderItem(3, aHeaderItem)

        aHeaderItem = QTableWidgetItem("DETAIL")
        self.tableWidgetCate.setHorizontalHeaderItem(4, aHeaderItem)

        aHeaderItem = QTableWidgetItem("MATREF")
        self.tableWidgetCate.setHorizontalHeaderItem(5, aHeaderItem)

        aHeaderItem = QTableWidgetItem("BLTREF")
        self.tableWidgetCate.setHorizontalHeaderItem(6, aHeaderItem)

        self.tableWidgetCate.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidgetCate)

        self.horizontalLayout = QHBoxLayout()

        self.buttonCate = QPushButton("CATE")
        self.buttonCate.clicked.connect(self.setCate)
        self.horizontalLayout.addWidget(self.buttonCate)

        self.buttonSdte = QPushButton("SDTE")
        self.buttonSdte.clicked.connect(self.setSdte)
        self.horizontalLayout.addWidget(self.buttonSdte)

        self.buttonSmte = QPushButton("SMTE")
        self.buttonSmte.clicked.connect(self.setSmte)
        self.horizontalLayout.addWidget(self.buttonSmte)

        self.buttonSbol = QPushButton("SBOL")
        self.buttonSbol.clicked.connect(self.setSbol)
        self.horizontalLayout.addWidget(self.buttonSbol)

        self.buttonAdd = QPushButton("Add")
        self.buttonAdd.setToolTip(QT_TRANSLATE_NOOP("Paragon", "Add selected component to SPEC"))
        self.buttonAdd.clicked.connect(self.addSpec)

        self.horizontalLayout.addWidget(self.buttonAdd)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
    # setupUi

    def retranslateUi(self):
        self.buttonSpec.setText(u"SPEC")
    # retranslateUi

    def setSpec(self):
        aSpecItem = PipeCad.CurrentItem()

        if aSpecItem.Type != "SPEC":
            QMessageBox.critical(self, "", "Please select SPEC!")
            return
        # if

        aName = aSpecItem.Name
        if self.comboBoxSpec.findText(aName) < 0:
            self.comboBoxSpec.addItem(aName)
            self.comboBoxSpec.setCurrentText(aName)
        # if

        # Set headings.
        aDatabase = QSqlDatabase.addDatabase("QSQLITE", "PipeStd_SPEC")
        aDatabase.setDatabaseName("catalogues/PipeStd.db")
        aDatabase.open()

        self.comboBoxHeadings.clear()
        for aSeleItem in aSpecItem.Member:
            self.queryModel = QSqlQueryModel()
            self.queryModel.setQuery("SELECT type, head FROM HEAD WHERE purpose='" + aSpecItem.Purpose + "' AND type='" + aSeleItem.Answer + "'", aDatabase)

            if self.queryModel.rowCount() > 0:
                aRecord = self.queryModel.record(0)
                aType = aRecord.value("type")
                aHead = aRecord.value("head")

                self.comboBoxHeadings.addItem(aType, aHead)
            # if
        # for
    # setSpec

    def headingsChanged(self, theIndex):
        if theIndex == -1:
            return
        # if

        aType = self.comboBoxHeadings.itemText(theIndex)
        aName = self.comboBoxSpec.currentText

        aSpecItem = PipeCad.GetItem(aName)
        if aSpecItem == None:
            return
        # if

        aMemberList = list(x for x in aSpecItem.Member if x.Answer == aType)
        #aMemberList = list(filter(lambda x: True if x.Answer == aType else False, aMemberList))

        aSpcoList = []
        for aMember in aMemberList:
            aList = PipeCad.CollectItem("SPCO", aMember)
            aSpcoList.extend(aList)
        # for

        aHeadings = self.comboBoxHeadings.itemData(theIndex).split()
        aCount = len(aHeadings)

        self.tableWidgetSpec.setHorizontalHeaderLabels(aHeadings)
        self.tableWidgetSpec.setColumnCount(aCount)
        self.tableWidgetSpec.setRowCount(len(aSpcoList))

        for i in range(aCount):
            aHeaderText = aHeadings[i]
            self.tableWidgetSpec.setHorizontalHeaderItem(i, QTableWidgetItem(aHeaderText))
        # for

        aSkeySet = set()

        for r in range(self.tableWidgetSpec.rowCount):
            aSpcoItem = aSpcoList[r]

            aSdteItem = aSpcoItem.Detref

            if aSdteItem is not None:
                aSkeySet.add(aSdteItem.Skey)
            # if
        # for

        self.comboBoxSkey.clear()
        self.comboBoxSkey.addItem("NONE")
        self.comboBoxSkey.setCurrentIndex(0)

        for aSkey in aSkeySet:
            self.comboBoxSkey.addItem(aSkey)
        # for

        self.skeyChanged()
    # headingsChanged

    def skeyChanged(self):

        aSkey = self.comboBoxSkey.currentText

        aType = self.comboBoxHeadings.currentText
        aName = self.comboBoxSpec.currentText

        aSpecItem = PipeCad.GetItem(aName)
        if aSpecItem == None:
            return
        # if

        aMemberList = list(x for x in aSpecItem.Member if x.Answer == aType)
        #aMemberList = list(filter(lambda x: True if x.Answer == aType else False, aMemberList))

        aSpcoList = []
        for aMember in aMemberList:
            aList = PipeCad.CollectItem("SPCO", aMember)
            aSpcoList.extend(aList)
        # for

        self.tableWidgetSpec.setRowCount(0)

        for i in range(len(aSpcoList)):
            aSpcoItem = aSpcoList[i]

            aCateItem = aSpcoItem.Catref
            aSdteItem = aSpcoItem.Detref
            aSmteItem = aSpcoItem.Matref
            aSbolItem = aSpcoItem.Bltref

            aSpcoName = aSpcoItem.Name

            if aSkey == "NONE" or (aSdteItem is not None and aSdteItem.Skey == aSkey):
                pass
            else:
                continue
            # if

            aRow = self.tableWidgetSpec.rowCount
            self.tableWidgetSpec.insertRow(aRow)

            for c in range(self.tableWidgetSpec.columnCount):
                aHeaderText = self.tableWidgetSpec.horizontalHeaderItem(c).text()
                if aHeaderText == "NAME":
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSpcoName))
                elif aHeaderText == "TYPE":
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aType))
                elif aHeaderText == "BTYP":
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSpcoItem.Purpose))
                elif aHeaderText == "PBOR0" and aCateItem is not None:
                    aParam = aCateItem.Param.split()
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aParam[0]))
                elif aHeaderText == "BDIA" and aCateItem is not None:
                    aParam = aCateItem.Param.split()
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aParam[0]))
                elif aHeaderText == "PBOR1" and aCateItem is not None:
                    aParam = aCateItem.Param.split()
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aParam[0]))
                elif aHeaderText == "PBOR2" and aCateItem is not None:
                    aParam = aCateItem.Param.split()
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aParam[1]))
                elif aHeaderText == "PBOR3" and aCateItem is not None:
                    aParam = aCateItem.Param.split()
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aParam[1]))
                elif aHeaderText == "SKEY" and aSdteItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSdteItem.Skey))
                elif aHeaderText == "BSEL" and aSdteItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSdteItem.Skey))
                elif aHeaderText == "CATREF" and aCateItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aCateItem.Name))
                elif aHeaderText == "DETREF" and aSdteItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSdteItem.Name))
                elif aHeaderText == "DETAIL" and aSdteItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSdteItem.Rtext))
                elif aHeaderText == "MATREF" and aSmteItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSmteItem.Name))
                elif aHeaderText == "BLTREF" and aSbolItem is not None:
                    self.tableWidgetSpec.setItem(aRow, c, QTableWidgetItem(aSbolItem.Name))
                # if
            # for
        # for
    # skeyChanged

    def setSdte(self):
        """Set Spec component name, skey, and detail text.
        """
        aSdteItem = PipeCad.CurrentItem()

        if aSdteItem.Type != "SDTE":
            QMessageBox.warning(self, "", "Please select a SDTE!")
            return
        # if

        aRows = []
        aSelectedItems = self.tableWidgetCate.selectedItems()
        for aItem in aSelectedItems:
            aRows.append(aItem.row())
        # for

        aRows = list(set(aRows))

        if len(aRows) < 1:
            return
        # if

        for r in aRows:
            aTableItem = QTableWidgetItem(aSdteItem.Name)
            aTableItem.setData(Qt.UserRole, aSdteItem)

            self.tableWidgetCate.setItem(r, 2, aTableItem)
            self.tableWidgetCate.setItem(r, 3, QTableWidgetItem(aSdteItem.Skey))
            self.tableWidgetCate.setItem(r, 4, QTableWidgetItem(aSdteItem.Rtext))
        # for
    # setSdte

    def setSmte(self):
        aSmteItem = PipeCad.CurrentItem()
        if aSmteItem.Type != "SMTE":
            QMessageBox.warning(self, "", "Please select a SMTE!")
            return
        # if

        aRows = []
        aSelectedItems = self.tableWidgetCate.selectedItems()
        for aItem in aSelectedItems:
            aRows.append(aItem.row())
        # for

        aRows = list(set(aRows))

        if len(aRows) < 1:
            return
        # if

        for r in aRows:
            aTableItem = QTableWidgetItem(aSmteItem.Name)
            aTableItem.setData(Qt.UserRole, aSmteItem)

            self.tableWidgetCate.setItem(r, 5, aTableItem)
        # for
    # setSmte

    def setSbol(self):
        aSbolItem = PipeCad.CurrentItem()
        if aSbolItem.Type != "SBOL":
            QMessageBox.warning(self, "", "Please select a SBOL!")
            return
        # if

        aRows = []
        aSelectedItems = self.tableWidgetCate.selectedItems()
        for aItem in aSelectedItems:
            aRows.append(aItem.row())
        # for

        aRows = list(set(aRows))

        if len(aRows) < 1:
            return
        # if

        for r in aRows:
            aTableItem = QTableWidgetItem(aSbolItem.Name)
            aTableItem.setData(Qt.UserRole, aSbolItem)

            self.tableWidgetCate.setItem(r, 6, aTableItem)
        # for
    # setSbol

    def delSpco(self):
        pass
        #aIndex = self.tableView.currentIndex()
        #if aIndex.isValid():
        #    if QMessageBox.question(self, "", "Are you sure to delete the selected record?") == QMessageBox.Yes:
        #        self.tableView.model().removeRow(aIndex.row())
    # delSpco

    def setCate(self):
        aScomList = []
        aSdteList = []

        aCateItem = PipeCad.CurrentItem()
        if aCateItem.Type == "CATE":
            aScomList = PipeCad.CollectItem("SCOM", aCateItem)
            aSdteList = PipeCad.CollectItem("SDTE", aCateItem)
        elif aCateItem.Type == "STCA":
            aScomList = PipeCad.CollectItem("SPRF", aCateItem)
        else:
            QMessageBox.warning(self, "", "Please select CATE or STCA!")
            return
        # if

        aScomSize = len(aScomList)

        self.tableWidgetCate.setRowCount(aScomSize)

        for r in range (aScomSize):
            aScomItem = aScomList[r]

            aParams = aScomItem.Param.split()

            aNameItem = QTableWidgetItem(aScomItem.Name)
            aNameItem.setData(Qt.UserRole, aScomItem)

            self.tableWidgetCate.setItem(r, 0, aNameItem)
            self.tableWidgetCate.setItem(r, 1, QTableWidgetItem(aParams[0]))
            self.tableWidgetCate.setItem(r, 2, QTableWidgetItem(""))
            self.tableWidgetCate.setItem(r, 3, QTableWidgetItem(""))
            self.tableWidgetCate.setItem(r, 4, QTableWidgetItem(""))
        # for
    # setCate

    def addSpec(self):
        """Add selected componet to spec.

        Args:

        Returns:

        Raises:
        """

        aSpecName = self.comboBoxSpec.currentText
        if len(aSpecName) == 0:
            return

        aSpecItem = PipeCad.GetItem(aSpecName)
        if aSpecItem == None:
            return

        aRows = []
        aSelectedItems = self.tableWidgetCate.selectedItems()
        for aItem in aSelectedItems:
            aRows.append(aItem.row())

        aRows = list(set(aRows))

        if len(aRows) < 1:
            return

        aType = self.comboBoxHeadings.currentText
        aSkey = self.tableWidgetCate.item(aRows[0], 3).text()

        aSeleItem = None
        aMemberList = aSpecItem.Member
        for aMember in aMemberList:
            if aMember.Answer == aType:
                aSeleItem = aMember
                break

        PipeCad.StartTransaction("Add Spco")

        if aSeleItem == None:
            PipeCad.CreateItem("SELE", aSpecName + "/" + aType)
            aSeleItem = PipeCad.CurrentItem()

        hasSeleItem = False
        aMemberList = aSeleItem.Member
        for aMember in aMemberList:
            if aMember.Answer == aSkey:
                aSeleItem = aMember
                hasSeleItem = True
                break
            # if
        # for

        if not hasSeleItem and aSpecItem.Purpose in {"PIPE", "BOLT"}:
            PipeCad.SetCurrentItem(aSeleItem)
            try:
                PipeCad.CreateItem("SELE", aSpecName + "/" + aType + "/" + aSkey)
            except Exception as e:
                PipeCad.SetCurrentItem("/" + aSpecName + "/" + aType + "/" + aSkey)
            # try

            aSeleItem = PipeCad.CurrentItem()
            aSeleItem.Purpose = aSkey
        elif aSpecItem.Purpose == "STL":
            aSkey = aType
        # if

        aSpcoItem = aSeleItem

        for r in aRows:
            aScomName = self.tableWidgetCate.item(r, 0).text()
            aBore = self.tableWidgetCate.item(r, 1).text()
            aDetail = self.tableWidgetCate.item(r, 4).text()

            aCatref = self.tableWidgetCate.item(r, 0).data(Qt.UserRole)
            aDetref = self.tableWidgetCate.item(r, 2).data(Qt.UserRole)
            aMatref = self.tableWidgetCate.item(r, 5).data(Qt.UserRole)
            aBltref = self.tableWidgetCate.item(r, 6).data(Qt.UserRole)

            PipeCad.SetCurrentItem(aSpcoItem)

            try:
                PipeCad.CreateItem("SPCO", aSpecName + "/" + aSkey + "/" + aScomName)
            except Exception as e:
                continue
            # try

            aSpcoItem = PipeCad.CurrentItem()
            aSpcoItem.Answer = aBore
            aSpcoItem.Purpose = aType

            if aCatref is not None:
                aSpcoItem.Catref = aCatref
            # if

            if aDetref is not None:
                aSpcoItem.Detref = aDetref
            # if

            if aMatref is not None:
                aSpcoItem.Matref = aMatref
            # if

            if aBltref is not None:
                aSpcoItem.Bltref = aBltref
            # if

        PipeCad.CommitTransaction()

        aIndex = self.comboBoxHeadings.currentIndex
        self.headingsChanged(aIndex)

        aRows.sort(reverse=True)
        for r in aRows:
            self.tableWidgetCate.removeRow(r)
        # for

    # addSpec

# Singleton Instance.
aSpecDlg = ModifyDialog(PipeCad)

def ModifySpec():
    aSpecDlg.setSpec()
    aSpecDlg.show()
# Modify    
