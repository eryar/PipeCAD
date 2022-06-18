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
# Date: 19:02 2021-11-29

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class StruDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Structure", "Create Structure"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Structure", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Structure", "Purpose"))
        self.comboPurpose = QComboBox()
        #self.comboPurpose.setEditable(True)
        self.comboPurpose.addItem("STL")
        self.comboPurpose.addItem("H&S")
        self.comboPurpose.addItem("GRID")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        try:
            PipeCad.StartTransaction("Create STRU")
            PipeCad.CreateItem("STRU", aName)
            aStruItem = PipeCad.CurrentItem()
            aStruItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# StruDialog

# Singleton Instance.
aStruDlg = StruDialog(PipeCad)

def CreateStru():
    aStruDlg.show()
# CreateStru


class FrmwDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Structure", "Create Framework"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Structure", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Structure", "Purpose"))
        self.comboPurpose = QComboBox()
        #self.comboPurpose.setEditable(True)
        self.comboPurpose.addItem("SUPP")
        self.comboPurpose.addItem("H&S")
        self.comboPurpose.addItem("LADD")
        self.comboPurpose.addItem("GRID")
        self.comboPurpose.addItem("FLOO")
        self.comboPurpose.addItem("STAI")
        self.comboPurpose.addItem("WALL")
        self.comboPurpose.addItem("WALK")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        try:
            PipeCad.StartTransaction("Create FRMW")
            PipeCad.CreateItem("FRMW", aName)
            aFrmwItem = PipeCad.CurrentItem()
            aFrmwItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# FrmwDialog

# Singleton Instance.
aFrmwDlg = FrmwDialog(PipeCad)

def CreateFrmw():
    aFrmwDlg.show()
# CreateFrmw


class SbfrDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Structure", "Create Sub-Framework"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Structure", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Structure", "Purpose"))
        self.comboPurpose = QComboBox()
        #self.comboPurpose.setEditable(True)
        self.comboPurpose.addItem("SUPP")
        self.comboPurpose.addItem("H&S")
        self.comboPurpose.addItem("LADD")
        self.comboPurpose.addItem("GRID")
        self.comboPurpose.addItem("FLOO")
        self.comboPurpose.addItem("STAI")
        self.comboPurpose.addItem("WALL")
        self.comboPurpose.addItem("WALK")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboPurpose)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        try:
            PipeCad.StartTransaction("Create SBFR")
            PipeCad.CreateItem("SBFR", aName)
            aFrmwItem = PipeCad.CurrentItem()
            aFrmwItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# SbfrDialog

# Singleton Instance.
aSbfrDlg = SbfrDialog(PipeCad)

def CreateSbfr():
    aSbfrDlg.show()
# CreateSbfr


class SectionSpecDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Structure", "Section Specification"))

        self.verticalLayout = QVBoxLayout(self)

        # Specification Data.
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Structure", "Specification Data"))

        self.formLayout = QFormLayout(self.groupBox)

        self.labelSpec = QLabel(QT_TRANSLATE_NOOP("Structure", "Specification"))
        self.comboSpec = QComboBox()
        self.comboSpec.currentIndexChanged.connect(self.specChanged)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelSpec)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboSpec)

        self.labelType = QLabel(QT_TRANSLATE_NOOP("Structure", "Generic Type"))
        self.comboType = QComboBox()
        self.comboType.currentTextChanged.connect(self.typeChanged)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelType)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboType)

        self.verticalLayout.addWidget(self.groupBox)

        # Specification List.
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Profile List"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)

        self.tableWidget.currentCellChanged.connect(self.profileChanged)

        self.verticalLayout.addWidget(self.tableWidget)

        # Pline Settings.
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Structure", "Pline Settings"))

        self.formLayout = QFormLayout(self.groupBox)

        self.labelJust = QLabel(QT_TRANSLATE_NOOP("Structure", "Jusitification"))
        self.comboJust = QComboBox()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelJust)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboJust)

        self.labelMline = QLabel(QT_TRANSLATE_NOOP("Structure", "Member Line"))
        self.comboMline = QComboBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelMline)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboMline)

        self.labelJline = QLabel(QT_TRANSLATE_NOOP("Structure", "Joint Line"))
        self.comboJline = QComboBox()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelJline)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboJline)

        self.verticalLayout.addWidget(self.groupBox)

        # Action Box.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        # Init specification data from Paragon.
        self.initSpec()
    # setupUi

    def initSpec(self):
        aSpecItems = PipeCad.CollectItem("SPEC")

        self.comboSpec.blockSignals(True)

        for aSpecItem in aSpecItems:
            if aSpecItem.Purpose == "STL":
                self.comboSpec.addItem(aSpecItem.Name, aSpecItem)
            # if
        # for

        self.comboSpec.blockSignals(False)

        if self.comboSpec.count > 0:
            self.specChanged()
        # if

        # Each p-line is identified by a two, three or four letter code (known as its PKEY) which 
        # identifies its relative position in the 2D profile (remember that each p-line is 
        # extruded in the design model to represent a line running along the length of a section). 
        # The most commonly referenced PKEYs use the following naming conventions (each profile 
        # uses only a subset of these):
        aPkeys = ["BBH",    # Bottom bolt hole
                  "BBHL",   # Bottom bolt hole, left
                  "BBHR",   # Bottom bolt hole, right
                  "BLW",    # Bottom left of web
                  "BLWT",   # Bottom left web top
                  "BOC",    # Bottom of channel
                  "BOS",    # Bottom of steel
                  "BRW",    # Bottom right of web
                  "BRWT",   # Bottom right web, top
                  "FOC",    # Face of channel
                  "HBA",    # Hole, bottom of angle
                  "HOA",    # Hole, outside of angle
                  "IOC",    # Inside of channel
                  "LBOA",   # Left bottom of angle
                  "LBOC",   # Left bottom of channel
                  "LBOS",   # Left bottom of steel
                  "LBTS",   # Left bottom top of steel
                  "LTBA",   # Left top bottom of angle
                  "LTBS",   # Left top bottom of steel
                  "LTOC",   # Left top of channel
                  "LTOS",   # Left top of steel
                  "LTTA",   # Left top of angle
                  "NA",     # Neutral axis
                  "NAB",    # Neutral axis bottom
                  "NAL",    # Neutral axis left
                  "NALO",   # Neutral axis left outside
                  "NAR",    # Neutral axis right
                  "NARO",   # Neutral axis right outside
                  "NAT",    # Neutral angle top
                  "RBOA",   # Right bottom of angle
                  "RBOC",   # Right bottom of channel
                  "RBOS",   # Right bottom of steel
                  "RBTS",   # Right bottom top of steel
                  "ROA",    # Right of angle
                  "ROC",    # Right outside of channel
                  "RTBS",   # Right top bottom of steel
                  "RTOC",   # Right top of channel
                  "RTOS",   # Right top of steel
                  "TBH",    # Top bolt hole
                  "TBHL",   # Top bolt hole, left
                  "TBHR",   # Top bolt hole, right
                  "TLW",    # Top left of web
                  "TLWB",   # Top left web, bottom
                  "TOAX",   # Top of angle, X orientation
                  "TOAY",   # Top of angle, Y orientation
                  "TOC",    # Top of channel
                  "TRWB",   # Top right web, bottom
                  "TOS",    # Top of steel
                  "TRW"     # Top right of web
                  ]

        self.comboJust.addItems(aPkeys)
        self.comboJust.setCurrentText("NA")

        self.comboMline.addItems(aPkeys)
        self.comboMline.setCurrentText("NA")

        self.comboJline.addItems(aPkeys)
        self.comboJline.setCurrentText("NA")
    # initSpec

    def specChanged(self):
        aSpecItem = self.comboSpec.currentData
        if aSpecItem is None:
            return
        # if

        self.comboType.blockSignals(True)

        for aSeleItem in aSpecItem.Member:
            self.comboType.addItem(aSeleItem.Answer, aSeleItem)
        # for

        self.comboType.blockSignals(False)

        if self.comboType.count > 0:
            self.typeChanged()
        # if
    # specChanged

    def typeChanged(self):
        self.tableWidget.setRowCount(0)

        aSeleItem = self.comboType.currentData
        if aSeleItem is None:
            return
        # if

        aSpcoList = aSeleItem.Member

        for aSpcoItem in aSpcoList:
            aCatref = aSpcoItem.Catref
            if aCatref is not None:
                aRow = self.tableWidget.rowCount
                self.tableWidget.insertRow(aRow)

                aTableItem = QTableWidgetItem(aCatref.Name)
                aTableItem.setData(Qt.UserRole, aSpcoItem)

                self.tableWidget.setItem(aRow, 0, aTableItem)
            # if
        # for
    # typeChanged

    def profileChanged(self, theCurrentRow, theCurrentColumn, thePreviousRow, thePreviousColumn):
        if theCurrentRow == thePreviousRow:
            return
        # if

    # profileChanged

