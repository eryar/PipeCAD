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

class CreateDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.modifyItem = None
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(280, 100)
        self.setWindowTitle("Create")

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()

        self.comboName.addItem("Create")
        self.comboName.addItem("Modify")
        self.comboName.activated.connect(self.activateName)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelPurpose = QLabel("Purpose")
        self.comboPurpose = QComboBox()
        #self.comboPurpose.setEditable(True)
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

    def activateName(self):
        self.modifyItem = PipeCad.CurrentItem()

        if self.createMode == 1:
            self.setWindowTitle("Modify Catalogue")
        elif self.createMode == 2:
            self.setWindowTitle("Modify Section")
        else:
            self.setWindowTitle("Modify Category")
        # if

        self.textName.setText(self.modifyItem.Name)
        self.comboPurpose.setCurrentText(self.modifyItem.Purpose)
    # indexChanged

    def setCreateMode(self, theMode):
        self.textName.setText("")
        self.comboName.setCurrentIndex(0)

        if theMode == 1:
            self.setWindowTitle("Create Catalogue")
        elif theMode == 2:
            self.setWindowTitle("Create Section")
        else:
            self.setWindowTitle("Create Category")
        # if

        self.createMode = theMode
    # setMode

    def create(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        if self.createMode == 1:
            # create catalogue
            try:
                PipeCad.StartTransaction("Create Catalogue")
                PipeCad.CreateItem("CATA", aName)
                aCataItem = PipeCad.CurrentItem()
                aCataItem.Purpose = aPurpose
                PipeCad.CommitTransaction()
            except Exception as e:
                QMessageBox.critical(self, "", e)
                raise e
            # try
        elif self.createMode == 2:
            # create section
            aType = "SECT"
            if aPurpose == "STL":
                aType = "STSE"
            # if

            try:
                PipeCad.StartTransaction("Create Section")
                PipeCad.CreateItem(aType, aName)
                aCataItem = PipeCad.CurrentItem()
                aCataItem.Purpose = aPurpose
                PipeCad.CommitTransaction()
            except Exception as e:
                QMessageBox.critical(self, "", e)
                raise e
            # try
        else:
            # create category
            aType = "CATE"
            if aPurpose == "STL":
                aType = "STCA"
            # if
            try:
                PipeCad.StartTransaction("Create Category")
                PipeCad.CreateItem(aType, aName)
                aCataItem = PipeCad.CurrentItem()
                aCataItem.Purpose = aPurpose
                PipeCad.CommitTransaction()
            except Exception as e:
                QMessageBox.critical(self, "", e)
                raise e
            # try
        # if
    # create

    def modify(self):
        aName = self.textName.text
        aPurpose = self.comboPurpose.currentText

        if self.modifyItem is None:
            QMessageBox.warning(self, "", "Please select item to modify!")
            return
        # if

        try:
            PipeCad.StartTransaction("Modify")
            self.modifyItem.Name = aName
            self.modifyItem.Purpose = aPurpose
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.warning(self, "", e)
            raise e
        # try
    # modify

    def accept(self):
        aIndex = self.comboName.currentIndex

        if aIndex == 0:
            self.create()
        else:
            self.modify()
        # if

        QDialog.accept(self)
    # accept
# CreateDialog

# Singleton Instance.
aCreateDlg = CreateDialog(PipeCad)

def CreateCata():
    aCreateDlg.setCreateMode(1)
    aCreateDlg.show()
# CreateCata

def CreateSect():
    aCreateDlg.setCreateMode(2)
    aCreateDlg.show()
# CreateSect

def CreateCate():
    aCreateDlg.setCreateMode(3)
    aCreateDlg.show()
# CreateCate


class TextDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.modifyItem = None
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(380, 100)
        self.setWindowTitle("Text Definition")

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()

        self.comboName.addItem("Create")
        self.comboName.addItem("Modify")
        self.comboName.activated.connect(self.activateName)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Purpose
        self.labelText = QLabel("Text")
        self.textText = QLineEdit("")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelText)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textText)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def activateName(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            # create
            self.textName.setText("")
        else:
            # modify
            try:
                aTextItem = PipeCad.CurrentItem()
                if aTextItem.Type != "TEXT":
                    raise TypeError(aTextItem.Name + " is not TEXT!")
                # if

                self.textName.setText(aTextItem.Name)
                self.textText.setText(aTextItem.Stext)
                self.modifyItem = aTextItem
            except Exception as e:
                QMessageBox.critical(self, "", e)
            # try
        # if
    # activateName

    def create(self):
        try:
            PipeCad.StartTransaction("Create Text")
            PipeCad.CreateItem("TEXT", self.textName.text)
            aTextItem = PipeCad.CurrentItem()
            aTextItem.Stext = self.textText.text
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # create

    def modify(self):

        if self.modifyItem is None:
            QMessageBox.warning(self, "", "Please select item to modify!")
            return
        # if

        try:
            PipeCad.StartTransaction("Modify Text")
            self.modifyItem.Name = self.textName.text
            self.modifyItem.Stext = self.textText.text
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # modify

    def accept(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            # create
            self.create()
        else:
            # modify
            self.modify()
        # if

        self.textName.setText("")
        QDialog.accept(self)
    # accept
# TextDialog

# Singleton Instance.
aTextDlg = TextDialog(PipeCad)

def CreateText():
    aTextDlg.show()
# CreateText


class SmteDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.modifyItem = None
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(380, 100)
        self.setWindowTitle("Material Text Definition")

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.textName = QLineEdit()

        self.comboName.addItem("Create")
        self.comboName.addItem("Modify")
        self.comboName.activated.connect(self.activateName)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Material ISO.
        self.labelText1 = QLabel("Material(ISO)")
        self.textText1 = QLineEdit("")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelText1)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textText1)

        # Text A.
        self.labelText2 = QLabel("Text Y")
        self.textText2 = QLineEdit("")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelText2)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textText2)

        # Text B.
        self.labelText3 = QLabel("Text Z")
        self.textText3 = QLineEdit("")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelText3)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textText3)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def activateName(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            # create
            self.textName.setText("")
            self.textText1.setText("")
            self.textText2.setText("")
            self.textText3.setText("")
        else:
            # modify
            try:
                aTextItem = PipeCad.CurrentItem()
                if aTextItem.Type != "SMTE":
                    raise TypeError(aTextItem.Name + " is not SMTE!")
                # if

                self.textName.setText(aTextItem.Name)
                self.textText1.setText(aTextItem.Xtext)
                self.textText2.setText(aTextItem.Ytext)
                self.textText3.setText(aTextItem.Ztext)
                self.modifyItem = aTextItem
            except Exception as e:
                QMessageBox.critical(self, "", e)
            # try
        # if
    # activateName

    def create(self):
        try:
            PipeCad.StartTransaction("Create Material Text")
            PipeCad.CreateItem("SMTE", self.textName.text)
            aTextItem = PipeCad.CurrentItem()
            aTextItem.Xtext = self.textText1.text
            aTextItem.Ytext = self.textText2.text
            aTextItem.Ztext = self.textText3.text
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # create

    def modify(self):

        if self.modifyItem is None:
            QMessageBox.warning(self, "", "Please select item to modify!")
            return
        # if

        try:
            PipeCad.StartTransaction("Modify Material Text")
            self.modifyItem.Name = self.textName.text
            self.modifyItem.Xtext = self.textText1.text
            self.modifyItem.Ytext = self.textText2.text
            self.modifyItem.Ztext = self.textText3.text
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # modify

    def accept(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            # create
            self.create()
        else:
            # modify
            self.modify()
        # if

        self.textName.setText("")
        self.textText1.setText("")
        self.textText2.setText("")
        self.textText3.setText("")

        QDialog.accept(self)
    # accept
# SmteDialog

# Singleton Instance.
aSmteDlg = SmteDialog(PipeCad)

def CreateSmte():
    aSmteDlg.show()
# CreateSmte
