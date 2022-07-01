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
# CreateSpiral

class StairDialog(QDialog):
    """docstring for StairDialog"""
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.lstrItem = None

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Stair", "Create Stair"))

        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.comboName = QComboBox()
        self.comboName.addItem(QT_TRANSLATE_NOOP("Stair", "Create"))
        self.comboName.addItem(QT_TRANSLATE_NOOP("Stair", "Modify"))
        self.comboName.activated.connect(self.typeActivated)

        self.textName = QLineEdit()

        self.labelPx = QLabel(QT_TRANSLATE_NOOP("Stair", "East"))
        self.textPx = QLineEdit("0")

        self.labelPy = QLabel(QT_TRANSLATE_NOOP("Stair", "North"))
        self.textPy = QLineEdit("0")

        self.labelPz = QLabel(QT_TRANSLATE_NOOP("Stair", "Up"))
        self.textPz = QLineEdit("0")

        self.labelDir = QLabel(QT_TRANSLATE_NOOP("Stair", "Direction"))
        self.textDir = QLineEdit("N")

        self.labelHeight = QLabel(QT_TRANSLATE_NOOP("Stair", "Height"))
        self.textHeight = QLineEdit("2800")

        self.labelAngle = QLabel(QT_TRANSLATE_NOOP("Stair", "Angle"))
        self.textAngle = QLineEdit("35")

        self.labelDepth = QLabel(QT_TRANSLATE_NOOP("Stair", "Stringer Depth"))
        self.textDepth = QLineEdit("200")

        self.labelThickness = QLabel(QT_TRANSLATE_NOOP("Stair", "Stringer Thickness"))
        self.textThickness = QLineEdit("75")

        self.labelWidth = QLabel(QT_TRANSLATE_NOOP("Stair", "Width Between Stringers"))
        self.textWidth = QLineEdit("800")

        self.labelFloorThickness = QLabel(QT_TRANSLATE_NOOP("Stair", "Landing Floor Thickness"))
        self.textFloorThickness = QLineEdit("30")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelPx)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textPx)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelPy)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textPy)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelPz)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textPz)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelDir)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textDir)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelHeight)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textHeight)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.labelAngle)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.textAngle)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelDepth)
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.textDepth)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.labelThickness)
        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.textThickness)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.labelWidth)
        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.textWidth)

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.labelFloorThickness)
        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.textFloorThickness)

        self.verticalLayout.addLayout(self.formLayout)

        # Action box.
        self.horizontalLayout = QHBoxLayout()

        self.buttonReset = QPushButton(QT_TRANSLATE_NOOP("Stair", "Reset"))
        self.buttonReset.clicked.connect(self.reset)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.horizontalLayout.addWidget(self.buttonReset)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def reset(self):
        self.textName.setText("")

        self.textPx.setText("0")
        self.textPy.setText("0")
        self.textPz.setText("0")
        self.textDir.setText("N")

        self.textHeight.setText("2800")
        self.textAngle.setText("35")
        self.textDepth.setText("200")
        self.textThickness.setText("75")
        self.textWidth.setText("800")
        self.textFloorThickness.setText("30")
    # reset

    def typeActivated(self):
        self.lstrItem = None
        aIndex = self.comboName.currentIndex
        if aIndex == 1:
            # Modify
            aTreeItem = PipeCad.CurrentItem()
            if aTreeItem.Type == "LSTR":
                self.lstrItem = aTreeItem

                aPos = aTreeItem.Position
                aOri = aTreeItem.Orientation

                self.textName.setText(aTreeItem.Name)
                self.textPx.setText(str(aPos.X))
                self.textPy.setText(str(aPos.Y))
                self.textPz.setText(str(aPos.Z))

                self.textDir.setText(aOri.YDirection.string())
                self.textHeight.setText(str(aTreeItem.Height))
                self.textAngle.setText(str(aTreeItem.Angle))
                self.textDepth.setText(str(aTreeItem.StringerDepth))
                self.textThickness.setText(str(aTreeItem.StringerThickness))
                self.textWidth.setText(str(aTreeItem.Width))
                self.textFloorThickness.setText(str(aTreeItem.FloorThickness))
            # if
        # if
    # indexChanged

    def createStair(self):
        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        aHeight = float(self.textHeight.text)
        aAngle = float(self.textAngle.text)
        aDepth = float(self.textDepth.text)
        aThickness = float(self.textThickness.text)
        aWidth = float(self.textWidth.text)
        aFloorThickness = float(self.textFloorThickness.text)

        aDy = Direction(self.textDir.text)
        aDz = Direction(0, 0, 1)

        PipeCad.StartTransaction("Create Stair")

        PipeCad.CreateItem("LSTR", self.textName.text)
        aLstrItem = PipeCad.CurrentItem()
        aLstrItem.Position = Position(aPx, aPy, aPz)
        aLstrItem.Orientation = Orientation(aDy, aDz)
        aLstrItem.Height = aHeight
        aLstrItem.Angle = aAngle
        aLstrItem.Width = aWidth
        aLstrItem.StringerDepth = aDepth
        aLstrItem.StringerThickness = aThickness
        aLstrItem.FloorThickness = aFloorThickness

        PipeCad.CommitTransaction()
    # createStair

    def modifyStair(self):
        if self.lstrItem is None:
            return
        # if

        aPx = float(self.textPx.text)
        aPy = float(self.textPy.text)
        aPz = float(self.textPz.text)

        aHeight = float(self.textHeight.text)
        aAngle = float(self.textAngle.text)
        aDepth = float(self.textDepth.text)
        aThickness = float(self.textThickness.text)
        aWidth = float(self.textWidth.text)
        aFloorThickness = float(self.textFloorThickness.text)

        aDy = Direction(self.textDir.text)
        aDz = Direction(0, 0, 1)

        PipeCad.StartTransaction("Modify Stair")

        self.lstrItem.Name = self.textName.text
        self.lstrItem.Position = Position(aPx, aPy, aPz)
        self.lstrItem.Orientation = Orientation(aDy, aDz)
        self.lstrItem.Height = aHeight
        self.lstrItem.Angle = aAngle
        self.lstrItem.Width = aWidth
        self.lstrItem.StringerDepth = aDepth
        self.lstrItem.StringerThickness = aThickness
        self.lstrItem.FloorThickness = aFloorThickness

        PipeCad.CommitTransaction()
    # modifyStair

    def accept(self):
        aIndex = self.comboName.currentIndex
        if aIndex == 0:
            self.createStair()
        else:
            self.modifyStair()
        # if

        QDialog.accept(self)
    # accept
# StairDialog

# Singleton Instance.
aStairDlg = StairDialog(PipeCad)

def CreateStair():
    aStairDlg.reset()
    aStairDlg.show()
# CreateStair
