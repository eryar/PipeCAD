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
# Date: 21:16 2021-09-16

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from PipeCAD import *

class SpecDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(640, 480)
        self.setWindowTitle(self.tr("Nozzle Specification"))

        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.horizontalLayout = QHBoxLayout()

        self.buttonSpecCE = QPushButton(self.tr("SPEC CE"))
        self.labelSpecCE = QLabel()

        self.buttonSpecCE.clicked.connect(self.setSpec)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonSpecCE)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.labelSpecCE)
        
        self.buttonCateCE = QPushButton(self.tr("CATE CE"))
        self.labelCateCE = QLabel()

        self.buttonCateCE.clicked.connect(self.setCate)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.buttonCateCE)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.labelCateCE)

        self.labelDescription = QLabel(self.tr("Description"))
        self.textDescription = QLineEdit()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textDescription)

        self.labelGenericType = QLabel(self.tr("Generic Type"))
        self.comboGenericType = QComboBox()
        self.comboGenericType.setEditable(True)
        self.comboGenericType.currentIndexChanged.connect(self.genericTypeChanged)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelGenericType)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboGenericType)

        self.verticalLayout.addLayout(self.formLayout)

        # Spco Table.
        self.spcoTable = QTableWidget()
        self.spcoTable.setColumnCount(2)
        self.spcoTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.spcoTable.setAlternatingRowColors(True)
        self.spcoTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.spcoTable.horizontalHeader().setStretchLastSection(True)
        self.spcoTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.spcoTable.verticalHeader().setMinimumSectionSize(16)
        self.spcoTable.verticalHeader().setDefaultSectionSize(18)

        aHeaderItem = QTableWidgetItem("Bore")
        self.spcoTable.setHorizontalHeaderItem(0, aHeaderItem)

        aHeaderItem = QTableWidgetItem("Name")
        self.spcoTable.setHorizontalHeaderItem(1, aHeaderItem)

        self.verticalLayout.addWidget(self.spcoTable)

        # Category Table.
        self.cateTable = QTableWidget()
        self.cateTable.setColumnCount(2)
        self.cateTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cateTable.setAlternatingRowColors(True)
        self.cateTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cateTable.horizontalHeader().setStretchLastSection(True)
        self.cateTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.cateTable.verticalHeader().setMinimumSectionSize(16)
        self.cateTable.verticalHeader().setDefaultSectionSize(18)

        aHeaderItem = QTableWidgetItem("Bore")
        self.cateTable.setHorizontalHeaderItem(0, aHeaderItem)

        aHeaderItem = QTableWidgetItem("Name")
        self.cateTable.setHorizontalHeaderItem(1, aHeaderItem)

        self.verticalLayout.addWidget(self.cateTable)

        # Actions.
        self.horizontalLayout = QHBoxLayout()
        self.buttonAdd = QPushButton(self.tr("Add"))
        self.buttonRem = QPushButton(self.tr("Remove"))

        self.buttonAdd.clicked.connect(self.addNozzle)
        self.buttonRem.clicked.connect(self.remNozzle)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonRem)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def setSpec(self):
        aSpecItem = PipeCad.CurrentItem()
        if aSpecItem.Type != "SPEC":
            QMessageBox.critical(self, "", self.tr("Can only be used from a SPEC!"))
            return

        self.comboGenericType.clear()
        self.labelSpecCE.setText(aSpecItem.Name)
        self.textDescription.setText(aSpecItem.Description)
        self.specItem = aSpecItem
        self.seleList = PipeCad.CollectItem("SELE", aSpecItem)

        for i in range (len(self.seleList)):
            aSeleItem = self.seleList[i]
            self.comboGenericType.addItem(aSeleItem.Description)
    # setSpec

    def genericTypeChanged(self, theIndex):
        aSeleItem = self.seleList[theIndex]
        aSpcoList = PipeCad.CollectItem("SPCO", aSeleItem)
        aSpcoSize = len(aSpcoList)
        self.spcoTable.setRowCount(aSpcoSize)
        for r in range (aSpcoSize):
            aSpcoItem = aSpcoList[r]
            aScomItem = aSpcoItem.Catref
            if aScomItem is not None:
                aParam = aScomItem.Param.split()
                self.spcoTable.setItem(r, 0, QTableWidgetItem(aParam[0]))
                self.spcoTable.setItem(r, 1, QTableWidgetItem(aScomItem.Name))

    def setCate(self):
        aCateItem = PipeCad.CurrentItem()
        if aCateItem.Type != "CATE":
            QMessageBox.critical(self, "", self.tr("Please select CATE!"))
            return

        self.labelCateCE.setText(aCateItem.Name)
        self.cateItem = aCateItem

        aScomList = PipeCad.CollectItem("SCOM", aCateItem)
        aScomSize = len(aScomList)
        self.cateTable.setRowCount(aScomSize)

        for r in range (aScomSize):
            aScomItem = aScomList[r]
            aParam = aScomItem.Param.split()
            aNameItem = QTableWidgetItem(aScomItem.Name)
            aNameItem.setData(Qt.UserRole, aScomItem)
            self.cateTable.setItem(r, 0, QTableWidgetItem(aParam[0]))
            self.cateTable.setItem(r, 1, aNameItem)
    # setCate

    def addNozzle(self):
        aRows = []
        aSelectedItems = self.cateTable.selectedItems()
        for aItem in aSelectedItems:
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        aSelectedRows = len(aRows)

        if aSelectedRows < 1:
            return

        PipeCad.StartTransaction("Build Nozzle Spec")
        PipeCad.SetCurrentItem(self.specItem)

        self.specItem.Description = self.textDescription.text

        PipeCad.CreateItem("SELE")
        aSeleItem = PipeCad.CurrentItem()
        aSeleItem.Description = self.comboGenericType.currentText

        aPrefix = aSeleItem.Description.replace(" ", "_")

        aRow = self.spcoTable.rowCount
        self.spcoTable.setRowCount(aRow + aSelectedRows)
        for r in range (aSelectedRows):

            aBoreItem = self.cateTable.item(aRows[r], 0)
            aNameItem = self.cateTable.item(aRows[r], 1)

            aBore = aBoreItem.text()
            aName = aNameItem.text()
            aCatref = aNameItem.data(Qt.UserRole)

            self.spcoTable.setItem(aRow + r, 0, QTableWidgetItem(aBore))
            self.spcoTable.setItem(aRow + r, 1, QTableWidgetItem(aName))

            PipeCad.CreateItem("SPCO", aPrefix + "/" + aName)
            aSpcoItem = PipeCad.CurrentItem()
            aSpcoItem.Catref = aCatref

        PipeCad.CommitTransaction()

        aRows.sort(reverse=True)
        for r in aRows:
            self.cateTable.removeRow(r)

    # addNozzle

    def remNozzle(self):
        pass
    # remNozzle

