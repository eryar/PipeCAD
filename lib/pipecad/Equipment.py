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
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Equipment Creation"))

        self.verticalLayout = QVBoxLayout(self)

        # Name
        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Design", "Name"))
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(180)

        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Position
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Design", "Position"))
        self.formLayout = QFormLayout(self.groupBox)

        self.labelPx = QLabel(QT_TRANSLATE_NOOP("Design", "East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(QT_TRANSLATE_NOOP("Design", "North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(QT_TRANSLATE_NOOP("Design", "Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addWidget(self.groupBox)

        # Attributes
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Design", "Attributes"))

        self.formLayout = QFormLayout(self.groupBox)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Design", "Description"))
        self.textDescription = QLineEdit("")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textDescription)

        self.labelFunction = QLabel(QT_TRANSLATE_NOOP("Design", "Function"))
        self.textFunction = QLineEdit("")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelFunction)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textFunction)

        self.labelPurpose = QLabel(QT_TRANSLATE_NOOP("Design", "Purpose"))
        self.textPurpose = QLineEdit("")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPurpose)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPurpose)

        self.verticalLayout.addWidget(self.groupBox)

        # Action buttons.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self)
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
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Sub-Equipment Creation"))

        self.verticalLayout = QVBoxLayout(self)

        # Name
        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Design", "Name"))
        self.textName = QLineEdit()
        self.textName.setMinimumWidth(220)

        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Position
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Design", "Position"))
        self.formLayout = QFormLayout(self.groupBox)

        self.labelPx = QLabel(QT_TRANSLATE_NOOP("Design", "East"))
        self.textPx = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.labelPy = QLabel(QT_TRANSLATE_NOOP("Design", "North"))
        self.textPy = QLineEdit("0.0")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.labelPz = QLabel(QT_TRANSLATE_NOOP("Design", "Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addWidget(self.groupBox)

        # Action buttons.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self)
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


class OriginDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.equiItem = None
        self.aidNumber = PipeCad.NextAidNumber()

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Modify Equipment Origin"))

        self.verticalLayout = QVBoxLayout(self)

        # CE
        self.formLayout = QFormLayout()

        self.buttonCE = QPushButton("CE")
        self.buttonCE.clicked.connect(self.setEquipment)

        self.labelCE = QLabel()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.buttonCE)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.labelCE)

        self.verticalLayout.addLayout(self.formLayout)

        # Position
        self.labelPosition = QLabel(QT_TRANSLATE_NOOP("Design", "Change Origin Wrt /*"))
        self.verticalLayout.addWidget(self.labelPosition)

        self.formLayout = QFormLayout()
        self.labelPx = QLabel(QT_TRANSLATE_NOOP("Design", "East"))
        self.textPx = QLineEdit("0.0")

        self.labelPy = QLabel(QT_TRANSLATE_NOOP("Design", "North"))
        self.textPy = QLineEdit("0.0")

        self.labelPz = QLabel(QT_TRANSLATE_NOOP("Design", "Up"))
        self.textPz = QLineEdit("0.0")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textPx)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPy)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPz)

        self.verticalLayout.addLayout(self.formLayout)

        # Action buttons.
        self.horizontalLayout = QHBoxLayout()

        self.buttonPick = QPushButton(QT_TRANSLATE_NOOP("Design", "Pick"))
        self.buttonPick.clicked.connect(self.pickVertex)
        self.horizontalLayout.addWidget(self.buttonPick)

        self.buttonPreview = QPushButton(QT_TRANSLATE_NOOP("Design", "Preview"))
        self.buttonPreview.clicked.connect(self.preview)
        self.horizontalLayout.addWidget(self.buttonPreview)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def setEquipment(self):
        self.equiItem = None
        self.labelCE.setText("")
        PipeCad.RemoveAid(self.aidNumber)

        aTreeItem = PipeCad.CurrentItem()
        if aTreeItem.Type != "EQUI":
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Design", "Please select EQUI to modify origin!"))
            return
        # if

        self.equiItem = aTreeItem

        aName = aTreeItem.Name
        if len(aName) < 1:
            aName = aTreeItem.RefNo
        # if

        self.labelCE.setText(aName)

        aPosition = aTreeItem.Position.Wrt()
        self.textPx.setText(str(aPosition.X))
        self.textPy.setText(str(aPosition.Y))
        self.textPz.setText(str(aPosition.Z))

        PipeCad.AddAidAxis(aPosition, aTreeItem.Orientation, self.aidNumber)
        PipeCad.UpdateViewer()
    # setEquipment

    def pickVertex(self):
        aPoint = PipeCad.PickPoint()
        if aPoint is None:
            return
        # if

        self.textPx.setText(str(aPoint.X))
        self.textPy.setText(str(aPoint.Y))
        self.textPz.setText(str(aPoint.Z))
    # pickVertex

    def preview(self):
        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        aPosition = Position(aPx, aPy, aPz)

        PipeCad.RemoveAid(self.aidNumber)
        PipeCad.AddAidAxis(aPosition, self.equiItem.Orientation, self.aidNumber)
        PipeCad.UpdateViewer()
    # preview

    def accept(self):
        if self.equiItem is None:
            return
        # if

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        aTargetPosition = Position(aPx, aPy, aPz)
        aEquipmentPosition = self.equiItem.Position

        aOffset = aTargetPosition.Distance(aEquipmentPosition)
        if aOffset < 0.1:
            return
        # if

        aDir = Direction(aTargetPosition, aEquipmentPosition)

        PipeCad.StartTransaction("Modify Equipment Origin")

        # Move equipment primitives member.
        for aTreeItem in self.equiItem.Member:
            PipeCad.Translate(aTreeItem, aDir, aOffset)
        # for

        # Move equipment.
        PipeCad.Translate(self.equiItem, aDir, -aOffset)

        PipeCad.CommitTransaction()

        PipeCad.RemoveAid(self.aidNumber)
        PipeCad.UpdateViewer()

        QDialog.accept(self)
    # accept

    def reject(self):
        PipeCad.RemoveAid(self.aidNumber)
        PipeCad.UpdateViewer()
        QDialog.reject(self)
    # reject

# OriginDialog

# Singleton Instance.
aOriginDlg = OriginDialog(PipeCad)

def ModifyOrigin():
    aTreeItem = PipeCad.CurrentItem()
    if aTreeItem.Type == "EQUI":
        aOriginDlg.setEquipment()
    else:
        QMessageBox.warning(PipeCad, "", QT_TRANSLATE_NOOP("Design", "Please select EQUI to modify origin!"))
        return
    # if

    aOriginDlg.show()
# ModifyOrigin