# SectionSpecDialog

class SectionDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.spcoItem = None

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Structure", "Create Section"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Structure", "Specification"))

        self.formLayout = QFormLayout(self.groupBox)

        self.buttonSpec = QPushButton(QT_TRANSLATE_NOOP("Structure", "Profile..."))
        self.buttonSpec.clicked.connect(self.selectSpec)
        self.textSpec = QLineEdit()
        self.textSpec.readOnly = True

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonSpec)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textSpec)

        self.labelJust = QLabel(QT_TRANSLATE_NOOP("Structure", "Jusitification"))
        self.textJust = QLabel()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelJust)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textJust)

        self.labelMline = QLabel(QT_TRANSLATE_NOOP("Structure", "Member Line"))
        self.textMline = QLabel()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelMline)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textMline)        

        self.labelJline = QLabel(QT_TRANSLATE_NOOP("Structure", "Joint Line"))
        self.textJline = QLabel()

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelJline)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textJline)

        self.verticalLayout.addWidget(self.groupBox)

        self.tabWidget = QTabWidget()

        # Tab 1: 2 points.
        self.tabPoints = QWidget()
        self.verticalLayoutTab = QVBoxLayout(self.tabPoints)

        self.gridLayout = QGridLayout()

        self.labelX1 = QLabel("X1")
        self.textX1 = QLineEdit("0")

        self.labelX2 = QLabel("X2")
        self.textX2 = QLineEdit("0")

        self.gridLayout.addWidget(self.labelX1, 0, 0)
        self.gridLayout.addWidget(self.textX1, 0, 1)
        self.gridLayout.addWidget(self.labelX2, 0, 2)
        self.gridLayout.addWidget(self.textX2, 0, 3)

        self.labelY1 = QLabel("Y1")
        self.textY1 = QLineEdit("0")

        self.labelY2 = QLabel("Y2")
        self.textY2 = QLineEdit("0")

        self.gridLayout.addWidget(self.labelY1, 1, 0)
        self.gridLayout.addWidget(self.textY1, 1, 1)
        self.gridLayout.addWidget(self.labelY2, 1, 2)
        self.gridLayout.addWidget(self.textY2, 1, 3)

        self.labelZ1 = QLabel("Z1")
        self.textZ1 = QLineEdit("0")

        self.labelZ2 = QLabel("Z2")
        self.textZ2 = QLineEdit("0")

        self.gridLayout.addWidget(self.labelZ1, 2, 0)
        self.gridLayout.addWidget(self.textZ1, 2, 1)
        self.gridLayout.addWidget(self.labelZ2, 2, 2)
        self.gridLayout.addWidget(self.textZ2, 2, 3)        

        self.verticalLayoutTab.addLayout(self.gridLayout)

        self.tabWidget.addTab(self.tabPoints, QT_TRANSLATE_NOOP("Structure", "2 Points"))

        # Tab 2: Point and direction with distance.
        self.tabPointVector = QWidget()
        self.verticalLayoutTab = QVBoxLayout(self.tabPointVector)

        self.gridLayout = QGridLayout()

        self.labelX = QLabel("X")
        self.textX = QLineEdit("0")

        self.labelY = QLabel("Y")
        self.textY = QLineEdit("0")

        self.labelZ = QLabel("Z")
        self.textZ = QLineEdit("0")

        self.labelDir = QLabel(QT_TRANSLATE_NOOP("Structure", "Direction"))
        self.textDir = QLineEdit("N")

        self.labelDistance = QLabel(QT_TRANSLATE_NOOP("Structure", "Distance"))
        self.textDistance = QLineEdit("0")

        self.gridLayout.addWidget(self.labelX, 0, 0)
        self.gridLayout.addWidget(self.textX, 0, 1)
        self.gridLayout.addWidget(self.labelY, 1, 0)
        self.gridLayout.addWidget(self.textY, 1, 1)
        self.gridLayout.addWidget(self.labelZ, 2, 0)
        self.gridLayout.addWidget(self.textZ, 2, 1)

        self.gridLayout.addWidget(self.labelDir, 0, 2)
        self.gridLayout.addWidget(self.textDir, 0, 3)

        self.gridLayout.addWidget(self.labelDistance, 1, 2)
        self.gridLayout.addWidget(self.textDistance, 1, 3)

        self.verticalLayoutTab.addLayout(self.gridLayout)

        self.tabWidget.addTab(self.tabPointVector, QT_TRANSLATE_NOOP("Structure", "Point and Vector"))

        self.verticalLayout.addWidget(self.tabWidget)

        # Action Box.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

    # setupUi

    def selectSpec(self):
        aSpecDlg = SectionSpecDialog(self)
        if aSpecDlg.exec() != QDialog.Accepted:
            return
        # if

        aRow = aSpecDlg.tableWidget.currentRow()
        if aRow < 0:
            return
        # if

        aTableItem = aSpecDlg.tableWidget.item(aRow, 0)
        if aTableItem is None:
            return
        # if

        aSpcoItem = aTableItem.data(Qt.UserRole)
        if aSpcoItem is None:
            return
        # if

        self.spcoItem = aSpcoItem

        self.textSpec.setText(aSpcoItem.Catref.Name)

        self.textJust.setText(aSpecDlg.comboJust.currentText)
        self.textMline.setText(aSpecDlg.comboMline.currentText)
        self.textJline.setText(aSpecDlg.comboJline.currentText)
    # selectSpec

    def accept(self):
        aIndex = self.tabWidget.currentIndex
        if aIndex == 0:
            # 2 Points
            aX = float(self.textX1.text)
            aY = float(self.textY1.text)
            aZ = float(self.textZ1.text)

            aPs = Position(aX, aY, aZ)

            aX = float(self.textX2.text)
            aY = float(self.textY2.text)
            aZ = float(self.textZ2.text)

            aPe = Position(aX, aY, aZ)

            PipeCad.StartTransaction("Create Section")
            PipeCad.CreateItem("SCTN")
            aSctnItem = PipeCad.CurrentItem()
            aSctnItem.StartPosition = aPs
            aSctnItem.EndPosition = aPe
            aSctnItem.Spref = self.spcoItem

            PipeCad.CommitTransaction()
        elif aIndex == 1:
            # Point and Vector
            aX = float(self.textX.text)
            aY = float(self.textY.text)
            aZ = float(self.textZ.text)
            aL = float(self.textDistance.text)
            aDir = Direction(self.textDir.text)

            aPs = Position(aX, aY, aZ)
            aPe = aPs.Offset(aDir, aL)

            PipeCad.StartTransaction("Create Section")
            PipeCad.CreateItem("SCTN")
            aSctnItem = PipeCad.CurrentItem()
            aSctnItem.StartPosition = aPs
            aSctnItem.EndPosition = aPe
            aSctnItem.Spref = self.spcoItem

            PipeCad.CommitTransaction()
        # if

        QDialog.accept(self)
    # accept

