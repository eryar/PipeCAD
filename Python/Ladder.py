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
# Date: 21:02 2021-11-29

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class StepDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Ladder", "Step Ladder"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        # Name
        self.comboName = QComboBox()
        self.comboName.addItem(QT_TRANSLATE_NOOP("Ladder", "Create"))
        self.comboName.addItem(QT_TRANSLATE_NOOP("Ladder", "Modify"))

        self.textName = QLineEdit("STEP-LADD-001")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        # Height
        self.labelHeight = QLabel(QT_TRANSLATE_NOOP("Ladder", "Height"))
        self.textHeight = QLineEdit("1800")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textHeight)

        # Width
        self.labelWidth = QLabel(QT_TRANSLATE_NOOP("Ladder", "Width"))
        self.textWidth = QLineEdit("500")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelWidth)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textWidth)

        self.verticalLayout.addLayout(self.formLayout)

        self.tabWidget = QTabWidget()

        # Tab 1
        self.tabStep1 = QWidget()
        self.verticalLayout1 = QVBoxLayout(self.tabStep1)
        self.formLayout1 = QFormLayout()

        # Position and direction.
        self.labelX1 = QLabel(QT_TRANSLATE_NOOP("Ladder", "East"))
        self.textX1 = QLineEdit("0.0")

        self.formLayout1.setWidget(0, QFormLayout.LabelRole, self.labelX1)
        self.formLayout1.setWidget(0, QFormLayout.FieldRole, self.textX1)

        self.labelY1 = QLabel(QT_TRANSLATE_NOOP("Ladder", "North"))
        self.textY1 = QLineEdit("0.0")

        self.formLayout1.setWidget(1, QFormLayout.LabelRole, self.labelY1)
        self.formLayout1.setWidget(1, QFormLayout.FieldRole, self.textY1)

        self.labelZ1 = QLabel(QT_TRANSLATE_NOOP("Ladder", "Up"))
        self.textZ1 = QLineEdit("0.0")

        self.formLayout1.setWidget(2, QFormLayout.LabelRole, self.labelZ1)
        self.formLayout1.setWidget(2, QFormLayout.FieldRole, self.textZ1)

        self.labelDir1 = QLabel(QT_TRANSLATE_NOOP("Ladder", "Direction"))
        self.textDir1 = QLineEdit("N")

        self.formLayout1.setWidget(3, QFormLayout.LabelRole, self.labelDir1)
        self.formLayout1.setWidget(3, QFormLayout.FieldRole, self.textDir1)

        # Anchor Type
        self.labelType = QLabel(QT_TRANSLATE_NOOP("Ladder", "Type"))
        self.comboType = QComboBox()
        self.comboType.addItem(QT_TRANSLATE_NOOP("Ladder", "a"), 1)
        self.comboType.addItem(QT_TRANSLATE_NOOP("Ladder", "b"), 2)

        self.formLayout1.setWidget(4, QFormLayout.LabelRole, self.labelType)
        self.formLayout1.setWidget(4, QFormLayout.FieldRole, self.comboType)

        # Clearance
        self.labelClearance = QLabel(QT_TRANSLATE_NOOP("Ladder", "Clearance"))
        self.textClearance = QLineEdit("300")

        self.formLayout1.setWidget(5, QFormLayout.LabelRole, self.labelClearance)
        self.formLayout1.setWidget(5, QFormLayout.FieldRole, self.textClearance)

        self.horizontalLayout = QHBoxLayout()
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumWidth(360)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/step_ladder1.png"))
        self.horizontalLayout.addLayout(self.formLayout1)
        self.horizontalLayout.addWidget(self.labelDiagram)

        self.verticalLayout1.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tabStep1, QT_TRANSLATE_NOOP("Ladder", "Step"))

        # Tab 2
        self.tabStep2 = QWidget()
        self.verticalLayout2 = QVBoxLayout(self.tabStep2)
        self.formLayout2 = QFormLayout()

        # Position and direction.
        self.labelX2 = QLabel(QT_TRANSLATE_NOOP("Ladder", "East"))
        self.textX2 = QLineEdit("0.0")

        self.formLayout2.setWidget(0, QFormLayout.LabelRole, self.labelX2)
        self.formLayout2.setWidget(0, QFormLayout.FieldRole, self.textX2)

        self.labelY2 = QLabel(QT_TRANSLATE_NOOP("Ladder", "North"))
        self.textY2 = QLineEdit("0.0")

        self.formLayout2.setWidget(1, QFormLayout.LabelRole, self.labelY2)
        self.formLayout2.setWidget(1, QFormLayout.FieldRole, self.textY2)

        self.labelZ2 = QLabel(QT_TRANSLATE_NOOP("Ladder", "Up"))
        self.textZ2 = QLineEdit("0.0")

        self.formLayout2.setWidget(2, QFormLayout.LabelRole, self.labelZ2)
        self.formLayout2.setWidget(2, QFormLayout.FieldRole, self.textZ2)

        self.labelDir2 = QLabel(QT_TRANSLATE_NOOP("Ladder", "Direction"))
        self.textDir2 = QLineEdit("N")

        self.formLayout2.setWidget(3, QFormLayout.LabelRole, self.labelDir2)
        self.formLayout2.setWidget(3, QFormLayout.FieldRole, self.textDir2)

        self.horizontalLayout = QHBoxLayout()
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumWidth(360)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/step_ladder2.png"))
        self.horizontalLayout.addLayout(self.formLayout2)
        self.horizontalLayout.addWidget(self.labelDiagram)

        self.verticalLayout2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tabStep2, QT_TRANSLATE_NOOP("Ladder", "Step with Handrail"))

        self.verticalLayout.addWidget(self.tabWidget)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def buildStep1(self):
        aHeight = float(self.textHeight.text)
        aWidth = float(self.textWidth.text)
        aClearance = float(self.textClearance.text)
        aAnchorType = self.comboType.currentData

        PipeCad.StartTransaction("Create Step Ladder")

        PipeCad.CreateItem("LADD", self.textName.text)
        aLaddItem = PipeCad.CurrentItem()
        aLaddItem.Category = 6
        aLaddItem.Height = aHeight
        aLaddItem.Width = aWidth
        aLaddItem.Clearance = aClearance
        aLaddItem.Anchor = aAnchorType

        PipeCad.CommitTransaction()
    # buildStep1

    def buildStep2(self):
        aHeight = float(self.textHeight.text)
        aWidth = float(self.textWidth.text)

        PipeCad.StartTransaction("Create Step Ladder")

        PipeCad.CreateItem("LADD", self.textName.text)
        aLaddItem = PipeCad.CurrentItem()
        aLaddItem.Category = 7
        aLaddItem.Height = aHeight
        aLaddItem.Width = aWidth

        PipeCad.CommitTransaction()
    # buildStep2

    def accept(self):
        aIndex = self.tabWidget.currentIndex
        if aIndex == 0:
            # Step ladder
            self.buildStep1()
        else:
            # Step with angle
            self.buildStep2()
        # if

        QDialog.accept(self)
    # accept

