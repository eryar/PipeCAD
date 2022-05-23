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
# Date: 11:20 2022-05-22

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *

class SpiralDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(500, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Spiral Stair"))

        self.verticalLayout = QVBoxLayout(self)
        self.gridLayout = QGridLayout()

        # Name
        self.labelName = QLabel(QT_TRANSLATE_NOOP("Design", "Name"))
        self.textName = QLineEdit("SPIRAL-STAIR-01")

        self.gridLayout.addWidget(self.labelName, 0, 0)
        self.gridLayout.addWidget(self.textName, 0, 1)

        # Position
        self.labelX = QLabel("East")
        self.textX = QLineEdit("0")
        self.labelY = QLabel("North")
        self.textY = QLineEdit("0")
        self.labelZ = QLabel("Up")
        self.textZ = QLineEdit("0")

        self.gridLayout.addWidget(self.labelX, 1, 0)
        self.gridLayout.addWidget(self.textX, 1, 1)

        self.gridLayout.addWidget(self.labelY, 2, 0)
        self.gridLayout.addWidget(self.textY, 2, 1)

        self.gridLayout.addWidget(self.labelZ, 3, 0)
        self.gridLayout.addWidget(self.textZ, 3, 1)

        # Spiral stair parameters.
        self.labelSpiralHeight = QLabel(QT_TRANSLATE_NOOP("Design", "Spiral Height"))
        self.textSpiralHeight = QLineEdit("18000")

        self.labelSpiralAngle = QLabel(QT_TRANSLATE_NOOP("Design", "Spiral Angle"))
        self.textSpiralAngle = QLineEdit("180")

        self.labelOutsideRadius = QLabel(QT_TRANSLATE_NOOP("Design", "Outside Radius"))
        self.textOutsideRadius = QLineEdit("5000")

        self.labelInsideRadius = QLabel(QT_TRANSLATE_NOOP("Design", "Inside Radius"))
        self.textInsideRadius = QLineEdit("3800")

        self.labelStepHeight = QLabel(QT_TRANSLATE_NOOP("Design", "Step Height"))
        self.textStepHeight = QLineEdit("150")

        self.labelStepThickness = QLabel(QT_TRANSLATE_NOOP("Design", "Step Thickness"))
        self.textStepThickness = QLineEdit("10")

        #self.labelPostNumber = QLabel(QT_TRANSLATE_NOOP("Design", "Post Number"))
        #self.textPostNumber = QLineEdit("4")

        self.gridLayout.addWidget(self.labelSpiralHeight, 4, 0)
        self.gridLayout.addWidget(self.textSpiralHeight, 4, 1)

        self.gridLayout.addWidget(self.labelSpiralAngle, 5, 0)
        self.gridLayout.addWidget(self.textSpiralAngle, 5, 1)

        self.gridLayout.addWidget(self.labelOutsideRadius, 6, 0)
        self.gridLayout.addWidget(self.textOutsideRadius, 6, 1)

        self.gridLayout.addWidget(self.labelInsideRadius, 7, 0)
        self.gridLayout.addWidget(self.textInsideRadius, 7, 1)

        self.gridLayout.addWidget(self.labelStepHeight, 8, 0)
        self.gridLayout.addWidget(self.textStepHeight, 8, 1)

        self.gridLayout.addWidget(self.labelStepThickness, 9, 0)
        self.gridLayout.addWidget(self.textStepThickness, 9, 1)

        #self.gridLayout.addWidget(self.labelPostNumber, 10, 0)
        #self.gridLayout.addWidget(self.textPostNumber, 10, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    # setupUi

    def accept(self):

        aX = float(self.textX.text)
        aY = float(self.textY.text)
        aZ = float(self.textZ.text)

        aSpiralHeight = float(self.textSpiralHeight.text)
        aSpiralAngle = float(self.textSpiralAngle.text)
        aOutsideRadius = float(self.textOutsideRadius.text)
        aInsideRadius = float(self.textInsideRadius.text)
        aStepHeight = float(self.textStepHeight.text)
        aStepThickness = float(self.textStepThickness.text)

        aStepNumber = int(aSpiralHeight / aStepHeight)
        aStepAngle = aSpiralAngle / aStepNumber

        PipeCad.StartTransaction("Build Spiral Stair")

        PipeCad.CreateItem("STRU", self.textName.text)
        aStruItem = PipeCad.CurrentItem()
        aStruItem.Position = Position(aX, aY, aZ)

        PipeCad.CreateItem("SUBS")

        for i in range(aStepNumber):
            PipeCad.CreateItem("RTOR")
            aRtorItem = PipeCad.CurrentItem()
            aRtorItem.InsideRadius = aInsideRadius
            aRtorItem.OutsideRadius = aOutsideRadius
            aRtorItem.Height = aStepThickness
            aRtorItem.Angle = aStepAngle
            aRtorItem.Color = 122

            PipeCad.Rotate(aStepAngle * i)
            PipeCad.Translate(0, 0, aStepHeight * i)

            aAngle = math.radians(aStepAngle) * i

            PipeCad.CreateItem("CYLI")
            aCyliItem = PipeCad.CurrentItem()
            aCyliItem.Color = 122
            aCyliItem.Diameter = 15
            aCyliItem.Height = 1200
            aCyliItem.Position = Position(
                aOutsideRadius * math.cos(aAngle),
                aOutsideRadius * math.sin(aAngle),
                aStepHeight * i + 600, aStruItem)
        # for

        PipeCad.CommitTransaction()
        
        QDialog.accept(self)
    # accept
#

# Singleton Instance.
aSpiralDlg = SpiralDialog(PipeCad)

def CreateSpiral():
    aSpiralDlg.show()
# Show
