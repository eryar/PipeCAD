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
# Date: 12:02 2022-05-06

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *


class TableWorldDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Create Table World"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Paragon", "Name"))
        self.lineEditName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEditName)

        # Purpose
        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Paragon", "Purpose"))
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

        aName = self.lineEditName.text
        aPurpose = self.comboPurpose.currentText

        if len(aName) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Paragon", "Please input name!"))
            return
        # if

        PipeCad.StartTransaction("Create Table World")

        PipeCad.CreateItem("TAWL", aName)
        aCctaItem = PipeCad.CurrentItem()
        aCctaItem.Purpose = aPurpose

        PipeCad.CommitTransaction()

        QDialog.accept(self)
    # accept

# Singleton Instance.
aTableWorldDlg = TableWorldDialog(PipeCad)

def CreateTableWorld():
    aTableWorldDlg.show()
# Create


class PipeTableDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.pdtaItem = None
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(500, 380)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Create Pipe Table"))

        self.verticalLayout = QVBoxLayout(self)

        # Name
        self.formLayout = QFormLayout()

        self.textName = QLineEdit()
        self.comboOption = QComboBox()
        self.comboOption.addItem("Create")
        self.comboOption.addItem("Modify")
        self.comboOption.activated.connect(self.optionActivated)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboOption)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Description
        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Paragon", "Description"))
        self.textDescription = QLineEdit()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDescription)

        # Purpose
        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Paragon", "Purpose"))
        self.comboPurpose = QComboBox()
        self.comboPurpose.setEditable(True)
        self.comboPurpose.addItem("PIPE")
        self.comboPurpose.addItem("STL")
        self.comboPurpose.addItem("NOZZ")
        self.comboPurpose.addItem("EQUI")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        # Data Table.
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Paragon", "Nominal Bore"), QT_TRANSLATE_NOOP("Paragon", "Wall Thickness"), QT_TRANSLATE_NOOP("Paragon", "Pipe Stock Length")])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)

        self.verticalLayout.addWidget(self.tableWidget)

        # Buttons.
        self.horizontalLayout = QHBoxLayout()

        self.buttonAdd = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Add"))
        self.buttonAdd.clicked.connect(self.addRow)

        self.buttonRemove = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Remove"))
        self.buttonRemove.clicked.connect(self.removeRow)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

    # setupUi

    def initTable(self, thePdtaItem):
        self.pdtaItem = thePdtaItem
        self.tableWidget.setRowCount(0)

        if thePdtaItem is None:
            self.textName.setText("")
            self.textDescription.setText("")
            self.comboPurpose.setCurrentIndex(0)
        else:
            self.textName.setText(thePdtaItem.Name)
            self.textDescription.setText(thePdtaItem.Description)
            self.comboPurpose.setCurrentText(thePdtaItem.Purpose)

            for aPdelItem in thePdtaItem.Member:
                aRow = self.tableWidget.rowCount
                self.tableWidget.insertRow(aRow)

                aTableItem = QTableWidgetItem(aPdelItem.Bore)
                aTableItem.setData(Qt.UserRole, aPdelItem)

                self.tableWidget.setItem(aRow, 0, aTableItem)
                self.tableWidget.setItem(aRow, 1, QTableWidgetItem(str(aPdelItem.WallThickness)))
                self.tableWidget.setItem(aRow, 2, QTableWidgetItem(str(aPdelItem.StockLength)))
            # for
        # if
    # init

    def optionActivated(self, theIndex):

        if theIndex == 0:
            # Create
            self.initTable(None)
        else:
            # Modify
            aTreeItem = PipeCad.CurrentItem()
            if aTreeItem.Type == "PDTA":
                self.initTable(aTreeItem)
            else:
                QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Paragon", "Please select PDTA item!"))
            # if
        # if

    # optionChanged

    def addRow(self):
        aRow = self.tableWidget.rowCount
        self.tableWidget.insertRow(aRow)
        self.tableWidget.setItem(aRow, 0, QTableWidgetItem("0"))
        self.tableWidget.setItem(aRow, 1, QTableWidgetItem("0.0"))
        self.tableWidget.setItem(aRow, 2, QTableWidgetItem("6000"))
    # addRow

    def removeRow(self):
        aRow = self.tableWidget.currentRow()
        if aRow != -1:
            self.tableWidget.removeRow(aRow)
        # if
    # removeRow

    def createTable(self):        
        PipeCad.StartTransaction("Create PDTA")

        PipeCad.CreateItem("PDTA", self.textName.text)
        aPdtaItem = PipeCad.CurrentItem()

        aPdtaItem.Description = self.textDescription.text
        aPdtaItem.Purpose = self.comboPurpose.currentText

        for r in range(self.tableWidget.rowCount):
            aBore = self.tableWidget.item(r, 0).text()
            aThickness = self.tableWidget.item(r, 1).text()
            aLength = self.tableWidget.item(r, 2).text()

            PipeCad.CreateItem("PDEL")
            aPdelItem = PipeCad.CurrentItem()
            aPdelItem.Bore = aBore
            aPdelItem.WallThickness = float(aThickness)
            aPdelItem.StockLength = float(aLength)
        # for

        PipeCad.CommitTransaction()
    # createTable

    def modifyTable(self):

        aPdelSetOld = set()
        aPdelSetNew = set()

        for aPdelItem in self.pdtaItem.Member:
            aPdelSetOld.add(aPdelItem)
        # for

        for r in range(self.tableWidget.rowCount):
            aTableItem = self.tableWidget.item(r, 0)
            if aTableItem is not None:
                aPdelItem = aTableItem.data(Qt.UserRole)
                if aPdelItem is not None:
                    aPdelSetNew.add(aPdelItem)
                # if
            # if
        # for

        PipeCad.StartTransaction("Modify PDTA")
        self.pdtaItem.Name = self.textName.text
        self.pdtaItem.Description = self.textDescription.text
        self.pdtaItem.Purpose = self.comboPurpose.currentText

        aDeleteSet = aPdelSetOld.difference(aPdelSetNew)
        for aPdelItem in aDeleteSet:
            PipeCad.SetCurrentItem(aPdelItem)
            PipeCad.DeleteItem("PDEL")
        # for

        if len(self.pdtaItem.Member) > 0:
            PipeCad.SetCurrentItem(self.pdtaItem.Member[-1])
        else:
            PipeCad.SetCurrentItem(self.pdtaItem)
        # if

        for r in range(self.tableWidget.rowCount):
            aPdelItem = self.tableWidget.item(r, 0).data(Qt.UserRole)
            if aPdelItem is None:
                # Create
                PipeCad.CreateItem("PDEL")
                aPdelItem = PipeCad.CurrentItem()
                aPdelItem.Bore = self.tableWidget.item(r, 0).text()
                aPdelItem.WallThickness = float(self.tableWidget.item(r, 1).text())
                aPdelItem.StockLength = float(self.tableWidget.item(r, 2).text())
            else:
                # Modify
                aPdelItem.Bore = self.tableWidget.item(r, 0).text()
                aPdelItem.WallThickness = float(self.tableWidget.item(r, 1).text())
                aPdelItem.StockLength = float(self.tableWidget.item(r, 2).text())
            # if
        # for

        PipeCad.CommitTransaction()

    # modifyTable

    def accept(self):

        if self.pdtaItem is None:
            self.createTable()
        else:
            self.modifyTable()
        # if

        QDialog.accept(self)
    # accept

# PipeTableDialog

# Singleton Instance.
aPipeTableDlg = PipeTableDialog(PipeCad)

def CreatePipeTable():
    aPipeTableDlg.initTable(None)
    aPipeTableDlg.show()
# CreatePipeTable