# StepDialog

# Singleton Instance.
aStepDlg = StepDialog(PipeCad)

def CreateStep():
    aStepDlg.show()
# CreateStep

def CreateOnEquipment():
    print("ladder on equipment")
# CreateOnEquipment

def CreateOnPlatform():
    print("ladder on platform")
# CreateOnPlatform


class LadderDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(640, 480)
        self.setWindowTitle(self.tr("Create Ladder"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit("Ladder001")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)
        self.verticalLayout.addLayout(self.formLayout)

        self.tabWidget = QTabWidget()

        # Tab1
        self.tabLadder1 = QWidget()
        self.verticalLayout1 = QVBoxLayout(self.tabLadder1)

        self.formLayout = QFormLayout()
        self.labelHeight1 = QLabel("Height")
        self.textHeight1 = QLineEdit("1800")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelHeight1)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textHeight1)

        self.labelAngle1 = QLabel("Angle")
        self.comboAngle1 = QComboBox()
        self.comboAngle1.addItems(["65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75"])
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelAngle1)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboAngle1)

        self.horizontalLayout = QHBoxLayout()
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumWidth(360)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/ladder1.png"))
        self.horizontalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addWidget(self.labelDiagram)

        self.verticalLayout1.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tabLadder1, "Step Ladder")

        # Tab2
        self.tabLadder2 = QWidget()
        self.verticalLayout2 = QVBoxLayout(self.tabLadder2)

        self.formLayout = QFormLayout()
        self.labelHeight2 = QLabel("Height")
        self.textHeight2 = QLineEdit("2800")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelHeight2)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textHeight2)

        self.labelClearance2 = QLabel("Clearance")
        self.textClearance2 = QLineEdit("200")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelClearance2)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textClearance2)

        self.horizontalLayout = QHBoxLayout()
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumWidth(360)
        self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/ladder2.png"))
        self.horizontalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addWidget(self.labelDiagram)

        self.verticalLayout2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tabLadder2, "Front Exit Ladder")

        # Tab3 
        self.tabLadder3 = QWidget()
        self.tabWidget.addTab(self.tabLadder3, "Side Exit Ladder")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

    # setupUi

    def retranslateUi(self):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLadder1), "Ladder1")
    # retranslateUi

    def accept(self):
        aIndex = self.tabWidget.currentIndex
        if aIndex == 0:
            # Ladder1 
            self.buildLadder1()
        elif aIndex == 1:
            # Ladder 2
            self.buildLadder2()
        elif aIndex == 2:
            # Ladder 3
            self.buildLadder3()

        QDialog.accept(self)
    # accept

    def buildLadder1(self):
        aType = self.comboType1.currentIndex
        aSupp = self.comboSupport1.currentIndex
        aName = self.textName1.text
        aHeight = float(self.textHeight1.text)
        aClearance = float(self.textClearance1.text)

        aStep = int((aHeight - 100) / 300.0)

        PipeCad.StartTransaction("Build Ladder")
        PipeCad.CreateItem("STRU", aName)
        aStruItem = PipeCad.CurrentItem()
        aStruItem.description = self.comboType1.currentText + ", H=" + self.textHeight1.text

        PipeCad.CreateItem("SUBS")
        aSubsItem = PipeCad.CurrentItem()
        for i in range(aStep + 1):
            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 467
            aCyliItem.Diameter = 25
            aCyliItem.Height = 500
            aCyliItem.Position = Position(0, 0, aHeight - 50 - i * 300)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0)

        if aType == 0:
            # a
            aLength = 300 * aStep + 100

            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = aLength
            aBoxItem.Position = Position(-244, 0, aHeight * 0.5)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = aLength
            aBoxItem.Position = Position(244, 0, aHeight * 0.5)
        else:
            # b
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = aHeight
            aBoxItem.Position = Position(-244, 0, aHeight * 0.5)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 60
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(-280, 0, 5)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = aHeight
            aBoxItem.Position = Position(244, 0, aHeight * 0.5)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 60
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(280, 0, 5)

        if aSupp == 0:
            # F.T
            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            #aBoxItem.Xlength = 60
            #aBoxItem.Ylength = 70
            #aBoxItem.Zlength = 10
            #aBoxItem.Position = Position(280, 0, 5)
        else:
            # S.T
            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = aClearance + 35
            aBoxItem.Zlength = 80
            aBoxItem.Position = Position(256, aBoxItem.Ylength * 0.5 - 35, aHeight - 150)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = aClearance + 35
            aBoxItem.Zlength = 80
            aBoxItem.Position = Position(-256, aBoxItem.Ylength * 0.5 - 35, aHeight - 150)

            aH = aHeight - aStep * 300 + 150

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = aClearance + 35
            aBoxItem.Zlength = 80
            aBoxItem.Position = Position(256, aBoxItem.Ylength * 0.5 - 35, aH)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 467
            aBoxItem.Xlength = 12
            aBoxItem.Ylength = aClearance + 35
            aBoxItem.Zlength = 80
            aBoxItem.Position = Position(-256, aBoxItem.Ylength * 0.5 - 35, aH)

        PipeCad.CommitTransaction()
    # buildLadder1

    def buildLadder2(self):
        aName = self.textName.text
        aHeight = float(self.textHeight2.text)
        aClearance = float(self.textClearance2.text)

        if aHeight <= 500:
            return
        elif aHeight <= 2300:
            # Ladder Short.
            PipeCad.StartTransaction("Build Ladder")

            PipeCad.CreateItem("STRU", aName)
            aStruItem = PipeCad.CurrentItem()

            # 65X10 Stringers.
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(230, 0, 0, aStruItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 10
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = aHeight + 90
            aBoxItem.Position = Position(0, 0, aBoxItem.Zlength * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 65
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(32.5, 0, 5, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 45
            aRtorItem.InsideRadius = 10
            aRtorItem.OutsideRadius = 20
            aRtorItem.Position = Position(15, 0, (aHeight + 90), aSubsItem)
            aRtorItem.Orientation = Orientation(-90, -45, 180, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 10
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 101
            aBoxItem.Position = Position(40.102, 0, (aHeight + 136.315), aSubsItem)
            aBoxItem.Orientation = Orientation(0, 45, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 45
            aRtorItem.InsideRadius = 10
            aRtorItem.OutsideRadius = 20
            aRtorItem.Position = Position(65.205, 0, (aHeight + 182.631), aSubsItem)
            aRtorItem.Orientation = Orientation(90, 45, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 10
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 812.5
            aBoxItem.Position = Position(80, 0, (aHeight + 588.75), aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 10
            aRtorItem.Angle = 90
            aRtorItem.InsideRadius = 42.5
            aRtorItem.OutsideRadius = 107.5
            aRtorItem.Position = Position(80, 75, (aHeight + 995), aSubsItem)
            aRtorItem.Orientation = Orientation(90, 0, -90, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 10
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(80, 75, (aHeight + 1070), aSubsItem)
            aRtorItem.Orientation = Orientation(0, 90, 0, aSubsItem)

            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(-230, 0, 0, aStruItem)
            aSubsItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aStruItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 10
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = aHeight + 90
            aBoxItem.Position = Position(0, 0, aBoxItem.Zlength * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 65
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(32.5, 0, 5, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 45
            aRtorItem.InsideRadius = 10
            aRtorItem.OutsideRadius = 20
            aRtorItem.Position = Position(15, 0, (aHeight + 90), aSubsItem)
            aRtorItem.Orientation = Orientation(-90, 0, 180, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 10
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 101
            aBoxItem.Position = Position(40.102, 0, (aHeight + 136.315), aSubsItem)
            aBoxItem.Orientation = Orientation(0, -45, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 45
            aRtorItem.InsideRadius = 10
            aRtorItem.OutsideRadius = 20
            aRtorItem.Position = Position(65.205, 0, (aHeight + 182.631), aSubsItem)
            aRtorItem.Orientation = Orientation(-90, -45, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 10
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 812.5
            aBoxItem.Position = Position(80, 0, (aHeight + 588.75), aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 10
            aRtorItem.Angle = 90
            aRtorItem.InsideRadius = 42.5
            aRtorItem.OutsideRadius = 107.5
            aRtorItem.Position = Position(80, -75, (aHeight + 995), aSubsItem)
            aRtorItem.Orientation = Orientation(-90, 0, 90, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 10
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(80, -75, (aHeight + 1070), aSubsItem)
            aRtorItem.Orientation = Orientation(0, -90, 180, aSubsItem)

            # Hoop Cage
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = 455
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(384, -152.5, (aHeight + 1070), aSubsItem)
            
            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = 455
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-384, -152.5, (aHeight + 1070), aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 380
            aRtorItem.OutsideRadius = 388
            aRtorItem.Position = Position(0, -380, (aHeight + 1070), aSubsItem)
            aRtorItem.Orientation = Orientation(0, -1, 0, 0, 0, -1, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 65
            aCyliItem.Position = Position(347.5, 50, aHeight + 1070, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 65
            aCyliItem.Position = Position(-347.5, 50, aHeight + 1070, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            # Jointed Floor Mounted
            aHandrailInset = 76
            aHandrialDiameter = 38

            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = aClearance + 52
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-384, aBoxItem.Ylength * 0.5 + 43, aHeight + 1070, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = aClearance + 52
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(384, aBoxItem.Ylength * 0.5 + 43, aHeight + 1070, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 8
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(-384, aBoxItem.Position.y + aBoxItem.Ylength * 0.5, aHeight + 1070, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 8
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(384, aBoxItem.Position.y + aBoxItem.Ylength * 0.5, aHeight + 1070, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = aClearance + 160
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-319, aBoxItem.Ylength * 0.5 - 65, aHeight + 535, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = aClearance + 160
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(319, aBoxItem.Ylength * 0.5 - 65, aHeight + 535, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 8
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(-319, aBoxItem.Position.y + aBoxItem.Ylength * 0.5, aHeight + 535, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 8
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(319, aBoxItem.Position.y + aBoxItem.Ylength * 0.5, aHeight + 535, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 100
            aCyliItem.Position = Position(-438, aClearance + 76, aHeight + 1070, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 100
            aCyliItem.Position = Position(438, aClearance + 76, aHeight + 1070, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 165
            aCyliItem.Position = Position(405.5, aClearance + 76, aHeight + 535, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 165
            aCyliItem.Position = Position(-405.5, aClearance + 76, aHeight + 535, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            # Posts.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(488, aClearance + 76, aHeight, aStruItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 535 * 2
            aCyliItem.Position = Position(0, 0, 535, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 76
            aBoxItem.Ylength = 114
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(0, 0, 5, aSubsItem)
            aBoxItem.Orientation = Orientation(1, 0, 0, 0, 0, 1, aSubsItem)

            # Posts.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(-488, aClearance + 76, aHeight, aStruItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 535 * 2
            aCyliItem.Position = Position(0, 0, 535, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 76
            aBoxItem.Ylength = 114
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(0, 0, 5, aSubsItem)
            aBoxItem.Orientation = Orientation(1, 0, 0, 0, 0, 1, aSubsItem)

            # Step cylinders.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            aN = int((aHeight - 150) / 230) + 1
            aD = (aHeight - 150) / aN

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 20
            aCyliItem.Height = 450
            aCyliItem.Position = Position(0, -32.5, 150, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            for i in range (aN):
                PipeCad.CreateItem("CYLI")
                aCyliItem = PipeCad.CurrentItem()
                aCyliItem.Color = 503
                aCyliItem.Diameter = 20
                aCyliItem.Height = 450
                aCyliItem.Position = Position(0, -32.5, 150 + (i + 1) * aD, aSubsItem)
                aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)
            # for

            PipeCad.CommitTransaction()
        elif aHeight > 2300 and aHeight < 19000:
            # Ladder Long.
            PipeCad.StartTransaction("Build Ladder")

            PipeCad.CreateItem("STRU", aName)
            aStruItem = PipeCad.CurrentItem()

            # Angle.
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(-225, 0, 0, aStruItem)
            aSubsItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aStruItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = aHeight + 79
            aBoxItem.Position = Position(4, 35, aBoxItem.Zlength * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 70
            aBoxItem.Ylength = 8
            aBoxItem.Zlength = aHeight + 79
            aBoxItem.Position = Position(35, 4, aBoxItem.Zlength * 0.5, aSubsItem)

            # Angle.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(225, 0, 0, aStruItem)
            aSubsItem.Orientation = Orientation(1, 0, 0, 0, 0, 1, aStruItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = aHeight + 79
            aBoxItem.Position = Position(4, 35, aBoxItem.Zlength * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 70
            aBoxItem.Ylength = 8
            aBoxItem.Zlength = aHeight + 79
            aBoxItem.Position = Position(35, 4, aBoxItem.Zlength * 0.5, aSubsItem)

            # Angle slop.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("PYRA")
            aPyraItem = PipeCad.CurrentItem()
            aPyraItem.Color = 503
            aPyraItem.Xbottom = 70
            aPyraItem.Xtop = 70
            aPyraItem.Xoffset = -80
            aPyraItem.Ybottom = 8
            aPyraItem.Ytop = 8
            aPyraItem.Yoffset = 0
            aPyraItem.Height = 59
            aPyraItem.Position = Position(-300, -4, aHeight + 108.5, aSubsItem)

            PipeCad.CreateItem("PYRA")
            aPyraItem = PipeCad.CurrentItem()
            aPyraItem.Color = 503
            aPyraItem.Xbottom = 8
            aPyraItem.Xtop = 8
            aPyraItem.Xoffset = -80
            aPyraItem.Ybottom = 70
            aPyraItem.Ytop = 70
            aPyraItem.Yoffset = 0
            aPyraItem.Height = 59
            aPyraItem.Position = Position(-269, -35, aHeight + 108.5, aSubsItem)

            PipeCad.CreateItem("PYRA")
            aPyraItem = PipeCad.CurrentItem()
            aPyraItem.Color = 503
            aPyraItem.Xbottom = 70
            aPyraItem.Xtop = 70
            aPyraItem.Xoffset = -80
            aPyraItem.Ybottom = 8
            aPyraItem.Ytop = 8
            aPyraItem.Yoffset = 0
            aPyraItem.Height = 59
            aPyraItem.Position = Position(300, -4, aHeight + 108.5, aSubsItem)
            aPyraItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aSubsItem)

            PipeCad.CreateItem("PYRA")
            aPyraItem = PipeCad.CurrentItem()
            aPyraItem.Color = 503
            aPyraItem.Xbottom = 8
            aPyraItem.Xtop = 8
            aPyraItem.Xoffset = -80
            aPyraItem.Ybottom = 70
            aPyraItem.Ytop = 70
            aPyraItem.Yoffset = 0
            aPyraItem.Height = 59
            aPyraItem.Position = Position(269, -35, aHeight + 108.5, aSubsItem)
            aPyraItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aSubsItem)

            # Angle.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(305, 0, aHeight + 137.5, aStruItem)
            aSubsItem.Orientation = Orientation(1, 0, 0, 0, 0, 1, aStruItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = 965
            aBoxItem.Position = Position(4, 35, aBoxItem.Zlength * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 70
            aBoxItem.Ylength = 8
            aBoxItem.Zlength = 965
            aBoxItem.Position = Position(35, 4, aBoxItem.Zlength * 0.5, aSubsItem)

            # Angle.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(-305, 0, aHeight + 137.5, aStruItem)
            aSubsItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aStruItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 8
            aBoxItem.Ylength = 70
            aBoxItem.Zlength = 965
            aBoxItem.Position = Position(4, 35, aBoxItem.Zlength * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 70
            aBoxItem.Ylength = 8
            aBoxItem.Zlength = 965
            aBoxItem.Position = Position(35, 4, aBoxItem.Zlength * 0.5, aSubsItem)

            # Cage.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 535 * 2 + 32.5 + (aHeight - 2300)
            aBoxItem.Position = Position(-416, -343, aHeight + 535 + 32.5 / 2 - (aHeight - 2300) * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 65
            aBoxItem.Zlength = 535 * 2 + 32.5 + (aHeight - 2300)
            aBoxItem.Position = Position(416, -343, aHeight + 535 + 32.5 / 2 - (aHeight - 2300) * 0.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 65
            aBoxItem.Ylength = 6
            aBoxItem.Zlength = 535 * 2 + 32.5 + (aHeight - 2300)
            aBoxItem.Position = Position(0, -759, aHeight + 535 + 32.5 / 2 - (aHeight - 2300) * 0.5, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 106
            aCyliItem.Position = Position(-366, -40, aHeight + 535 * 2, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 106
            aCyliItem.Position = Position(366, -40, aHeight + 535 * 2, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            # Top Cage.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 419
            aRtorItem.OutsideRadius = 425
            aRtorItem.Position = Position(0, -343, aHeight + 535 * 2, aSubsItem)
            aRtorItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aSubsItem)

            # Bottom Cage.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 65
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 419
            aRtorItem.OutsideRadius = 425
            aRtorItem.Position = Position(0, -343, 2332.5, aSubsItem)
            aRtorItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 89
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-422, -298.5, 2332.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 263
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-329, -161, 2332.5, aSubsItem)
            aBoxItem.Orientation = Orientation(0, 0, -45, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 60
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-236, -38, 2332.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 89
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(422, -298.5, 2332.5, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 263
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(329, -161, 2332.5, aSubsItem)
            aBoxItem.Orientation = Orientation(0, 0, 45, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 60
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(236, -38, 2332.5, aSubsItem)

            aN = int((aHeight - 2332.5) / 760) + 1
            aD = (aHeight - 2300) / aN
            if aN > 1:
                for i in range(aN):
                    PipeCad.SetCurrentItem(aSubsItem)
                    PipeCad.CreateItem("SUBS")
                    aSubsItem = PipeCad.CurrentItem()

                    aPz = 2332.5 + aD * (i + 1)

                    PipeCad.CreateItem("RTOR")
                    aRtorItem = PipeCad.CurrentItem()
                    aRtorItem.Color = 503
                    aRtorItem.Height = 65
                    aRtorItem.Angle = 180
                    aRtorItem.InsideRadius = 419
                    aRtorItem.OutsideRadius = 425
                    aRtorItem.Position = Position(0, -343, aPz, aSubsItem)
                    aRtorItem.Orientation = Orientation(0, -1, 0, 0, 0, 1, aSubsItem)

                    PipeCad.CreateItem("BOX")
                    aBoxItem = PipeCad.CurrentItem()
                    aBoxItem.Color = 503
                    aBoxItem.Xlength = 6
                    aBoxItem.Ylength = 89
                    aBoxItem.Zlength = 65
                    aBoxItem.Position = Position(-422, -298.5, aPz, aSubsItem)

                    PipeCad.CreateItem("BOX")
                    aBoxItem = PipeCad.CurrentItem()
                    aBoxItem.Color = 503
                    aBoxItem.Xlength = 6
                    aBoxItem.Ylength = 263
                    aBoxItem.Zlength = 65
                    aBoxItem.Position = Position(-329, -161, aPz, aSubsItem)
                    aBoxItem.Orientation = Orientation(0, 0, -45, aSubsItem)

                    PipeCad.CreateItem("BOX")
                    aBoxItem = PipeCad.CurrentItem()
                    aBoxItem.Color = 503
                    aBoxItem.Xlength = 6
                    aBoxItem.Ylength = 60
                    aBoxItem.Zlength = 65
                    aBoxItem.Position = Position(-236, -38, aPz, aSubsItem)

                    PipeCad.CreateItem("BOX")
                    aBoxItem = PipeCad.CurrentItem()
                    aBoxItem.Color = 503
                    aBoxItem.Xlength = 6
                    aBoxItem.Ylength = 89
                    aBoxItem.Zlength = 65
                    aBoxItem.Position = Position(422, -298.5, aPz, aSubsItem)

                    PipeCad.CreateItem("BOX")
                    aBoxItem = PipeCad.CurrentItem()
                    aBoxItem.Color = 503
                    aBoxItem.Xlength = 6
                    aBoxItem.Ylength = 263
                    aBoxItem.Zlength = 65
                    aBoxItem.Position = Position(329, -161, aPz, aSubsItem)
                    aBoxItem.Orientation = Orientation(0, 0, 45, aSubsItem)

                    PipeCad.CreateItem("BOX")
                    aBoxItem = PipeCad.CurrentItem()
                    aBoxItem.Color = 503
                    aBoxItem.Xlength = 6
                    aBoxItem.Ylength = 60
                    aBoxItem.Zlength = 65
                    aBoxItem.Position = Position(236, -38, aPz, aSubsItem)
                # for
            # if

            # Top Cage.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 343 + aClearance + 76 + 38 * 0.5
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-422, -24, aHeight + 1070, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 343 + aClearance + 76 + 38 * 0.5
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(422, -24, aHeight + 1070, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 343 + aClearance + 76 + 38 * 0.5
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(-422, -24, aHeight + 535, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 6
            aBoxItem.Ylength = 343 + aClearance + 76 + 38 * 0.5
            aBoxItem.Zlength = 65
            aBoxItem.Position = Position(422, -24, aHeight + 535, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 6
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(-422, 295, aHeight + 1070, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 6
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(-422, 295, aHeight + 535, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 6
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(422, 295, aHeight + 1070, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.Color = 503
            aRtorItem.Height = 6
            aRtorItem.Angle = 180
            aRtorItem.InsideRadius = 0.1
            aRtorItem.OutsideRadius = 32.5
            aRtorItem.Position = Position(422, 295, aHeight + 535, aSubsItem)
            aRtorItem.Orientation = Orientation(0, 1, 0, 1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 100
            aCyliItem.Position = Position(-475, 276, aHeight + 1070, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 100
            aCyliItem.Position = Position(-475, 276, aHeight + 535, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 100
            aCyliItem.Position = Position(475, 276, aHeight + 1070, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 100
            aCyliItem.Position = Position(475, 276, aHeight + 535, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 106
            aCyliItem.Position = Position(-366, -40, aHeight + 535, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 106
            aCyliItem.Position = Position(366, -40, aHeight + 535, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            # Posts.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(525, aClearance + 76, aHeight, aStruItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 535 * 2
            aCyliItem.Position = Position(0, 0, 535, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 76
            aBoxItem.Ylength = 114
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(0, 0, 5, aSubsItem)
            aBoxItem.Orientation = Orientation(1, 0, 0, 0, 0, 1, aSubsItem)

            # Posts.
            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()
            aSubsItem.Position = Position(-525, aClearance + 76, aHeight, aStruItem)

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 535 * 2
            aCyliItem.Position = Position(0, 0, 535, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 1070, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)

            PipeCad.CreateItem("DISH")
            aDishItem = PipeCad.CurrentItem()
            aDishItem.Color = 503
            aDishItem.Diameter = 76
            aDishItem.Height = 38
            aDishItem.Radius = 0
            aDishItem.Position = Position(0, 0, 535, aSubsItem)
            aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)

            PipeCad.CreateItem("BOX")
            aBoxItem = PipeCad.CurrentItem()
            aBoxItem.Color = 503
            aBoxItem.Xlength = 76
            aBoxItem.Ylength = 114
            aBoxItem.Zlength = 10
            aBoxItem.Position = Position(0, 0, 5, aSubsItem)
            aBoxItem.Orientation = Orientation(1, 0, 0, 0, 0, 1, aSubsItem)

            # Ladder rungs
            aN = int(aHeight / 230.0)
            aD = aHeight / aN

            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 20
            aCyliItem.Height = 450
            aCyliItem.Position = Position(0, -40, 230, aSubsItem)
            aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            for i in range (1, aN):
                PipeCad.CreateItem("CYLI")
                aCyliItem = PipeCad.CurrentItem()
                aCyliItem.Color = 503
                aCyliItem.Diameter = 20
                aCyliItem.Height = 450
                aCyliItem.Position = Position(0, -40, 230 + i * aD, aSubsItem)
                aCyliItem.Orientation = Orientation(0, 1, 0, -1, 0, 0, aSubsItem)

            PipeCad.CommitTransaction()
    # buildLadder2

    def buildLadder3(self):
        print("build ladder 3")
    # buildLadder3

# Singleton Instance.
aLadderDialog = LadderDialog(PipeCad)

def Create():
    aLadderDialog.show()
# Create