# Singleton Instance.
aSpecDlg = SpecDialog(PipeCad)

def Show():
    aSpecDlg.show()
# Show

class CreateDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()

    def setupUi(self):
        self.resize(600, 360)
        self.setWindowTitle(self.tr("Create Nozzle"))

        self.horizontalLayout = QHBoxLayout(self)

        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        self.labelName = QLabel(self.tr("Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelSpecification = QLabel(self.tr("Specification"))
        self.comboSpecification = QComboBox()

        aSpecList = PipeCad.CollectItem("SPEC")

        for aSpecItem in (aSpecList):
            if aSpecItem.Purpose == "NOZZ":
                self.comboSpecification.addItem(aSpecItem.Description, aSpecItem)
            # if
        # for

        self.comboSpecification.currentIndexChanged.connect(self.specificationChanged)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelSpecification)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboSpecification)

        self.labelGenericType = QLabel(self.tr("Generic Type"))
        self.comboGenericType = QComboBox()
        self.comboGenericType.currentIndexChanged.connect(self.genericTypeChanged)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelGenericType)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboGenericType)

        self.labelBore = QLabel(self.tr("Bore"))
        self.comboBore = QComboBox()

        self.comboSpecification.currentIndexChanged(0)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelBore)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBore)

        self.labelHeight = QLabel(self.tr("Height"))
        self.textHeight = QLineEdit("100.0")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textHeight)

        self.labelTemperature = QLabel(self.tr("Temperature"))
        self.textTemperature = QLineEdit("0.0")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelTemperature)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textTemperature)

        self.labelPressure = QLabel(self.tr("Pressure"))
        self.textPressure = QLineEdit("0.0")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelPressure)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.textPressure)

        self.labelDescription = QLabel(self.tr("Description"))
        self.textDescription = QLineEdit()

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.textDescription)

        self.labelPurpose = QLabel(self.tr("Purpose"))
        self.textPurpose = QLineEdit()

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.textPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupPosition = QGroupBox(self.tr("Position"))
        self.formLayout = QFormLayout(self.groupPosition)

        self.labelX = QLabel("X")
        self.textX = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelX)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textX)

        self.labelY = QLabel("Y")
        self.textY = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelY)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textY)

        self.labelZ = QLabel("Z")
        self.textZ = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelZ)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textZ)

        self.labelP1 = QLabel("P1")
        self.textP1 = QLineEdit("N")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelP1)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textP1)

        self.verticalLayout.addWidget(self.groupPosition)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumSize(QSize(280, 360))
        self.labelDiagram.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/nozzle-diagram.png"))
        self.horizontalLayout.addWidget(self.labelDiagram)
    # setupUi


    def specificationChanged(self):
        self.comboGenericType.clear()

        aSpecItem = self.comboSpecification.currentData

        aSeleList = PipeCad.CollectItem("SELE", aSpecItem)

        for aSeleItem in aSeleList:
            self.comboGenericType.addItem(aSeleItem.Description, aSeleItem)
        # for
    # specificationChanged

    def genericTypeChanged(self):
        self.comboBore.clear()

        aSeleItem = self.comboGenericType.currentData
        aSpcoList = PipeCad.CollectItem("SPCO", aSeleItem)

        aBoreDict = dict()

        for aSpcoItem in aSpcoList:
            aScomItem = aSpcoItem.Catref
            if aScomItem is not None:
                aParam = aScomItem.Param.split()
                aBoreDict[int(aParam[0])] = aScomItem
            # if
        # for

        for aBore in sorted(aBoreDict):
            self.comboBore.addItem(aBore, aBoreDict[aBore])
        # for
    # genericTypeChanged

    def accept(self):
        try:
            PipeCad.StartTransaction("Create Nozzle")

            PipeCad.CreateItem("NOZZ", self.textName.text)
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Catref = self.comboBore.currentData
        
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept

# Singleton.
aNozzleDlg = CreateDialog(PipeCad)

def Create():
    aNozzleDlg.show()
# Create

def Modify():
    QMessageBox.information(PipeCad, "", "Modify Nozzle")
# Modify
