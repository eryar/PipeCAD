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
# Copyright (C) 2022 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 11:20 2022-04-21

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *

class EquipmentDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(300, 360)
        self.setWindowTitle(self.tr("Equipment Creation"))

        self.verticalLayout = QVBoxLayout(self)

        # Name
        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(180)

        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Position
        self.groupBox = QGroupBox(self.tr("Position"))
        self.formLayout = QFormLayout(self.groupBox)

        self.labelPx = QLabel(self.tr("East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(self.tr("North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(self.tr("Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addWidget(self.groupBox)

        # Attributes
        self.groupBox = QGroupBox(self.tr("Attributes"))

        self.formLayout = QFormLayout(self.groupBox)

        self.labelDescription = QLabel(self.tr("Description"))
        self.textDescription = QLineEdit("")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textDescription)

        self.labelFunction = QLabel(self.tr("Function"))
        self.textFunction = QLineEdit("")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelFunction)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textFunction)

        self.labelPurpose = QLabel(self.tr("Purpose"))
        self.textPurpose = QLineEdit("")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPurpose)

        self.verticalLayout.addWidget(self.groupBox)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.retranslateUi()
    # setupUi

    def retranslateUi(self):
        pass
    # retranslateUi

    def accept(self):
        aName = self.textName.text
        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        PipeCad.StartTransaction("Create Equipment")
        PipeCad.CreateItem("EQUI", aName)

        aEquipment = PipeCad.CurrentItem()
        aEquipment.Position = Position(aPx, aPy, aPz)
        aEquipment.Description = self.textDescription.text
        aEquipment.Function = self.textFunction.text
        aEquipment.Purpose = self.textPurpose.text

        PipeCad.CommitTransaction()       

        QDialog.accept(self)
    # accept
# EquipmentDialog

# Singleton Instance.
aEquipmentDlg = EquipmentDialog(PipeCad)

def Create():
    aEquipmentDlg.textName.setText("")
    aEquipmentDlg.show()
# Create


class SubEquipmentDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(300, 360)
        self.setWindowTitle(self.tr("Sub-Equipment Creation"))

        self.verticalLayout = QVBoxLayout(self)

        # Name
        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(220)

        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Position
        self.groupBox = QGroupBox(self.tr("Position"))
        self.formLayout = QFormLayout(self.groupBox)

        self.labelPx = QLabel(self.tr("East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(self.tr("North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(self.tr("Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addWidget(self.groupBox)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.retranslateUi()
    # setupUi

    def retranslateUi(self):
        pass
    # retranslateUi

    def accept(self):
        aName = self.textName.text
        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        PipeCad.StartTransaction("Create Sub-Equipment")
        PipeCad.CreateItem("SUBE", aName)

        aEquipment = PipeCad.CurrentItem()
        aEquipment.Position = Position(aPx, aPy, aPz)

        PipeCad.CommitTransaction()       

        QDialog.accept(self)
    # accept
# EquipmentDialog

# Singleton Instance.
aSubEquipmentDlg = SubEquipmentDialog(PipeCad)

def CreateSub():
    aSubEquipmentDlg.textName.setText("")
    aSubEquipmentDlg.show()
# CreateSub
