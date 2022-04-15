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
from PythonQt.PipeCAD import *

from PipeCAD import *


class SiteDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle(self.tr("Create Site"))

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
        self.setWindowTitle(self.tr("Create Zone"))

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

def Search():
    QMessageBox.warning(PipeCad, "", "Not implement yet!")
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
