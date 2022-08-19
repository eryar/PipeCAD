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
# Date: 12:02 2021-12-20

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
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Create Bolt Table"))

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

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):

        aName = self.lineEditName.text
        aPurpose = self.comboPurpose.currentText

        if len(aName) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Paragon", "Please input bolt table name!"))
            return
        # if

        PipeCad.StartTransaction("Create Bolt Table")

        PipeCad.CreateItem("BLTA", aName)
        aCctaItem = PipeCad.CurrentItem()
        aCctaItem.Purpose = aPurpose

        PipeCad.CommitTransaction()

        QDialog.accept(self)
    # accept

# Singleton Instance.
aCreateDlg = CreateDialog(PipeCad)

def Create():
    aCreateDlg.show()
# Create

class InputDialog(QDialog):
    def __init__(self, theTitle, parent = None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(theTitle)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()
        self.labelName = QLabel(QT_TRANSLATE_NOOP("aPurpose", "Name"))
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(180)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def getName(self):
        return self.textName.text
    # getName
# InputDialog


class BoltDialog(QDialog):
    def __init__(self, theBltaItem, theBlisItem, parent = None):
        QDialog.__init__(self, parent)

        self.bltaItem = theBltaItem
        self.blisItem = theBlisItem
        self.sbolItem = None

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Single Bolt"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        self.labelName = QLabel("Bolt Name")
        self.textName = QLineEdit()

        self.labelDiameter = QLabel("Diameter")
        self.textDiameter = QLineEdit("0")

        self.labelLength = QLabel("Length")
        self.textLength = QLineEdit("0")

        self.labelNumber = QLabel("Number")
        self.textNumber = QLineEdit("0")

        self.labelExtra = QLabel("Extra Length")
        self.textExtra = QLineEdit("0")

        self.labelStd = QLabel("Std Length")
        self.comboStd = QComboBox()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDiameter)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDiameter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelLength)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textLength)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelNumber)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textNumber)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelExtra)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textExtra)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelStd)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.comboStd)

        self.verticalLayout.addLayout(self.formLayout)

        # Bolt Item table.
        self.tableBoltItem = QTableWidget()
        self.tableBoltItem.setColumnCount(2)
        self.tableBoltItem.setAlternatingRowColors(True)
        self.tableBoltItem.setHorizontalHeaderLabels(["Type", "Length"])
        self.tableBoltItem.horizontalHeader().setStretchLastSection(True)
        self.tableBoltItem.horizontalHeader().setDefaultSectionSize(50)
        self.tableBoltItem.verticalHeader().setDefaultSectionSize(18)
        self.tableBoltItem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableBoltItem.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableBoltItem.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableBoltItem.cellClicked.connect(self.boltItemClicked)

        self.verticalLayout.addWidget(self.tableBoltItem)

        self.horizontalLayout = QHBoxLayout()
        self.comboItemType = QComboBox()
        self.comboItemType.addItems(["NUT", "WASH"])
        self.textItemLength = QLineEdit("0")

        self.buttonAdd = QPushButton(QIcon(":/PipeCad/Resources/plus.png"), "")
        self.buttonAdd.setToolTip("Add Item")
        self.buttonAdd.clicked.connect(self.addBoltItem)

        self.buttonModify = QPushButton(QIcon(":/PipeCad/Resources/modify_bolt.png"), "")
        self.buttonModify.setToolTip("Modify Item")
        self.buttonModify.clicked.connect(self.modifyBoltItem)

        self.buttonDelete = QPushButton(QIcon(":/PipeCad/Resources/minus.png"), "")
        self.buttonDelete.setToolTip("Delete Item")
        self.buttonDelete.clicked.connect(self.deleteBoltItem)

        self.horizontalLayout.addWidget(self.comboItemType)
        self.horizontalLayout.addWidget(self.textItemLength)
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonDelete)
        self.horizontalLayout.addWidget(self.buttonModify)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Button Box: OK/Cancel.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def reset(self, theSbolItem = None):
        # Init STD length.
        aDtabList = PipeCad.CollectItem("DTAB", self.bltaItem)
        for aDtabItem in aDtabList:
            self.comboStd.addItem(aDtabItem.Name, aDtabItem)
        # for

        # Set Single Bolt info.
        if theSbolItem is None:
            return
        # if

        self.comboStd.setCurrentText(theSbolItem.Stdblength.Name)

        self.sbolItem = theSbolItem

        self.textName.setText(theSbolItem.Name)
        self.textDiameter.setText(theSbolItem.Bdiameter)
        self.textLength.setText(theSbolItem.Length)
        self.textNumber.setText(theSbolItem.Noff)

        aBoltItems = theSbolItem.Bitems.split()
        aItemLength = theSbolItem.Bitlength.split()
        if len(aBoltItems) == len(aItemLength):
            aRow = len(aBoltItems)
            self.tableBoltItem.setRowCount(aRow)

            for i in range(aRow):
                self.tableBoltItem.setItem(i, 0, QTableWidgetItem(aBoltItems[i]))
                self.tableBoltItem.setItem(i, 1, QTableWidgetItem(aItemLength[i]))
            # for
        # if
    # reset

    def boltItemClicked(self, theRow):
        aType = self.tableBoltItem.item(theRow, 0).text()
        aLength = self.tableBoltItem.item(theRow, 1).text()

        self.comboItemType.setCurrentText(aType)
        self.textItemLength.setText(aLength)
    # boltItemClicked

    def addBoltItem(self):
        aItem = self.comboItemType.currentText
        aLength = self.textItemLength.text

        aRow = self.tableBoltItem.rowCount
        self.tableBoltItem.insertRow(aRow)
        self.tableBoltItem.setItem(aRow, 0, QTableWidgetItem(aItem))
        self.tableBoltItem.setItem(aRow, 1, QTableWidgetItem(aLength))
    # addBoltItem

    def modifyBoltItem(self):
        aRow = self.tableBoltItem.currentRow()
        if aRow < 0:
            return
        # if

        aItem = self.comboItemType.currentText
        aLength = self.textItemLength.text
        
        self.tableBoltItem.setItem(aRow, 0, QTableWidgetItem(aItem))
        self.tableBoltItem.setItem(aRow, 1, QTableWidgetItem(aLength))

    # modifyBoltItem

    def deleteBoltItem(self):
        aRow = self.tableBoltItem.currentRow()
        if aRow < 0:
            return
        # if

        aAnswer = QMessageBox.question(self, "", "Are you sure to delete the item?")
        if aAnswer == QMessageBox.No:
            return
        # if

        self.tableBoltItem.removeRow(aRow)
    # deleteBoltItem

    def accept(self):
        if self.blisItem is None:
            return
        # if

        # Create Single Bolt.
        aMemberList = self.blisItem.Member
        if len(aMemberList) > 0:
            PipeCad.SetCurrentItem(aMemberList[-1])
        else:
            PipeCad.SetCurrentItem(self.blisItem)
        # if

        try:
            PipeCad.StartTransaction("Single Bolt")

            aSbolItem = self.sbolItem
            if aSbolItem is None:
                PipeCad.CreateItem("SBOL", self.textName.text)
                aSbolItem = PipeCad.CurrentItem()
            # if

            aSbolItem.Bdiameter = self.textDiameter.text
            aSbolItem.Length = float(self.textLength.text)
            aSbolItem.Noff = int(self.textNumber.text)
            aSbolItem.Xtralength = float(self.textExtra.text)
            aSbolItem.Stdblength = self.comboStd.currentData

            # Set bolt items.
            aBitems = []
            aBitlength = []
            for i in range(self.tableBoltItem.rowCount):
                aItem = self.tableBoltItem.item(i, 0).text()
                aLength = self.tableBoltItem.item(i, 1).text()

                aBitems.append(aItem)
                aBitlength.append(aLength)
            # for

            aSbolItem.Bitems = " ".join(aBitems)
            aSbolItem.Bitlength = " ".join(aBitlength)

            PipeCad.CommitTransaction()
        except Exception as e:
            raise e
        # try

        QDialog.accept(self)
    # accept

