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

class RegularDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Regular Structure"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupColumn = QGroupBox()
        self.groupColumn.setTitle("Column Data")

        self.formLayout = QFormLayout(self.groupColumn)

        self.labelColumnArea = QLabel("Storage Area")
        self.textColumnArea = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelColumnArea)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textColumnArea)

        self.buttonColumn = QPushButton("Profile...")
        self.textColumn = QLineEdit()
        
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

        self.labelBeamArea = QLabel("Storage Area")
        self.textBeamArea = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelBeamArea)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textBeamArea)

        self.buttonBeam = QPushButton("Profile...")
        self.textBeam = QLineEdit()
        
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
        self.buttonPreview.setText(u"Preview")
        self.buttonPreview.setDefault(True)
        self.buttonPreview.clicked.connect(self.preview)

        self.horizontalLayout.addWidget(self.buttonPreview)

        self.buttonBuild = QPushButton()
        self.buttonBuild.setText(u"Build")
        self.buttonBuild.clicked.connect(self.build)

        self.horizontalLayout.addWidget(self.buttonBuild)

        self.buttonCancel = QPushButton()
        self.buttonCancel.setText(u"Cancel")
        self.buttonCancel.clicked.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.resize(390, 580)
    # setupUi

    def preview(self):
    
        PipeCad.ClearAid()
        
        aLx = []
        aLy = []
        aLz = []
        
        # East Spacings
        aSpacings = self.textEast.plainText.split("\n")
        for x in aSpacings:
            aLx.append(float(x))
        
        # North Spacings
        aSpacings = self.textNorth.plainText.split("\n")
        for y in aSpacings:
            aLy.append(float(y))
        
        # Elevation
        aSpacings = self.textElev.plainText.split("\n")
        for z in aSpacings:
            aLz.append(float(z))
        
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
                    PipeCad.AddAidLine(aPs, aPe, 1)

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
                    PipeCad.AddAidLine(aPs, aPe, 1)

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
                    PipeCad.AddAidLine(aPs, aPe, 1)
        
        PipeCad.UpdateViewer()
    # preview
        
    def build(self):
        aColumnArea = PipeCad.GetItem(self.textColumnArea.text)
        if aColumnArea is None:
            QMessageBox.warning(self, "", "Please enter Column Storage Area!")
            return

        aBeamArea = PipeCad.GetItem(self.textBeamArea.text)
        if aBeamArea is None:
            QMessageBox.warning(self, "", "Please enter Beam Storage Area!")
            return

        aColumnSpec = PipeCad.GetItem(self.textColumn.text)
        if aColumnSpec is None:
            QMessageBox.warning(self, "", "Please enter Column Profile Spec!")
            return

        aBeamSpec = PipeCad.GetItem(self.textBeam.text)
        if aBeamSpec is None:
            QMessageBox.warning(self, "", "Please enter Beam Profile Spec!")
            return

        aLx = []
        aLy = []
        aLz = []
        
        # East Spacings
        aSpacings = self.textEast.plainText.split("\n")
        for x in aSpacings:
            aLx.append(float(x))
        
        # North Spacings
        aSpacings = self.textNorth.plainText.split("\n")
        for y in aSpacings:
            aLy.append(float(y))
        
        # Elevation
        aSpacings = self.textElev.plainText.split("\n")
        for z in aSpacings:
            aLz.append(float(z))

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
                        aSctnItem.startPosition = aPs
                        aSctnItem.endPosition = aPe
                        aSctnItem.spref = aBeamSpec

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
                        aSctnItem.startPosition = aPs
                        aSctnItem.endPosition = aPe
                        aSctnItem.spref = aColumnSpec

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
                        aSctnItem.startPosition = aPs
                        aSctnItem.endPosition = aPe
                        aSctnItem.spref = aColumnSpec

        PipeCad.CommitTransaction()
    # build

    def reject(self):
        PipeCad.ClearAid()
        QDialog.reject(self)
    # reject

# Singleton Instance.
aStruDialog = RegularDialog(PipeCad)

def CreateRegular():
    aStruDialog.show()
# Create
