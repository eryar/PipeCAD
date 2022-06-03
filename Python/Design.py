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
# Date: 11:20 2021-12-23

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class SiteDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Site"))

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
            PipeCad.StartTransaction("Create SITE")
            PipeCad.CreateItem("SITE", aName)
            aSpwlItem = PipeCad.CurrentItem()
            aSpwlItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# SiteDialog

# Singleton Instance.
aSiteDlg = SiteDialog(PipeCad)

def CreateSite():
    aSiteDlg.show()
# CreateSite

class ZoneDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Create Zone"))

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
            PipeCad.StartTransaction("Create ZONE")
            PipeCad.CreateItem("ZONE", aName)
            aSpwlItem = PipeCad.CurrentItem()
            aSpwlItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try

        QDialog.accept(self)
    # accept
# ZoneDialog

# Singleton Instance.
aZoneDlg = ZoneDialog(PipeCad)

def CreateZone():
    aZoneDlg.show()
# CreateZone


class SearchDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.ownerItem = None

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Search"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Design", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Type
        self.labelType = QLabel(QT_TRANSLATE_NOOP("Design", "Type"))
        self.textType = QLineEdit()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelType)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textType)

        # Search beneath item.
        self.labelOwner = QLabel(QT_TRANSLATE_NOOP("Design", "Owner"))
        self.buttonOwner = QPushButton(QT_TRANSLATE_NOOP("Design", "CE"))
        self.buttonOwner.clicked.connect(self.setOwner)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelOwner)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.buttonOwner)

        self.verticalLayout.addLayout(self.formLayout)

        # Result table.
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.setHorizontalHeaderLabels(["Type", "Name"])

        self.tableWidget.cellDoubleClicked.connect(self.locateItem)

        self.verticalLayout.addWidget(self.tableWidget)

        # Action buttons.
        self.horizontalLayout = QHBoxLayout()

        self.buttonSearch = QPushButton(QT_TRANSLATE_NOOP("Design", "Search"))
        self.buttonSearch.setDefault(True)
        self.buttonSearch.clicked.connect(self.search)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonSearch)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

    # setupUi

    def setOwner(self):
        self.ownerItem = PipeCad.CurrentItem()
        if len(self.ownerItem.Name) < 1:
            self.buttonOwner.setText("CE: " + self.ownerItem.RefNo)
        else:
            self.buttonOwner.setText("CE: " + self.ownerItem.Name)
        # if
    # setOwner

    def search(self):
        aName = self.textName.text
        aType = self.textType.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please input key word in item name!"))
            return
        # if

        aItemList = PipeCad.SearchItem(aName, aType, self.ownerItem)
        self.tableWidget.setRowCount(len(aItemList))

        for r in range(self.tableWidget.rowCount):
            aTreeItem = aItemList[r]

            self.tableWidget.setItem(r, 0, QTableWidgetItem(aTreeItem.Type))

            if len(aTreeItem.Name) > 0:
                self.tableWidget.setItem(r, 1, QTableWidgetItem(aTreeItem.Name))
            else:
                self.tableWidget.setItem(r, 1, QTableWidgetItem(aTreeItem.RefNo))
            # if

            self.tableWidget.item(r, 0).setData(Qt.UserRole, aTreeItem)
        # for

    # search

    def locateItem(self, theRow):
        if theRow < 0:
            return
        # if

        aTreeItem = self.tableWidget.item(theRow, 0).data(Qt.UserRole)
        if aTreeItem is None:
            return
        # if

        PipeCad.SetCurrentItem(aTreeItem)
        PipeCad.LookAt(aTreeItem)
        
    # locateItem

    def accept(self):
        aRow = self.tableWidget.currentRow()

        self.locateItem(aRow)

    # accept
# SearchDialog

# Singleton Instance.
aSearchDlg = SearchDialog(PipeCad)

def Search():
    aSearchDlg.show()
# Search


class TextDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(280, 180)
        self.setWindowTitle(self.tr("Create 3D Text"))

        self.verticalLayout = QVBoxLayout(self)

        # Form layout.
        self.formLayout = QFormLayout()
        self.verticalLayout.addLayout(self.formLayout)

        # Text.
        self.labelText = QLabel("Text")
        self.textText = QLineEdit("Hello PipeCAD!")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelText)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textText)

        # Size
        self.labelSize = QLabel("Size")
        self.textSize = QLineEdit("80")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelSize)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textSize)

        # Font.
        self.labelFont = QLabel("Font")
        self.comboFont = QFontComboBox()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelFont)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboFont)

        # Dialog Button.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aText = self.textText.text
        aSize = self.textSize.text
        aFont = self.comboFont.currentFont.family()

        if len(aText) < 1:
            QMessageBox.warning(PipeCad, "", self.tr("Please input text!"))
        # if

        aTreeItem = PipeCad.CurrentItem()
        if aTreeItem.Type == "ZONE" or aTreeItem.Owner.Type == "ZONE":
            pass
        else:
            QMessageBox.warning(self, "", self.tr("Please create 3d text in ZONE!"))
            return
        # if

        PipeCad.CreateText(aText, aFont, float(aSize))

        QDialog.accept(self)
    # accept

# TextDialog

# Singleton Instance.
aTextDlg = TextDialog(PipeCad)

def CreateText():
    aTextDlg.show()
# CreateText


def ShowFlow():
    # Show pipe flow aid arrow on PIPE/BRANCH.
    aTreeItem = PipeCad.CurrentItem()

    if aTreeItem.Type not in {"PIPE", "BRAN"}:
        QMessageBox.critical(PipeCad, "", QT_TRANSLATE_NOOP("Design", "Please select PIPE/BRAN to display flow arrow!"))
        return
    # if

    aAidNumber = PipeCad.NextAidNumber()

    aBranches = list()
    if aTreeItem.Type == "BRAN":
        aBranches.append(aTreeItem)
    else:
        aBranches = PipeCad.CollectItem("BRAN", aTreeItem)
    # if

    for aBranItem in aBranches:
        aPos = aBranItem.Hposition
        aDir = aBranItem.Hdirection
        aLength = float(aBranItem.Hbore) * 1.5

        # Show aid arrow at branch head.
        PipeCad.AddAidArrow(aPos, aDir, aLength, 2, 0.4, aAidNumber)

        aPos = aBranItem.Tposition
        aDir = aBranItem.Tdirection.Reversed()
        aLength = float(aBranItem.Tbore) * 1.5

        # Show aid arrow at branch tail.
        PipeCad.AddAidArrow(aPos, aDir, aLength, 2, 0.4, aAidNumber)

        for aCompItem in aBranItem.Member:
            if aCompItem.Type != "ELBO":
                continue
            # if

            aArrivePoint = aCompItem.ArrivePoint
            if aArrivePoint is not None:
                aPos = aArrivePoint.Position
                aDir = aArrivePoint.Direction.Reversed()
                aLength = float(aArrivePoint.Bore) * 1.5

                # Show aid arrow at elbow point.
                PipeCad.AddAidArrow(aPos, aDir, aLength, 2, 0.4, aAidNumber)
            # if

            aLeavePoint = aCompItem.LeavePoint
            if aLeavePoint is not None:
                aPos = aLeavePoint.Position
                aDir = aLeavePoint.Direction
                aLength = float(aLeavePoint.Bore) * 1.5

                # Show aid arrow at elbow point.
                PipeCad.AddAidArrow(aPos, aDir, aLength, 2, 0.4, aAidNumber)
            # if
        # for

    # for

    PipeCad.UpdateViewer()

# ShowFlow