# SectionDialog

# Singleton Instance.
aSctnDlg = SectionDialog(PipeCad)

def CreateSctn():
    aSctnDlg.show()
# CreateSctn

class RegularDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(390, 580)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Structure", "Regular Structure"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupColumn = QGroupBox()
        self.groupColumn.setTitle("Column Data")

        self.formLayout = QFormLayout(self.groupColumn)

        self.buttonColumnArea = QPushButton("Storage Area")
        self.buttonColumnArea.clicked.connect(self.setColumnArea)

        self.textColumnArea = QLineEdit()
        self.textColumnArea.readOnly = True

        self.columnArea = None

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonColumnArea)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textColumnArea)

        self.buttonColumn = QPushButton("Set Profile ")
        self.buttonColumn.clicked.connect(self.selectColumnSpec)

        self.textColumn = QLineEdit()
        self.textColumn.readOnly = True

        self.columnSpec = None
        
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.buttonColumn)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textColumn)

        self.labelColumnJustification = QLabel("Jusitification")
        self.textColumnJustification = QLabel("<font color=Brown>NA</font>")
        
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelColumnJustification)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textColumnJustification)

        self.labelColumnMemberLine = QLabel("Member Line")
        self.textColumnMemberLine = QLabel("<font color=Brown>NA</font>")
        
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelColumnMemberLine)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textColumnMemberLine)

        self.labelColumnJointLine = QLabel("Joint Line")
        self.textColumnJointLine = QLabel("<font color=Brown>NA</font>")
        
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelColumnJointLine)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textColumnJointLine)

        self.verticalLayout.addWidget(self.groupColumn)

        self.groupBeam = QGroupBox()
        self.groupBeam.setTitle("Beam Data")

        self.formLayout = QFormLayout(self.groupBeam)

        self.buttonBeamArea = QPushButton("Storage Area")
        self.buttonBeamArea.clicked.connect(self.setBeamArea)

        self.textBeamArea = QLineEdit()

        self.beamArea = None

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonBeamArea)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textBeamArea)

        self.buttonBeam = QPushButton("Set Profile ")
        self.buttonBeam.clicked.connect(self.selectBeamSpec)

        self.textBeam = QLineEdit()
        self.textBeam.readOnly = True

        self.beamSpec = None
        
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.buttonBeam)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textBeam)

        self.labelBeamJustification = QLabel("Jusitification")
        self.textBeamJustification = QLabel("<font color=Brown>NA</font>")
        
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelBeamJustification)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textBeamJustification)

        self.labelBeamMemberLine = QLabel("Member Line")
        self.textBeamMemberLine = QLabel("<font color=Brown>NA</font>")
        
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelBeamMemberLine)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textBeamMemberLine)

        self.labelBeamJointLine = QLabel("Joint Line")
        self.textBeamJointLine = QLabel("<font color=Brown>NA</font>")
        
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelBeamJointLine)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textBeamJointLine)

        self.verticalLayout.addWidget(self.groupBeam)

        self.gridLayout = QGridLayout()
        self.labelEast = QLabel("East Spacings")
        self.labelNorth = QLabel("North Spacings")
        self.labelElev = QLabel("Elevation")

        self.gridLayout.addWidget(self.labelEast, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.labelNorth, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.labelElev, 0, 2, 1, 1)

        self.textEast = QPlainTextEdit()
        self.textNorth = QPlainTextEdit()
        self.textElev = QPlainTextEdit()

        self.gridLayout.addWidget(self.textEast, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.textNorth, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.textElev, 1, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonPreview = QPushButton()
        self.buttonPreview.setText(QT_TRANSLATE_NOOP("Structure", "Preview"))
        self.buttonPreview.setDefault(True)
        self.buttonPreview.clicked.connect(self.preview)

        self.horizontalLayout.addWidget(self.buttonPreview)

        self.buttonBuild = QPushButton()
        self.buttonBuild.setText(QT_TRANSLATE_NOOP("Structure", "Build"))
        self.buttonBuild.clicked.connect(self.build)

        self.horizontalLayout.addWidget(self.buttonBuild)

        self.buttonCancel = QPushButton()
        self.buttonCancel.setText(QT_TRANSLATE_NOOP("Structure", "Cancel"))
        self.buttonCancel.clicked.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.aidNumber = PipeCad.NextAidNumber()
        
    # setupUi

    def setColumnArea(self):
        aTreeItem = PipeCad.CurrentItem()
        if aTreeItem.Type in ["FRMW", "SBFR"]:
            aName = aTreeItem.Name
            if len(aName) < 1:
                aName = aTreeItem.RefNo
            # if

            self.textColumnArea.setText(aName)

            self.columnArea = aTreeItem
        else:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Structure", "Please select FRMW/SBFR to store column!"))
        # if
    # setColumnArea

    def selectColumnSpec(self):
        aSpecDlg = SectionSpecDialog(self)
        if aSpecDlg.exec() != QDialog.Accepted:
            return
        # if

        aRow = aSpecDlg.tableWidget.currentRow()
        if aRow < 0:
            return
        # if

        aTableItem = aSpecDlg.tableWidget.item(aRow, 0)
        if aTableItem is None:
            return
        # if

        aSpcoItem = aTableItem.data(Qt.UserRole)
        if aSpcoItem is None:
            return
        # if

        self.columnSpec = aSpcoItem

        self.textColumn.setText(aSpcoItem.Catref.Name)

        self.textColumnJustification.setText(aSpecDlg.comboJust.currentText)
        self.textColumnMemberLine.setText(aSpecDlg.comboMline.currentText)
        self.textColumnJointLine.setText(aSpecDlg.comboJline.currentText)
    # selectColumnSpec

    def setBeamArea(self):
        aTreeItem = PipeCad.CurrentItem()
        if aTreeItem.Type in ["FRMW", "SBFR"]:
            aName = aTreeItem.Name
            if len(aName) < 1:
                aName = aTreeItem.RefNo
            # if

            self.textBeamArea.setText(aName)

            self.beamArea = aTreeItem
        else:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Structure", "Please select FRMW/SBFR to store beam!"))
        # if
    # setBeamArea

    def selectBeamSpec(self):
        aSpecDlg = SectionSpecDialog(self)
        if aSpecDlg.exec() != QDialog.Accepted:
            return
        # if

        aRow = aSpecDlg.tableWidget.currentRow()
        if aRow < 0:
            return
        # if

        aTableItem = aSpecDlg.tableWidget.item(aRow, 0)
        if aTableItem is None:
            return
        # if

        aSpcoItem = aTableItem.data(Qt.UserRole)
        if aSpcoItem is None:
            return
        # if

        self.beamSpec = aSpcoItem

        self.textBeam.setText(aSpcoItem.Catref.Name)

        self.textBeamJustification.setText(aSpecDlg.comboJust.currentText)
        self.textBeamMemberLine.setText(aSpecDlg.comboMline.currentText)
        self.textBeamJointLine.setText(aSpecDlg.comboJline.currentText)
    # selectBeamSpec

    def preview(self):
    
        PipeCad.RemoveAid(self.aidNumber)
        
        aLx = []
        aLy = []
        aLz = []
        
        # East Spacings
        aSpacings = self.textEast.plainText.split("\n")
        for x in aSpacings:
            aLx.append(float(x))
        # for
        
        # North Spacings
        aSpacings = self.textNorth.plainText.split("\n")
        for y in aSpacings:
            aLy.append(float(y))
        # for
        
        # Elevation
        aSpacings = self.textElev.plainText.split("\n")
        for z in aSpacings:
            aLz.append(float(z))
        # for
        
        aPs = Position(0, 0, 0)
        aPe = Position(0, 0, 0)

        # Draw aid line in elevations.
        for e in aLz:
            aPs.z = aPe.z
            aPe.z += e

            aPs.x = 0
            aPe.x = 0

            for x in aLx:
                aPs.x += x
                aPe.x += x
                aPs.y = 0
                aPe.y = 0
                for y in aLy:
                    aPs.y += y
                    aPe.y += y
                    PipeCad.AddAidLine(aPs, aPe, self.aidNumber)
                # for
            # for
        # for

        # Draw aid line in x direction.
        aPs = Position(0.0, 0.0, 0.0)
        aPe = Position(0.0, 0.0, 0.0)
        for x in aLx: 
            aPs.x = aPe.x
            aPe.x += x

            aPs.y = 0
            aPe.y = 0

            for y in aLy:
                aPs.y += y
                aPe.y += y
                aPs.z = 0
                aPe.z = 0
                for e in aLz:
                    aPs.z += e
                    aPe.z += e
                    PipeCad.AddAidLine(aPs, aPe, self.aidNumber)
                # for
            # for
        # for

        # Draw aid line in y direction.
        aPs = Position(0.0, 0.0, 0.0)
        aPe = Position(0.0, 0.0, 0.0)
        for y in aLy: 
            aPs.y = aPe.y
            aPe.y += y

            aPs.x = 0
            aPe.x = 0

            for x in aLx:
                aPs.x += x
                aPe.x += x
                aPs.z = 0
                aPe.z = 0
                for e in aLz:
                    aPs.z += e
                    aPe.z += e
                    PipeCad.AddAidLine(aPs, aPe, self.aidNumber)
                # for
            # for
        # for
        
        PipeCad.UpdateViewer()
    # preview
        
    def build(self):
        aColumnArea = self.columnArea
        if aColumnArea is None:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Structure", "Please enter Column Storage Area!"))
            return
        # if

        aBeamArea = self.beamArea
        if aBeamArea is None:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Structure", "Please enter Beam Storage Area!"))
            return
        # if

        aColumnSpec = self.columnSpec
        if aColumnSpec is None:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Structure", "Please enter Column Profile Spec!"))
            return
        # if

        aBeamSpec = self.beamSpec
        if aBeamSpec is None:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Structure", "Please enter Beam Profile Spec!"))
            return
        # if

        aLx = []
        aLy = []
        aLz = []
        
        # East Spacings
        aSpacings = self.textEast.plainText.split("\n")
        for x in aSpacings:
            aLx.append(float(x))
        # for
        
        # North Spacings
        aSpacings = self.textNorth.plainText.split("\n")
        for y in aSpacings:
            aLy.append(float(y))
        # for
        
        # Elevation
        aSpacings = self.textElev.plainText.split("\n")
        for z in aSpacings:
            aLz.append(float(z))
        # for

        PipeCad.StartTransaction("Create Structure")
        PipeCad.SetCurrentItem(aBeamArea)

        # Draw aid line in elevations.
        aPs = Position(0, 0, 0)
        aPe = Position(0, 0, 0)
        for e in aLz:
            aPs.z = aPe.z
            aPe.z += e

            aPs.x = 0
            aPe.x = 0

            for x in aLx:
                aPs.x += x
                aPe.x += x
                aPs.y = 0
                aPe.y = 0
                for y in aLy:
                    aPs.y += y
                    aPe.y += y

                    if aPs.distance(aPe) > 1.0:
                        PipeCad.CreateItem("SCTN")
                        aSctnItem = PipeCad.CurrentItem()
                        aSctnItem.StartPosition = aPs
                        aSctnItem.EndPosition = aPe
                        aSctnItem.Spref = aBeamSpec
                    # if
                # for
            # for
        # for

        PipeCad.SetCurrentItem(aColumnArea)
        # Draw aid line in x direction.
        aPs = Position(0.0, 0.0, 0.0)
        aPe = Position(0.0, 0.0, 0.0)
        for x in aLx: 
            aPs.x = aPe.x
            aPe.x += x

            aPs.y = 0
            aPe.y = 0

            for y in aLy:
                aPs.y += y
                aPe.y += y
                aPs.z = 0
                aPe.z = 0
                for e in aLz:
                    aPs.z += e
                    aPe.z += e
                    if aPs.distance(aPe) > 1.0:
                        PipeCad.CreateItem("SCTN")
                        aSctnItem = PipeCad.CurrentItem()
                        aSctnItem.StartPosition = aPs
                        aSctnItem.EndPosition = aPe
                        aSctnItem.Spref = aColumnSpec
                    # if
                # for
            # for
        # for

        PipeCad.SetCurrentItem(aColumnArea)
        # Draw aid line in y direction.
        aPs = Position(0.0, 0.0, 0.0)
        aPe = Position(0.0, 0.0, 0.0)
        for y in aLy: 
            aPs.y = aPe.y
            aPe.y += y

            aPs.x = 0
            aPe.x = 0

            for x in aLx:
                aPs.x += x
                aPe.x += x
                aPs.z = 0
                aPe.z = 0
                for e in aLz:
                    aPs.z += e
                    aPe.z += e
                    if aPs.distance(aPe) > 1.0:
                        PipeCad.CreateItem("SCTN")
                        aSctnItem = PipeCad.CurrentItem()
                        aSctnItem.StartPosition = aPs
                        aSctnItem.EndPosition = aPe
                        aSctnItem.Spref = aColumnSpec
                    # if
                # for
            # for
        # for

        PipeCad.CommitTransaction()
    # build

    def reject(self):
        PipeCad.RemoveAid(self.aidNumber)
        QDialog.reject(self)
    # reject

# Singleton Instance.
aRegularDlg = RegularDialog(PipeCad)

def CreateRegular():
    aRegularDlg.show()
# Create
