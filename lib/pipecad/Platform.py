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
# Date: 17:20 2021-12-02

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *

from math import *

class CircularDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Circular Platform"))

        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout(self)
        self.labelName = QLabel("Name")
        self.textName = QLineEdit("PLATFORM-001")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelRadius = QLabel("Radius to outside floor")
        self.textRadius = QLineEdit("2800")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelRadius)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textRadius)

        self.labelAngle = QLabel("Angle")
        self.textAngle = QLineEdit("90")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelAngle)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textAngle)

        self.labelWidth = QLabel("Floor width")
        self.textWidth = QLineEdit("800")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelWidth)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textWidth)

        self.labelFloorThickness = QLabel("Floorplate thickness")
        self.textFloorThickness = QLineEdit("25")
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelFloorThickness)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textFloorThickness)

        self.labelDepth = QLabel("Kickplate depth")
        self.textDepth = QLineEdit("100")
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelDepth)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textDepth)

        self.labelKickplateThickness = QLabel("Kickplate thickness")
        self.textKickplateThickness = QLineEdit("10")
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelKickplateThickness)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.textKickplateThickness)

        self.labelInsideRail = QLabel("Inside rail")
        self.checkInsideRail = QCheckBox()
        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelInsideRail)
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.checkInsideRail)

        self.verticalLayout.addLayout(self.formLayout)

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
        aRadius = float(self.textRadius.text)
        aAngle = float(self.textAngle.text) * 0.5
        aWidth = float(self.textWidth.text)
        aFthickness = float(self.textFloorThickness.text)
        aDepth = float(self.textDepth.text)
        aKthickness = float(self.textKickplateThickness.text)
        hasInsideRail = self.checkInsideRail.checked

        PipeCad.StartTransaction("Create Circular Platform")
        PipeCad.CreateItem("STRU", aName)
        aStruItem = PipeCad.CurrentItem()
        aStruItem.Orientation = Orientation(-1, 0, 0, 0, 0, 1)

        # Kickplate
        PipeCad.CreateItem("SUBS")
        aSubsItem = PipeCad.CurrentItem()

        PipeCad.CreateItem("RTOR")
        aRtorItem = PipeCad.CurrentItem()
        aRtorItem.Color = 467
        aRtorItem.OutsideRadius = aRadius
        aRtorItem.InsideRadius = aRadius - aWidth
        aRtorItem.Height = aFthickness
        aRtorItem.Angle = aAngle

        PipeCad.CreateItem("RTOR")
        aRtorItem = PipeCad.CurrentItem()
        aRtorItem.Color = 467
        aRtorItem.OutsideRadius = aRadius
        aRtorItem.InsideRadius = aRadius - aKthickness
        aRtorItem.Height = aDepth + aFthickness
        aRtorItem.Angle = aAngle

        PipeCad.CreateItem("RTOR")
        aRtorItem = PipeCad.CurrentItem()
        aRtorItem.Color = 467
        aRtorItem.OutsideRadius = aRadius - aWidth + aKthickness
        aRtorItem.InsideRadius = aRadius - aWidth
        aRtorItem.Height = aDepth + aFthickness
        aRtorItem.Angle = aAngle

        PipeCad.CreateItem("RTOR")
        aRtorItem = PipeCad.CurrentItem()
        aRtorItem.Color = 467
        aRtorItem.OutsideRadius = aRadius
        aRtorItem.InsideRadius = aRadius - aWidth
        aRtorItem.Height = aFthickness
        aRtorItem.Angle = aAngle
        aRtorItem.Orientation = Orientation(0, 0, aAngle, aSubsItem)

        PipeCad.CreateItem("RTOR")
        aRtorItem = PipeCad.CurrentItem()
        aRtorItem.Color = 467
        aRtorItem.OutsideRadius = aRadius
        aRtorItem.InsideRadius = aRadius - aKthickness
        aRtorItem.Height = aDepth + aFthickness
        aRtorItem.Angle = aAngle
        aRtorItem.Orientation = Orientation(0, 0, aAngle, aSubsItem)

        PipeCad.CreateItem("RTOR")
        aRtorItem = PipeCad.CurrentItem()
        aRtorItem.Color = 467
        aRtorItem.OutsideRadius = aRadius - aWidth + aKthickness
        aRtorItem.InsideRadius = aRadius - aWidth
        aRtorItem.Height = aDepth + aFthickness
        aRtorItem.Angle = aAngle
        aRtorItem.Orientation = Orientation(0, 0, aAngle, aSubsItem)

        # Handrail.
        PipeCad.SetCurrentItem(aSubsItem)
        PipeCad.CreateItem("SUBS")
        aSubsItem = PipeCad.CurrentItem()

        PipeCad.CreateItem("CTOR")
        aCtorItem = PipeCad.CurrentItem()
        aCtorItem.Color = 503
        aCtorItem.OutsideRadius = aRadius - 38
        aCtorItem.InsideRadius = aRadius - 76
        aCtorItem.Angle = aAngle
        aCtorItem.Position = Position(0, 0, 600, aSubsItem)

        PipeCad.CreateItem("CTOR")
        aCtorItem = PipeCad.CurrentItem()
        aCtorItem.Color = 503
        aCtorItem.OutsideRadius = aRadius - 38
        aCtorItem.InsideRadius = aRadius - 76
        aCtorItem.Angle = aAngle
        aCtorItem.Position = Position(0, 0, 1200, aSubsItem)

        PipeCad.CreateItem("CTOR")
        aCtorItem = PipeCad.CurrentItem()
        aCtorItem.Color = 503
        aCtorItem.OutsideRadius = aRadius - 38
        aCtorItem.InsideRadius = aRadius - 76
        aCtorItem.Angle = aAngle
        aCtorItem.Position = Position(0, 0, 600, aSubsItem)
        aCtorItem.Orientation = Orientation(0, 0, aAngle, aSubsItem)

        PipeCad.CreateItem("CTOR")
        aCtorItem = PipeCad.CurrentItem()
        aCtorItem.Color = 503
        aCtorItem.OutsideRadius = aRadius - 38
        aCtorItem.InsideRadius = aRadius - 76
        aCtorItem.Angle = aAngle
        aCtorItem.Position = Position(0, 0, 1200, aSubsItem)
        aCtorItem.Orientation = Orientation(0, 0, aAngle, aSubsItem)

        # Build post at given interval(max 1000)
        aInterval = 1000
        aLength = aAngle / 180 * math.pi * aRadius

        aR = aRadius - 57
        aM = int(aLength // aInterval)
        aDa = aAngle * 2.0 / aM

        aN = aM + 1
        if math.isclose(aAngle, 180):
            aN = aM

        for i in range(aN):
            aAi = aDa * i * math.pi / 180.0
            aDx = math.cos(aAi) * aR
            aDy = math.sin(aAi) * aR

            PipeCad.SetCurrentItem(aSubsItem)
            PipeCad.CreateItem("SUBS")
            aSubsItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 503
            aCyliItem.Diameter = 38
            aCyliItem.Height = 1200
            aCyliItem.Position = Position(aDx, aDy, 600, aSubsItem)

            # PipeCad.CreateItem("DISH")
            # aDishItem = PipeCad.CurrentItem()
            # aDishItem.Diameter = 76
            # aDishItem.Height = 38
            # aDishItem.radius = 0
            # aDishItem.Orientation = Orientation(0, 0, 1, 0, -1, 0, aSubsItem)
            # aDishItem.Position = aCyliItem.Position

            # PipeCad.CreateItem("DISH")
            # aDishItem = PipeCad.CurrentItem()
            # aDishItem.Diameter = 76
            # aDishItem.Height = 38
            # aDishItem.radius = 0
            # aDishItem.Orientation = Orientation(0, 0, -1, 0, 1, 0, aSubsItem)
            # aDishItem.Position = aCyliItem.Position

        PipeCad.CommitTransaction()

        QDialog.accept(self)
    # accept

# Singleton Instance.
aCircularDlg = CircularDialog(PipeCad)

def CreateCircular():
    aCircularDlg.show()
# Show