# BoltDialog


class ModifyDialog(QDialog):
    """docstring for ModifyDialog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.boltTable = None
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(680, 600)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Modify Bolt Table"))

        self.verticalLayout = QVBoxLayout(self)

        # CE
        self.formLayout = QFormLayout()
        self.buttonCe = QPushButton("CE")
        self.labelCe = QLabel("")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonCe)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.labelCe)

        self.buttonCe.clicked.connect(self.reset)

        self.verticalLayout.addLayout(self.formLayout)

        # Tab Widgets.
        self.tabWidget = QTabWidget()

        # Bolt Length Tabe.
        self.tabLength = QWidget()
        self.tabWidget.addTab(self.tabLength, QT_TRANSLATE_NOOP("Paragon", "Bolt Length"))

        self.verticalLayoutTab = QVBoxLayout(self.tabLength)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Paragon", "Length Table"))
        self.verticalLayoutTab.addWidget(self.groupBox)
        self.horizontalLayoutBox = QHBoxLayout(self.groupBox)

        self.tableLength = QTableWidget(self.groupBox)
        self.tableLength.setColumnCount(1)
        self.tableLength.setAlternatingRowColors(True)
        self.tableLength.setHorizontalHeaderLabels(["Length Table Name"])
        self.tableLength.horizontalHeader().setStretchLastSection(True)
        self.tableLength.verticalHeader().setDefaultSectionSize(18)
        self.tableLength.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableLength.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableLength.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableLength.itemClicked.connect(self.lengthTableClicked)

        self.horizontalLayoutBox.addWidget(self.tableLength)

        self.verticalLayoutTemp = QVBoxLayout()
        self.buttonAddLength = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Add Length Table"))
        self.buttonDelLength = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Delete Length Table"))
        aSpacerItem = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.buttonAddLength.clicked.connect(self.addLengthTable)
        self.buttonDelLength.clicked.connect(self.delLengthTable)

        self.verticalLayoutTemp.addWidget(self.buttonAddLength)
        self.verticalLayoutTemp.addWidget(self.buttonDelLength)
        self.verticalLayoutTemp.addItem(aSpacerItem)

        self.horizontalLayoutBox.addLayout(self.verticalLayoutTemp)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Paragon", "Diameter Table"))
        self.verticalLayoutTab.addWidget(self.groupBox)
        self.horizontalLayoutBox = QHBoxLayout(self.groupBox)

        self.verticalLayoutTemp = QVBoxLayout()
        self.tableDiameter = QTableWidget()
        self.tableDiameter.setColumnCount(1)
        self.tableDiameter.setAlternatingRowColors(True)
        self.tableDiameter.setHorizontalHeaderLabels(["Diameter Table Name"])
        self.tableDiameter.horizontalHeader().setStretchLastSection(True)
        self.tableDiameter.verticalHeader().setDefaultSectionSize(18)
        self.tableDiameter.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableDiameter.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableDiameter.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableDiameter.itemClicked.connect(self.diameterTableClicked)

        self.horizontalLayout = QHBoxLayout()
        self.buttonAddDiameter = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Add Diameter Table"))
        self.buttonDelDiameter = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Delete Diameter Table"))
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addWidget(self.buttonAddDiameter)
        self.horizontalLayout.addWidget(self.buttonDelDiameter)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonAddDiameter.clicked.connect(self.addDiameterTable)
        self.buttonDelDiameter.clicked.connect(self.delDiameterTable)

        self.verticalLayoutTemp.addWidget(self.tableDiameter)
        self.verticalLayoutTemp.addLayout(self.horizontalLayout)

        self.horizontalLayoutBox.addLayout(self.verticalLayoutTemp)

        # Create Length Values.
        self.verticalLayoutTemp = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.labelStart = QLabel(QT_TRANSLATE_NOOP("Paragon", "Length Start"))
        self.textStart = QLineEdit("0")
        self.labelInterval = QLabel(QT_TRANSLATE_NOOP("Paragon", "Length Interval"))
        self.textInterval = QLineEdit("0")
        self.labelEnd = QLabel(QT_TRANSLATE_NOOP("Paragon", "Length End"))
        self.textEnd = QLineEdit("0")
        self.buttonBuild = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Build"))
        self.buttonBuild.clicked.connect(self.buildLength)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelStart)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textStart)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelEnd)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textEnd)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelInterval)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textInterval)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.buttonBuild)

        self.verticalLayoutTemp.addLayout(self.formLayout)

        self.horizontalLayoutBox.addLayout(self.verticalLayoutTemp)

        # Length
        self.verticalLayoutTemp = QVBoxLayout()
        self.tableItem = QTableWidget()
        self.tableItem.setColumnCount(1)
        self.tableItem.setAlternatingRowColors(True)
        self.tableItem.setHorizontalHeaderLabels(["Length"])
        self.tableItem.horizontalHeader().setStretchLastSection(True)
        self.tableItem.verticalHeader().setDefaultSectionSize(18)
        #self.tableItem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableItem.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableItem.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.horizontalLayout = QHBoxLayout()
        self.buttonDelItem = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Delete Length"))
        self.buttonDelItem.clicked.connect(self.deleteLengthItem)

        self.buttonApplyItem = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Apply"))
        self.buttonApplyItem.clicked.connect(self.applyLengthItem)

        self.horizontalLayout.addWidget(self.buttonDelItem)
        self.horizontalLayout.addWidget(self.buttonApplyItem)
        #aSpacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.horizontalLayout.addItem(aSpacerItem)

        self.verticalLayoutTemp.addWidget(self.tableItem)
        self.verticalLayoutTemp.addLayout(self.horizontalLayout)
        self.horizontalLayoutBox.addLayout(self.verticalLayoutTemp)

        # Single Bolt Tab.
        self.tabBolt = QWidget()
        self.tabWidget.addTab(self.tabBolt, QT_TRANSLATE_NOOP("Paragon", "Single Bolt"))

        self.verticalLayoutTab = QVBoxLayout(self.tabBolt)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Paragon", "Single Bolt List"))
        self.verticalLayoutTab.addWidget(self.groupBox)

        self.horizontalLayoutBox = QHBoxLayout(self.groupBox)
        self.tableBoltList = QTableWidget(self.groupBox)
        self.tableBoltList.setColumnCount(1)
        self.tableBoltList.setAlternatingRowColors(True)
        self.tableBoltList.setHorizontalHeaderLabels(["Bolt Name"])
        self.tableBoltList.horizontalHeader().setStretchLastSection(True)
        self.tableBoltList.verticalHeader().setDefaultSectionSize(18)
        self.tableBoltList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableBoltList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableBoltList.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableBoltList.itemClicked.connect(self.boltListClicked)

        self.horizontalLayoutBox.addWidget(self.tableBoltList)

        self.verticalLayoutTemp = QVBoxLayout()
        self.buttonAddBoltList = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Add Single Bolt List"))
        self.buttonDelBoltList = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Delete Single Bolt List"))
        aSpacerItem = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.buttonAddBoltList.clicked.connect(self.addBoltList)
        self.buttonDelBoltList.clicked.connect(self.deleteBoltList)

        self.verticalLayoutTemp.addWidget(self.buttonAddBoltList)
        self.verticalLayoutTemp.addWidget(self.buttonDelBoltList)
        self.verticalLayoutTemp.addItem(aSpacerItem)

        self.horizontalLayoutBox.addLayout(self.verticalLayoutTemp)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Paragon", "Single Bolt Elements"))
        self.verticalLayoutTab.addWidget(self.groupBox)

        self.verticalLayoutBox = QVBoxLayout(self.groupBox)

        self.tableBoltItem = QTableWidget()
        self.tableBoltItem.setColumnCount(6)
        self.tableBoltItem.setAlternatingRowColors(True)
        self.tableBoltItem.setHorizontalHeaderLabels(["Bolt Name", "Diameter", "Length", "Number", "Extra Length", "Std Bolt Length"])
        self.tableBoltItem.horizontalHeader().setStretchLastSection(True)
        self.tableBoltItem.horizontalHeader().setDefaultSectionSize(80)
        self.tableBoltItem.verticalHeader().setDefaultSectionSize(18)
        self.tableBoltItem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableBoltItem.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableBoltItem.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayoutBox.addWidget(self.tableBoltItem)

        self.horizontalLayoutBox = QHBoxLayout()
        self.buttonAddBolt = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Add Bolt"))
        self.buttonModBolt = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Modify Bolt"))
        self.buttonDelBolt = QPushButton(QT_TRANSLATE_NOOP("Paragon", "Delete Bolt"))
        aSpacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttonAddBolt.clicked.connect(self.addBolt)
        self.buttonModBolt.clicked.connect(self.modifyBolt)
        self.buttonDelBolt.clicked.connect(self.deleteBolt)

        self.horizontalLayoutBox.addWidget(self.buttonAddBolt)
        self.horizontalLayoutBox.addWidget(self.buttonModBolt)
        self.horizontalLayoutBox.addWidget(self.buttonDelBolt)
        self.horizontalLayoutBox.addItem(aSpacerItem)

        self.verticalLayoutBox.addLayout(self.horizontalLayoutBox)

        self.verticalLayout.addWidget(self.tabWidget)

        # ButtonBox.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel, self)
        #self.buttonBox.setStandardButtons()

        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.rejected.connect(self.reject)

    # setupUi

    def reset(self):
        aBltaItem = PipeCad.CurrentItem()
        self.boltTable = aBltaItem

        self.labelCe.setText(aBltaItem.Name)

        self.resetBoltLength(aBltaItem)
        self.resetSingleBolt(aBltaItem)
    # reset

    def resetBoltLength(self, theBltaItem):
        # Init Length Table.
        self.tableLength.setRowCount(0)

        aMemberList = theBltaItem.Member
        for aMember in aMemberList:
            if aMember.Type == "LTAB":
                aRow = self.tableLength.rowCount
                aTableItem = QTableWidgetItem(aMember.Name)
                aTableItem.setData(Qt.UserRole, aMember)
                self.tableLength.insertRow(aRow)
                self.tableLength.setItem(aRow, 0, aTableItem)
            # if
        # for

        self.tableDiameter.setRowCount(0)
        self.tableItem.setRowCount(0)

        if self.tableLength.rowCount > 0:
            aTableItem = self.tableLength.item(0, 0)
            self.tableLength.setCurrentItem(aTableItem)
            self.lengthTableClicked(aTableItem)
        # if
    # resetBoltLength

    def resetSingleBolt(self, theBltaItem):
        self.tableBoltList.setRowCount(0)

        aMemberList = theBltaItem.Member
        for aMember in aMemberList:
            if aMember.Type == "BLIS":
                aRow = self.tableBoltList.rowCount
                aTableItem = QTableWidgetItem(aMember.Name)
                aTableItem.setData(Qt.UserRole, aMember)

                self.tableBoltList.insertRow(aRow)
                self.tableBoltList.setItem(aRow, 0, aTableItem)
            # if
        # for

        if self.tableBoltList.rowCount > 0:
            aTableItem = self.tableBoltList.item(0, 0)
            self.tableBoltList.setCurrentItem(aTableItem)
            self.boltListClicked(aTableItem)
        # if
    # resetSingleBolt

    def lengthTableClicked(self, theTableItem):
        aLtabItem = theTableItem.data(Qt.UserRole)
        if aLtabItem is None:
            self.tableDiameter.setRowCount(0)
            return
        # if

        aMemberList = aLtabItem.Member        
        self.tableDiameter.setRowCount(len(aMemberList))
        for i in range (len(aMemberList)):
            aDtabItem = aMemberList[i]
            aTableItem = QTableWidgetItem(aDtabItem.Name)
            aTableItem.setData(Qt.UserRole, aDtabItem)

            self.tableDiameter.setItem(i, 0, aTableItem)
        # for

        if self.tableDiameter.rowCount > 0:
            aTableItem = self.tableDiameter.item(0, 0)
            self.tableDiameter.setCurrentItem(aTableItem)
            self.diameterTableClicked(aTableItem)
        # if

    # lengthTableClicked

    def diameterTableClicked(self, theTableItem):
        aDtabItem = theTableItem.data(Qt.UserRole)
        if aDtabItem is None:
            self.tableItem.setRowCount(0)
            return
        # if

        aLengthList = aDtabItem.Blength.split()
        self.tableItem.setRowCount(len(aLengthList))

        for i in range (self.tableItem.rowCount):
            aTableItem = QTableWidgetItem(aLengthList[i])
            self.tableItem.setItem(i, 0, aTableItem)
        # for

    # diameterTableClicked

    def addLengthTable(self):
        if self.boltTable is None:
            return
        # if

        aInputDlg = InputDialog(QT_TRANSLATE_NOOP("Paragon", "Add Length Table"), self)
        if aInputDlg.exec() == QDialog.Rejected:
            return
        # if

        aTableName = aInputDlg.getName()
        if len(aTableName) < 1:
            return
        # if

        aMemberList = self.boltTable.Member
        if len(aMemberList) > 0:
            PipeCad.SetCurrentItem(aMemberList[-1])
        else:
            PipeCad.SetCurrentItem(self.boltTable)
        # if

        try:
            PipeCad.CreateItem("LTAB", aTableName)
        except Exception as e:
            return
        # try

        # Insert data to the table widget.
        aTableItem = QTableWidgetItem(aTableName)
        aTableItem.setData(Qt.UserRole, PipeCad.CurrentItem())

        aRow = self.tableLength.rowCount
        self.tableLength.insertRow(aRow)
        self.tableLength.setItem(aRow, 0, aTableItem)
        self.tableLength.setCurrentItem(aTableItem)

    # addLengthTable

    def delLengthTable(self):
        aTableItem = self.tableLength.currentItem()
        if aTableItem is None:
            return
        # if

        if QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Paragon", "Are you sure to delete the length table " + aTableItem.text())) != QMessageBox.Yes:
            return
        # if

        aLtabItem = aTableItem.data(Qt.UserRole)
        PipeCad.SetCurrentItem(aLtabItem)
        PipeCad.DeleteItem(aLtabItem.Type)

        self.resetBoltLength(self.boltTable)

    # delLengthTable

    def addDiameterTable(self):
        if self.tableLength.rowCount < 1:
            return
        # if

        aLtabItem = self.tableLength.currentItem().data(Qt.UserRole)
        if aLtabItem is None:
            return
        # if

        aInputDlg = InputDialog("Add Diameter Table", self)
        if aInputDlg.exec() == QDialog.Rejected:
            return
        # if

        aTableName = aInputDlg.getName()
        if len(aTableName) < 1:
            return
        # if

        aMemberList = aLtabItem.Member
        if len(aMemberList) > 0:
            PipeCad.SetCurrentItem(aMemberList[-1])
        else:
            PipeCad.SetCurrentItem(aLtabItem)
        # if

        try:
            PipeCad.CreateItem("DTAB", aTableName)
        except Exception as e:
            return
        # try

        # Insert data to the table widget.
        aTableItem = QTableWidgetItem(aTableName)
        aTableItem.setData(Qt.UserRole, PipeCad.CurrentItem())

        aRow = self.tableDiameter.rowCount
        self.tableDiameter.insertRow(aRow)
        self.tableDiameter.setItem(aRow, 0, aTableItem)
        self.tableDiameter.setCurrentItem(aTableItem)
    # addDiameterTable

    def delDiameterTable(self):
        aTableItem = self.tableDiameter.currentItem()
        if aTableItem is None:
            return
        # if

        if QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Paragon", "Are you sure to delete the diameter table " + aTableItem.text())) != QMessageBox.Yes:
            return
        # if

        aDtabItem = aTableItem.data(Qt.UserRole)
        PipeCad.SetCurrentItem(aDtabItem)
        PipeCad.DeleteItem(aDtabItem.Type)

        self.resetBoltLength(self.boltTable)
    # delDiameterTable

    def buildLength(self):
        if self.tableDiameter.rowCount < 1:
            return
        # if

        aDtabItem = self.tableDiameter.currentItem().data(Qt.UserRole)
        if aDtabItem is None:
            return
        # if

        aIs = int(self.textStart.text)
        aIi = int(self.textInterval.text)
        aIe = int(self.textEnd.text)

        if aIi == 0:
            return
        # if

        aRowCount = (aIe - aIs) / aIi + 1
        self.tableItem.setRowCount(aRowCount)

        aLengthList = []

        for i in range (self.tableItem.rowCount):
            aLength = str(aIs + aIi * i)
            aLengthList.append(aLength)
            aTableItem = QTableWidgetItem(aLength)
            self.tableItem.setItem(i, 0, aTableItem)
        # for

        aDtabItem.Blength = " ".join(aLengthList)
    # buildLength

    def deleteLengthItem(self):
        aRow = self.tableItem.currentRow()

        self.tableItem.removeRow(aRow)
    # deleteLengthItem

    def applyLengthItem(self):
        aTableItem = self.tableDiameter.currentItem()
        if aTableItem is None:
            return
        # if

        aDtabItem = aTableItem.data(Qt.UserRole)
        if aDtabItem is None:
            return
        # if

        aLengthList = []

        for i in range (self.tableItem.rowCount):
            aTableItem = self.tableItem.item(i, 0)
            aLengthList.append(aTableItem.text())
        # for

        aDtabItem.Blength = " ".join(aLengthList)
    # applyLengthItem

    def addBoltList(self):
        if self.boltTable is None:
            return
        # if

        aInputDlg = InputDialog(QT_TRANSLATE_NOOP("Paragon", "Add Bolt List"), self)
        if aInputDlg.exec() == QDialog.Rejected:
            return
        # if

        aBoltName = aInputDlg.getName()
        if len(aBoltName) < 1:
            return
        # if

        aMemberList = self.boltTable.Member
        if len(aMemberList) > 0:
            PipeCad.SetCurrentItem(aMemberList[-1])
        else:
            PipeCad.SetCurrentItem(self.boltTable)
        # if

        try:
            PipeCad.CreateItem("BLIS", aBoltName)
        except Exception as e:
            return
        # try

        # Insert data to the table widget.
        aTableItem = QTableWidgetItem(aBoltName)
        aTableItem.setData(Qt.UserRole, PipeCad.CurrentItem())

        aRow = self.tableBoltList.rowCount
        self.tableBoltList.insertRow(aRow)
        self.tableBoltList.setItem(aRow, 0, aTableItem)
        self.tableBoltList.setCurrentItem(aTableItem)

    # addBoltList

    def deleteBoltList(self):
        QMessageBox.question(self, "", "Are you sure to delete the selected bolt list?")
    # deleteBoltList

    def boltListClicked(self, theTableItem):
        aBlisItem = theTableItem.data(Qt.UserRole)
        if aBlisItem is None:
            self.tableBoltItem.setRowCount(0)
            return
        # if

        aMemberList = aBlisItem.Member
        self.tableBoltItem.setRowCount(len(aMemberList))
        for i in range (len(aMemberList)):
            aSbolItem = aMemberList[i]
            aTableItem = QTableWidgetItem(aSbolItem.Name)
            aTableItem.setData(Qt.UserRole, aSbolItem)

            self.tableBoltItem.setItem(i, 0, aTableItem)
            self.tableBoltItem.setItem(i, 1, QTableWidgetItem(aSbolItem.Bdiameter))
            self.tableBoltItem.setItem(i, 2, QTableWidgetItem(str(aSbolItem.Length)))
            self.tableBoltItem.setItem(i, 3, QTableWidgetItem(str(aSbolItem.Noff)))
            self.tableBoltItem.setItem(i, 4, QTableWidgetItem(str(aSbolItem.Xtralength)))

            aStdLength = aSbolItem.Stdblength
            if aStdLength is None:
                self.tableBoltItem.setItem(i, 5, QTableWidgetItem("unset"))
            else:
                self.tableBoltItem.setItem(i, 5, QTableWidgetItem(aStdLength.Name))
            # if
        # for

        if self.tableBoltItem.rowCount > 0:
            self.tableBoltItem.setCurrentCell(0, 0)
        # if

    # boltListClicked

    def addBolt(self):
        aTableItem = self.tableBoltList.currentItem()
        if aTableItem is None:
            return
        # if

        aBlisItem = aTableItem.data(Qt.UserRole)
        if aBlisItem is None:
            return
        # if

        aBoltDlg = BoltDialog(self.boltTable, aBlisItem, self)
        aBoltDlg.reset()
        if aBoltDlg.exec() == QDialog.Rejected:
            return
        # if

        # Update Bolt Element table.
        self.boltListClicked(aTableItem)

    # addBolt

    def modifyBolt(self):
        aTableItem = self.tableBoltList.currentItem()
        if aTableItem is None:
            return
        # if

        aBlisItem = aTableItem.data(Qt.UserRole)
        if aBlisItem is None:
            return
        # if

        aRow = self.tableBoltItem.currentRow()
        if aRow < 0:
            return
        # if

        aBoltItem = self.tableBoltItem.item(aRow, 0)
        if aBoltItem is None:
            return
        # if

        aSbolItem = aBoltItem.data(Qt.UserRole)
        if aSbolItem is None:
            return
        # if

        aBoltDlg = BoltDialog(self.boltTable, aBlisItem, self)
        aBoltDlg.reset(aSbolItem)
        if aBoltDlg.exec() == QDialog.Rejected:
            return
        # if

        # Update Bolt Element table.
        self.boltListClicked(aTableItem)
    # modifyBolt

    def deleteBolt(self):
        QMessageBox.information(self, "", "Delete Bolt")
    # deleteBolt
# ModifyDialog


# Singleton Instance.
aModifyDlg = ModifyDialog(PipeCad)

def Modify():
    aBltaItem = PipeCad.CurrentItem()
    if aBltaItem.Type != "BLTA":
        QMessageBox.warning(PipeCad, "", "Please Select BLTA to modify!")
        return
    # if

    aModifyDlg.reset()
    aModifyDlg.show()
# Modify
