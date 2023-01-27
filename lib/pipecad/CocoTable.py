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
# Date: 21:02 2021-09-19

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *


class CreateDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Create Coco Table"))

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
            PipeCad.StartTransaction("Create Coco Table")

            PipeCad.CreateItem("CCTA", aName)
            aCctaItem = PipeCad.CurrentItem()
            aCctaItem.Purpose = aPurpose

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# CreateDialog

# Singleton Instance.
aCreateDlg = CreateDialog(PipeCad)

def Create():
    aCreateDlg.show()
# Create


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent = None):
        QItemDelegate.__init__(self, parent)
    # __init__

    def setupCoco(self, theCctaItem):
        self.cocoTypes = []
        if theCctaItem is None:
            return
        # if

        aCcdeList = PipeCad.CollectItem("CCDE", theCctaItem)
        for aCcdeItem in aCcdeList:
            self.cocoTypes.append(aCcdeItem.Connection)
        # for
    # setupCoco

    def createEditor(self, theParent, theOption, theIndex):
        anEditor = QComboBox(theParent)
        #anEditor.setEditable(True)
        anEditor.addItems(self.cocoTypes)
        return anEditor
    # createEditor

    def setEditorData(self, theEditor, theIndex):
        aText = theIndex.data()
        if aText is not None:
            theEditor.setCurrentText(aText)
        # if
    # setEditorData

    def setModelData(self, theEditor, theModel, theIndex):
        theModel.setData(theIndex, theEditor.currentText)
    # setModelData

# ComboBoxDelegate

class CocdesDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(380, 500)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "COCO Description"))

        self.verticalLayout = QVBoxLayout(self)

        self.tableWidget = QTableWidget(18, 2)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Description"])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()

        self.buttonAdd = QPushButton("Add")
        self.buttonAdd.clicked.connect(self.addRow)

        self.buttonDelete = QPushButton("Delete")
        self.buttonDelete.clicked.connect(self.deleteRow)

        # Spacer Item.
        aSpacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Dialog Buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonDelete)
        self.horizontalLayout.addItem(aSpacerItem)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def fillForm(self, theCctaItem):
        if theCctaItem is None:
            return
        # if

        aCcdeList = PipeCad.CollectItem("CCDE", theCctaItem)
        self.tableWidget.setRowCount(len(aCcdeList) + 1)
        for i in range (len(aCcdeList)):
            aCcdeItem = aCcdeList[i]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(aCcdeItem.Connection))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(aCcdeItem.Description))
        # for
    # fillForm

    def addRow(self):
        aRow = self.tableWidget.rowCount
        self.tableWidget.insertRow(aRow)
    # addRow

    def deleteRow(self):
        aAnswer = QMessageBox.question(self, "", "Are you sure to delete the selected row?")
        if aAnswer != QMessageBox.Yes:
            return
        # if

        aRows = []
        for aItem in self.tableWidget.selectedItems():
            aRows.append(aItem.row())
        # for

        # Remove duplicate row.
        aRows = list(set(aRows))
        if len(aRows) < 1:
            return
        # if

        aRows.sort(reverse=True)
        for r in aRows:
            self.tableWidget.removeRow(r)
        # for
    # deleteRow

# CocdesDialog

class ModifyDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.cocoTable = None
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(580, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Modify COCO Table"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.buttonCE = QPushButton("CE")
        self.labelName = QLabel("")

        self.buttonCE.clicked.connect(self.setCocoTable)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonCE)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.labelName)
        self.verticalLayout.addLayout(self.formLayout)

        # Actions.
        self.horizontalLayout = QHBoxLayout()
        self.buttonCcde = QPushButton("COCO Description")
        self.buttonAddRow = QPushButton("Add Row")
        self.buttonDelRow = QPushButton("Delete Row")
        self.buttonAddColumn = QPushButton("Add Column")
        self.buttonDelColumn = QPushButton("Delete Column")

        self.buttonCcde.clicked.connect(self.setupTypes)
        self.buttonAddRow.clicked.connect(self.addRow)
        self.buttonDelRow.clicked.connect(self.deleteRow)
        self.buttonAddColumn.clicked.connect(self.addColumn)
        self.buttonDelColumn.clicked.connect(self.deleteColumn)

        self.horizontalLayout.addWidget(self.buttonCcde)
        self.horizontalLayout.addWidget(self.buttonAddRow)
        self.horizontalLayout.addWidget(self.buttonDelRow)
        self.horizontalLayout.addWidget(self.buttonAddColumn)
        self.horizontalLayout.addWidget(self.buttonDelColumn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # COCO Table.
        self.tableWidget = QTableWidget(3, 4)
        self.tableWidget.setHorizontalHeaderLabels(["CType"])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        #self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # Delegate.
        self.comboBoxDelegate = ComboBoxDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(self.comboBoxDelegate)

        self.verticalLayout.addWidget(self.tableWidget)

        # Dialog Buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def setCocoTable(self):
        aItem = PipeCad.CurrentItem()
        if aItem.Type == "CCTA":
            self.cocoTable = aItem
            self.labelName.setText(aItem.Name)
            self.comboBoxDelegate.setupCoco(aItem)
        else:
            QMessageBox.warning(self, "", "Please select CCTA!")
        # if
    # setCocoTable

    def setupTypes(self):
        aDlg = CocdesDialog(self)
        aDlg.fillForm(self.cocoTable)
        if aDlg.exec() == QDialog.Rejected:
            return
        # if

        if self.cocoTable is None:
            QMessageBox.warning(self, "", "Please set CCTA first!")
            return
        # if

        aMemberList = self.cocoTable.Member
        if len(aMemberList) > 0:
            PipeCad.SetCurrentItem(aMemberList[-1])
        else:
            PipeCad.SetCurrentItem(self.cocoTable)
        # if

        PipeCad.StartTransaction("Set COCO Description")
        aRowCount = aDlg.tableWidget.rowCount
        for r in range (aRowCount):
            aNameItem = aDlg.tableWidget.item(r, 0)
            aDescItem = aDlg.tableWidget.item(r, 1)
            if aNameItem is not None and len(aNameItem.text()) > 0:
                try:
                    PipeCad.CreateItem("CCDE", aNameItem.text() + "-DESC")
                except Exception as e:
                    PipeCad.SetCurrentItem("/" + aNameItem.text() + "-DESC")
                # try

                aCcdeItem = PipeCad.CurrentItem()
                aCcdeItem.Connection = aNameItem.text()
                aCcdeItem.Description = aDescItem.text()
            # if
        # for
        PipeCad.CommitTransaction()

        self.comboBoxDelegate.setupCoco(self.cocoTable)
    # setupTypes

    def addRow(self):
        aRow = self.tableWidget.rowCount
        self.tableWidget.insertRow(aRow)
    # addRow

    def deleteRow(self):
        aRow = self.tableWidget.currentRow()
        self.tableWidget.removeRow(aRow)
    # deleteRow

    def addColumn(self):
        aColumn = self.tableWidget.columnCount
        self.tableWidget.insertColumn(aColumn)
    # addColumn

    def deleteColumn(self):
        aColumn = self.tableWidget.currentColumn()
        self.tableWidget.removeColumn(aColumn)
    # deleteColumn

    def accept(self):
        if self.cocoTable is None:
            return
        # if

        aRowCount = self.tableWidget.rowCount
        aColumnCount = self.tableWidget.columnCount
        if aRowCount < 1:
            return
        # if

        aMemberList = self.cocoTable.Member
        if len(aMemberList) > 0:
            PipeCad.SetCurrentItem(aMemberList[-1])
        else:
            PipeCad.SetCurrentItem(self.cocoTable)
        # if

        PipeCad.StartTransaction("Modify COCO Table")
        for r in range(aRowCount):
            aTypeItem = self.tableWidget.item(r, 0)
            if aTypeItem is not None and len(aTypeItem.text()) > 0:
                for c in range(1, aColumnCount):
                    aConnItem = self.tableWidget.item(r, c)
                    if aConnItem is not None and len(aConnItem.text()) > 0:
                        try:
                            PipeCad.CreateItem("COCO", aTypeItem.text() + "-" + aConnItem.text())
                            aCocoItem = PipeCad.CurrentItem()
                            aCocoItem.Ctype1 = aTypeItem.text()
                            aCocoItem.Ctype2 = aConnItem.text()
                        except Exception as e:
                            pass
                        # try
                    # if

                # for
            # if
        # for

        PipeCad.CommitTransaction()

        QDialog.accept(self)
    # accept
# ModifyDialog

# Singleton Instance.
aModifyDlg = ModifyDialog(PipeCad)

def Modify():
    aModifyDlg.setCocoTable()
    aModifyDlg.show()
# Create
