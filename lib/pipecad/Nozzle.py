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

import os
import ezdxf

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class SpecDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(640, 480)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Nozzle Specification"))

        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.horizontalLayout = QHBoxLayout()

        self.buttonSpecCE = QPushButton(QT_TRANSLATE_NOOP("Paragon", "SPEC CE"))
        self.labelSpecCE = QLabel()

        self.buttonSpecCE.clicked.connect(self.setSpec)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonSpecCE)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.labelSpecCE)
        
        self.buttonCateCE = QPushButton(QT_TRANSLATE_NOOP("Paragon", "CATE CE"))
        self.labelCateCE = QLabel()

        self.buttonCateCE.clicked.connect(self.setCate)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.buttonCateCE)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.labelCateCE)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Paragon", "Description"))
        self.textDescription = QLineEdit()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textDescription)

        self.labelGenericType = QLabel(QT_TRANSLATE_NOOP("Paragon", "Generic Type"))
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
        self.buttonAdd = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Add"))
        self.buttonRem = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Remove"))

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
            QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Paragon", "Can only be used from a SPEC!"))
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
            QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Paragon", "Please select CATE!"))
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

class NozzleDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.nozzItem = None
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(600, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Nozzle"))

        self.horizontalLayout = QHBoxLayout(self)

        self.verticalLayout = QVBoxLayout()

        self.formLayout = QFormLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Paragon", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelSpecification = QLabel(QT_TRANSLATE_NOOP("Paragon", "Specification"))
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

        self.labelGenericType = QLabel(QT_TRANSLATE_NOOP("Paragon", "Generic Type"))
        self.comboGenericType = QComboBox()
        self.comboGenericType.currentIndexChanged.connect(self.genericTypeChanged)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelGenericType)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboGenericType)

        self.labelBore = QLabel(QT_TRANSLATE_NOOP("Paragon", "Bore"))
        self.comboBore = QComboBox()

        self.comboSpecification.currentIndexChanged(0)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelBore)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBore)

        self.labelHeight = QLabel(QT_TRANSLATE_NOOP("Paragon", "Height"))
        self.textHeight = QLineEdit("100.0")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textHeight)

        self.labelTemperature = QLabel(QT_TRANSLATE_NOOP("Paragon", "Temperature"))
        self.textTemperature = QLineEdit("0.0")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelTemperature)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textTemperature)

        self.labelPressure = QLabel(QT_TRANSLATE_NOOP("Paragon", "Pressure"))
        self.textPressure = QLineEdit("0.0")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelPressure)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.textPressure)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Paragon", "Description"))
        self.textDescription = QLineEdit()

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.textDescription)

        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Paragon", "Purpose"))
        self.textPurpose = QLineEdit()

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.textPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupPosition = QGroupBox(QT_TRANSLATE_NOOP("Paragon", "Position"))
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

    def initNozzle(self, theNozzItem):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Modify Nozzle"))

        self.nozzItem = theNozzItem
        self.textName.setText(theNozzItem.Name)

    # initNozzle

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

    def createNozzle(self):
        aX = float(self.textX.text)
        aY = float(self.textY.text)
        aZ = float(self.textZ.text)

        aTreeItem = PipeCad.CurrentItem()
        if aTreeItem.Type == "EQUI":
            pass
        if aTreeItem.Owner.Type == "EQUI":
            aTreeItem = aTreeItem.Owner
        else:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Equipment", "Please select EQUI to create nozzle!"))
            return
        # if

        aDir = Direction(self.textP1.text, aTreeItem)

        try:
            PipeCad.StartTransaction("Create Nozzle")

            PipeCad.CreateItem("NOZZ", self.textName.text)
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = float(self.textHeight.text)
            aNozzItem.Purpose = self.textPurpose.text
            aNozzItem.Description = self.textDescription.text
            aNozzItem.Position = Position(aX, aY, aZ, aTreeItem)
            aNozzItem.Catref = self.comboBore.currentData
            aNozzItem.Orientate("P1", aDir)
        
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # createNozzle

    def modifyNozzle(self):
        pass
    # modifyNozzle

    def accept(self):

        if self.nozzItem is None:
            self.createNozzle()
        else:
            self.modifyNozzle()
        # if

        QDialog.accept(self)
    # accept
# NozzleDialog

# Singleton.
aNozzleDlg = NozzleDialog(PipeCad)

def Create():
    aNozzleDlg.show()
# Create

def Modify():
    aNozzItem = PipeCad.CurrentItem()
    if aNozzItem.Type != "NOZZ":
        QMessageBox.warning(PipeCad, "", QT_TRANSLATE_NOOP("Design", "Please select NOZZ to modify!"))
        return
    # if

    aNozzleDlg.initNozzle(aNozzItem)
    aNozzleDlg.show()

# Modify


class ModifyDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Modify Nozzle"))

        self.verticalLayout = QVBoxLayout(self)

        # Nozzle Data.
        self.gridLayout = QGridLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Design", "Name"))
        self.textName = QLineEdit()

        self.labelAngle = QLabel(QT_TRANSLATE_NOOP("Design", "Angle"))
        self.textAngle = QLineEdit()

        self.labelOrientation = QLabel(QT_TRANSLATE_NOOP("Design", "Orientation"))
        self.comboOrientation = QComboBox()
        self.comboOrientation.addItems(["Horizontal", "Vertical"])

        self.labelDistance = QLabel(QT_TRANSLATE_NOOP("Design", "Distance"))
        self.textDistance = QLineEdit()

        self.labelElevation = QLabel(QT_TRANSLATE_NOOP("Design", "Elevation"))
        self.textElevation = QLineEdit()

        self.labelLength = QLabel(QT_TRANSLATE_NOOP("Design", "Length"))
        self.textLength = QLineEdit()

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Design", "Description"))
        self.textDescription = QLineEdit()
        self.textDescription.setMinimumWidth(180)

        self.gridLayout.addWidget(self.labelName, 0, 0)
        self.gridLayout.addWidget(self.textName, 0, 1)

        self.gridLayout.addWidget(self.labelAngle, 1, 0)
        self.gridLayout.addWidget(self.textAngle, 1, 1)

        self.gridLayout.addWidget(self.labelOrientation, 2, 0)
        self.gridLayout.addWidget(self.comboOrientation, 2, 1)

        self.gridLayout.addWidget(self.labelDistance, 3, 0)
        self.gridLayout.addWidget(self.textDistance, 3, 1)

        self.gridLayout.addWidget(self.labelElevation, 4, 0)
        self.gridLayout.addWidget(self.textElevation, 4, 1)

        self.gridLayout.addWidget(self.labelLength, 5, 0)
        self.gridLayout.addWidget(self.textLength, 5, 1)

        self.gridLayout.addWidget(self.labelDescription, 6, 0)
        self.gridLayout.addWidget(self.textDescription, 6, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        # Button Box.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        QDialog.accept(self)
    # accept

# ModifyDialog


class OrientDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.equiItem = None

        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(680, 380)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Nozzle Orientation"))

        self.verticalLayout = QVBoxLayout(self)

        # Equipment Info.
        self.gridLayout = QGridLayout()

        self.buttonCE = QPushButton("CE")
        self.buttonCE.clicked.connect(self.setEquipment)

        self.labelName = QLabel("Name")
        self.labelDescription = QLabel("Description")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addWidget(self.buttonCE, 0, 0)
        self.gridLayout.addWidget(self.labelName, 0, 1)
        self.gridLayout.addWidget(self.labelDescription, 0, 2)
        self.gridLayout.addItem(self.horizontalSpacer, 0, 3)

        self.verticalLayout.addLayout(self.gridLayout)

        # Nozzle Table.
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Angle", "Orientation", "Distance", "Elevation", "Bore", "Type", "Length", "Description"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.resizeColumnsToContents()

        self.verticalLayout.addWidget(self.tableWidget)

        # Action buttons.
        self.horizontalLayout = QHBoxLayout()

        self.buttonModify = QPushButton("Modify")
        self.buttonExport = QPushButton("Export")

        self.buttonModify.clicked.connect(self.modifyNozzle)
        self.buttonExport.clicked.connect(self.exportNozzle)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        #self.horizontalLayout.addWidget(self.buttonModify)
        self.horizontalLayout.addWidget(self.buttonExport)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def reset(self):
        self.labelName.setText("")
        self.labelDescription.setText("")
        self.tableWidget.setRowCount(0)
    # reset

    def setEquipment(self):
        aTreeItem = PipeCad.CurrentItem()
        if aTreeItem.Type != "EQUI":
            self.equiItem = None
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please select EQUI!"))
            return
        # if

        self.equiItem = aTreeItem

        self.labelName.setText(aTreeItem.Name)
        self.labelDescription.setText(aTreeItem.Description)
        self.tableWidget.setRowCount(0)

        aDz = Direction(0, 0, 1)

        aNozzles = PipeCad.CollectItem("NOZZ", aTreeItem)
        for aNozzItem in aNozzles:

            aRow = self.tableWidget.rowCount
            self.tableWidget.insertRow(aRow)

            aTableItem = QTableWidgetItem(aNozzItem.Name)
            aTableItem.setData(Qt.UserRole, aNozzItem)

            self.tableWidget.setItem(aRow, 0, aTableItem)

            aPn = aNozzItem.Position
            self.tableWidget.setItem(aRow, 4, QTableWidgetItem(str(aPn.Z)))

            aDistance = int(math.sqrt(aPn.X * aPn.X + aPn.Y * aPn.Y))

            try:
                aAngle = math.atan2(aPn.X, aPn.Y)
            except Exception as e:
                aAngle = 0
            # try

            aAngle = math.degrees(aAngle)

            if aAngle < 0:
                aAngle += 360
            # if

            aAngle = round(aAngle)

            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(str(aAngle)))
            self.tableWidget.setItem(aRow, 3, QTableWidgetItem(str(aDistance)))

            aOrientation = aNozzItem.Orientation
            if aOrientation.XDirection.IsParallel(aDz, 0.001):
                self.tableWidget.setItem(aRow, 2, QTableWidgetItem("Vertical"))
            elif aOrientation.ZDirection.IsParallel(aDz, 0.001):
                self.tableWidget.setItem(aRow, 2, QTableWidgetItem("Horizontal"))
            else:
                self.tableWidget.setItem(aRow, 2, QTableWidgetItem("--"))
            # if

            aLinkPoint = aNozzItem.linkPoint("P1")
            if aLinkPoint is not None:
                self.tableWidget.setItem(aRow, 5, QTableWidgetItem(aLinkPoint.Bore))
                self.tableWidget.setItem(aRow, 6, QTableWidgetItem(aLinkPoint.Type))
            # if

            self.tableWidget.setItem(aRow, 7, QTableWidgetItem(str(aNozzItem.Height)))
            self.tableWidget.setItem(aRow, 8, QTableWidgetItem(aNozzItem.Description))
        # for

        self.tableWidget.resizeColumnsToContents()

    # setEquipment

    def modifyNozzle(self):
        aRow = self.tableWidget.currentRow()
        if aRow < 0:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please select table item!"))
            return
        # if

        aNozzItem = self.tableWidget.item(aRow, 0).data(Qt.UserRole)
        if aNozzItem is None:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Nozzle item is invalid!"))
            return
        # if

        aModifyDlg = ModifyDialog(self)
        aModifyDlg.textName.setText(self.tableWidget.item(aRow, 0).text())
        aModifyDlg.textAngle.setText(self.tableWidget.item(aRow, 1).text())
        aModifyDlg.comboOrientation.setCurrentText(self.tableWidget.item(aRow, 2).text())
        aModifyDlg.textDistance.setText(self.tableWidget.item(aRow, 3).text())
        aModifyDlg.textElevation.setText(self.tableWidget.item(aRow, 4).text())
        aModifyDlg.textLength.setText(self.tableWidget.item(aRow, 7).text())
        aModifyDlg.textDescription.setText(self.tableWidget.item(aRow, 8).text())

        if aModifyDlg.exec() == QDialog.Accepted:
            PipeCad.SetCurrentItem(self.equiItem)
            self.setEquipment()
        # if

    # modifyNozzle

    def exportNozzle(self):
        if self.equiItem is None:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please select EQUI to export drawing!"))
            return
        # if

        aDwgPath = os.getenv(PipeCad.CurrentProject.Code + "DWG")

        aFileName = QFileDialog.getSaveFileName(self,
            QT_TRANSLATE_NOOP("Design", "Save DXF File"),
            aDwgPath + "/" + self.equiItem.Name,
            QT_TRANSLATE_NOOP("Design", "DXF Files (*.dxf)")
        )

        if len(aFileName) < 1:
            return
        # if

        # Calculate projection scale.
        aMaxDistance = 1
        for r in range (self.tableWidget.rowCount):
            aDistance = float(self.tableWidget.item(r, 3).text())
            if aMaxDistance < aDistance:
                aMaxDistance = aDistance
            # if
        # for

        aScale = 297 / (2 * aMaxDistance)
        aScales = [10, 5, 2, 1, 1/2, 1/5, 1/10, 1/20, 1/30, 1/50, 1/100]

        for s in aScales:
            if aScale > s:
                aScale = s
                break
            # if
        # for

        # Set project direction.
        aDn = Direction(0, 0, 1)
        aDx = Direction(1, 0, 0)

        PipeCad.SetProjector(self.equiItem.Position, aDn, aDx, aScale)

        # Project Equipment 
        PipeCad.AddProjectItem(self.equiItem)

        # Export projection to DXF
        PipeCad.ProjectDXF(aFileName)

        # Finish nozzle orientation drawing.
        try:
            aDxfFile = ezdxf.readfile(aFileName)
        except Exception as e:
            raise e
        # try

        aModelSpace = aDxfFile.modelspace()

        aDxfFile.styles.add("XZ", font="isocp.shx")

        # A4 297x420
        aModelSpace.add_line((-148.5, -270), (148.5, -270))
        aModelSpace.add_line((148.5, -270), (148.5, 150))
        aModelSpace.add_line((148.5, 150), (-148.5, 150))
        aModelSpace.add_line((-148.5, 150), (-148.5, -270))

        # North Arrow
        aDxfFile.layers.add(name="NORTH")
        aModelSpace.add_text("N", dxfattribs={"layer": "NORTH", "width":0.7, "style": "XZ"}).set_pos((120, 140), align="CENTER")
        aModelSpace.add_text("0%%D", dxfattribs={"layer": "NORTH", "width":0.7, "style": "XZ"}).set_pos((121, 136))
        aModelSpace.add_text("90%%D", dxfattribs={"layer": "NORTH", "width":0.7, "style": "XZ"}).set_pos((136, 121))
        aModelSpace.add_text("180%%D", dxfattribs={"layer": "NORTH", "width":0.7, "style": "XZ"}).set_pos((122, 100))
        aModelSpace.add_text("270%%D", dxfattribs={"layer": "NORTH", "width":0.7, "style": "XZ"}).set_pos((100, 121))

        aModelSpace.add_circle((120, 120), 10, dxfattribs={"layer": "NORTH"})
        aModelSpace.add_line((100, 120), (140, 120), dxfattribs={"layer": "NORTH"})
        aModelSpace.add_line((120, 100), (120, 140), dxfattribs={"layer": "NORTH"})
        aModelSpace.add_polyline2d([(120, 130, 0, 5), (120, 110)], "xyse", dxfattribs={"layer": "NORTH"})

        # Center Line.
        aDxfFile.linetypes.new("CENTER", dxfattribs={
            "description": "Center ____ _ ____ _ ____ _ ____ _ ____ _ ____",
            "pattern": [20.0, 12.5, -2.5, 2.5, -2.5]
         })

        aDxfFile.layers.add(name="EQUI_CENTER", color=4, linetype="CENTER")

        aModelSpace.add_line((-130, 0), (130, 0), dxfattribs={"layer": "EQUI_CENTER"})
        aModelSpace.add_line((0, -130), (0, 130), dxfattribs={"layer": "EQUI_CENTER"})

        # Nozzle Angles.
        aPc = PipeCad.ProjectPoint(self.equiItem.Position)

        aAngleDict = dict()
        for i in range(self.tableWidget.rowCount):
            aAngle = self.tableWidget.item(i, 1).text()
            aName = self.tableWidget.item(i, 0).text()
            aNozzItem = self.tableWidget.item(i, 0).data(Qt.UserRole)
            aOrientation = self.tableWidget.item(i, 2).text()
            aDistance = float(self.tableWidget.item(i, 3).text())

            if aDistance > 0:
                aAngleDict.setdefault(aAngle, []).append(aNozzItem)
            else:
                aSplits = aName.split("-")
                if len(aSplits) > 1:
                    aModelSpace.add_text(aSplits[-1], dxfattribs={"height": 3.5, "width":0.7, "style": "XZ"}).set_pos((aPc.X, aPc.Y))
                else:
                    aModelSpace.add_text(aName, dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((aPc.X, aPc.Y))
                # if
            # if
        # for

        for aAngle, aNozzles in aAngleDict.items():
            aPnt = PipeCad.ProjectPoint(aNozzles[0].Position)
            if aPnt is None:
                continue
            # if

            aDistance = math.sqrt(aPnt.X * aPnt.X + aPnt.Y * aPnt.Y)
            if aDistance < 0.01:
                continue
            # if

            aDx = aPnt.X / aDistance
            aDy = aPnt.Y / aDistance

            aPx = aDx * aMaxDistance * aScale + aPc.X
            aPy = aDy * aMaxDistance * aScale + aPc.Y

            aModelSpace.add_line((aPc.X, aPc.Y), (aPx, aPy), dxfattribs={"layer": "EQUI_CENTER"})
            aModelSpace.add_text(aAngle + "%%D", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((aPx + aDx * 3.5, aPy + aDy * 3.5), align="MIDDLE_CENTER")

            for i in range(len(aNozzles)):
                aNozzItem = aNozzles[i]
                aTag = aNozzItem.Name
                aSplits = aNozzItem.Name.split('-')
                if len(aSplits) > 1:
                    aTag = aSplits[-1]
                # if

                aNx = aPx + aDx * (i + 1.8) * 6
                aNy = aPy + aDy * (i + 1.8) * 6

                aModelSpace.add_text(aTag, dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((aNx, aNy), align="MIDDLE_CENTER")
                aModelSpace.add_circle((aNx, aNy), 3)
            # for
        # for

        # Draw Nozzle Table.
        aModelSpace.add_text("PipeCAD", dxfattribs={"height": 10, "width": 0.7, "style": "XZ"}).set_pos((-140, -265))
        aModelSpace.add_text(self.equiItem.Name, dxfattribs={"height": 8, "width": 0.7, "style": "XZ"}).set_pos((-90, -265))
        aModelSpace.add_text("SCALE", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-15, -268))
        aModelSpace.add_text(str(aScale), dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((0, -268))

        aModelSpace.add_text("NAME", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-145, -252))
        aModelSpace.add_text("BORE", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-130, -252))
        aModelSpace.add_text("CONNECTION TYPE", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-100, -252))
        aModelSpace.add_text("DESCRIPTION", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-35, -252))

        aModelSpace.add_text("NAME", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((3.5, -252))
        aModelSpace.add_text("BORE", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((18.5, -252))
        aModelSpace.add_text("CONNECTION TYPE", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((48.5, -252))
        aModelSpace.add_text("DESCRIPTION", dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((113.5, -252))

        aModelSpace.add_line((-98.5, -270), (-98.5, -254))
        aModelSpace.add_line((-18.5, -270), (-18.5, -254))
        aModelSpace.add_line((-2.5, -270), (-2.5, -254))
        aModelSpace.add_line((17.5, -270), (17.5, -254))
        aModelSpace.add_line((-18.5, -262), (148.5, -262))
        aModelSpace.add_line((-148.5, -254), (148.5, -254))

        aRow = round(self.tableWidget.rowCount / 2)
        aTy = -246 + aRow * 8

        aModelSpace.add_line((-148.5, -246), (148.5, -246))
        aModelSpace.add_line((-148.5, aTy), (148.5, aTy))

        aModelSpace.add_line((-132.5, aTy), (-132.5, -254))
        aModelSpace.add_line((-116.5, aTy), (-116.5, -254))
        aModelSpace.add_line((-50, aTy), (-50, -254))
        aModelSpace.add_line((0, aTy), (0, -254))
        aModelSpace.add_line((16, aTy), (16, -254))
        aModelSpace.add_line((32, aTy), (32, -254))
        aModelSpace.add_line((98.5, aTy), (98.5, -254))

        for r in range(self.tableWidget.rowCount):
            aName = self.tableWidget.item(r, 0).text()
            aBore = self.tableWidget.item(r, 5).text()
            aType = self.tableWidget.item(r, 6).text()
            #aDescription = self.tableWidget(r, 8).text()
            aSplits = aName.split('-')
            if len(aSplits) > 1:
                aName = aSplits[-1]
            # if

            if (r % 2) == 0:
                aY = -246 + int(r / 2) * 8
                aModelSpace.add_line((-148.5, aY), (148.5, aY))
            # if

            aY = -244 + int(r / 2) * 8

            aModelSpace.add_text(aName, dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-145 + 148.5 * (r % 2), aY))
            aModelSpace.add_text(aBore, dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-130 + 148.5 * (r % 2), aY))
            aModelSpace.add_text(aType, dxfattribs={"height": 3.5, "width": 0.7, "style": "XZ"}).set_pos((-114 + 148.5 * (r % 2), aY))
        # for

        # Save DXF file.
        aDxfFile.save()
    # exportNozzle

# OrientDialog

# Singleton Instance.
aOrientDlg = OrientDialog(PipeCad)

def Orient():

    aTreeItem = PipeCad.CurrentItem()
    if aTreeItem.Type == "EQUI":
        aOrientDlg.setEquipment()
    else:
        aOrientDlg.reset()
    # if

    aOrientDlg.show()
# Orient
