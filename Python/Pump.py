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
# Date: 11:20 2021-11-02

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *

class PumpDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(500, 360)
        self.setWindowTitle(self.tr("Standard Pumps"))

        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.textName.setMaximumWidth(180)
        
        self.labelType = QLabel("Type")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.comboBoxType = QComboBox()
        self.comboBoxType.addItem("Centrifugal Pump Centerline Mounted")
        self.comboBoxType.addItem("Centrifugal Pump Horizontal Inlet/Vertical Outlet")
        self.comboBoxType.addItem("Center Line Mounted, Vertical Nozzles Centrifugal Pumps")
        self.comboBoxType.addItem("Center Line Mounted, Tangential Offset Centrifugal Pumps")
        self.comboBoxType.addItem("Center Line Mounted, Vertical Offset Nozzles")

        self.comboBoxType.currentIndexChanged.connect(self.typeChanged)

        self.comboBoxType.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.comboBoxType.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)
        self.horizontalLayout.addWidget(self.labelType)
        self.horizontalLayout.addWidget(self.comboBoxType)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setMinimumWidth(280)
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumWidth(400)
        
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Dimension", "Value"])
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.tableWidget.verticalHeader().setHidden(True)

        self.horizontalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addWidget(self.labelDiagram)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.typeChanged(0)
        self.retranslateUi()
    # setupUi

    def retranslateUi(self):
        pass
    # retranslateUi

    def typeChanged(self, theIndex):
        # Set Parameters List
        self.tableWidget.clearContents()

        if theIndex == 0:
            # Centrifugal Pump Centerline Mounted
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-pump001.png"))
            self.tableWidget.setRowCount(8)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Baseplate Length"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Baseplate Width"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Distance Origin to Baseplate"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Distance Suction Nozzle"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Distance Bottom to CI"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Dicharge Nozzle to Coupling"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Distance Suction Nozzle to Coupling"))
            self.tableWidget.setItem(7, 0, QTableWidgetItem("H = Outside Diameter Discharge"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1500"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("500"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("220"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("155"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("340"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("180"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("500"))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("60"))
        elif theIndex == 1:
            # Centrifugal Pump Horizontal Inlet/Vertical Outlet
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-pump002.png"))
            self.tableWidget.setRowCount(11)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Baseplate Length"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Baseplate Width"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Baseplate Height"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Height Baseplate to CI"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Discharge Nozzle Height"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Suction Nozzle Height"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Distance Discharge Nozzle"))
            self.tableWidget.setItem(7, 0, QTableWidgetItem("H = Origin to Baseplate End"))
            self.tableWidget.setItem(8, 0, QTableWidgetItem("J = Distance to Coupling"))
            self.tableWidget.setItem(9, 0, QTableWidgetItem("K = Coupling Height"))
            self.tableWidget.setItem(10, 0, QTableWidgetItem("L = Motor Length"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1800"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("650"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("80"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("300"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("400"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("300"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("200"))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("350"))
            self.tableWidget.setItem(8, 1, QTableWidgetItem("950"))
            self.tableWidget.setItem(9, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(10, 1, QTableWidgetItem("800"))
        elif theIndex == 2:
            # Centre Line Mounted, Vertical Nozzles
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-pump003.png"))
            self.tableWidget.setRowCount(9)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Baseplate Length"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Baseplate Width"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Distance Origin to Baseplate"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Total Distance"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Distance Bottom to CI"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Nozzle Height"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Distance Suction Nozzle"))
            self.tableWidget.setItem(7, 0, QTableWidgetItem("H = Outside Diameter Suction"))
            self.tableWidget.setItem(8, 0, QTableWidgetItem("J = Distance Discharge Nozzle"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1500"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("500"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("300"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("1200"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("340"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("180"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("150"))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("120"))
            self.tableWidget.setItem(8, 1, QTableWidgetItem("130"))
        else:
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-pump000.png"))
            self.tableWidget.setRowCount(0)

        # Disable edit for column 1
        for r in range (self.tableWidget.rowCount):
            self.tableWidget.item(r, 0).setFlags(Qt.NoItemFlags)
    # typeChanged

    def accept(self):
        aName = self.textName.text
        aType = self.comboBoxType.currentIndex

        if len(aName) < 1:
            QMessageBox.warning(self, "", u"Please input Pump Name!")
            return

        if aType == 0:
            # Centrifugal Pump Centerline Mounted
            A = float(self.tableWidget.item(0, 1).text())
            B = float(self.tableWidget.item(1, 1).text())
            C = float(self.tableWidget.item(2, 1).text())
            D = float(self.tableWidget.item(3, 1).text())
            E = float(self.tableWidget.item(4, 1).text())
            F = float(self.tableWidget.item(5, 1).text())
            G = float(self.tableWidget.item(6, 1).text())
            H = float(self.tableWidget.item(7, 1).text())

            aDiameter = A / 4.714
            aHeight = (A - C - G + D + 1.5 * H - 79) * 0.5

            PipeCad.StartTransaction("Centrifugal Pump")
            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = B
            aItem.Ylength = A
            aItem.Zlength = A * 0.065
            aItem.Position = Position(0, C - A * 0.5, aItem.Zlength * 0.5 - E)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = F * 1.3
            aItem.Ylength = H * 1.2
            aItem.Zlength = E
            aItem.Position = Position(0, 0, E * -0.5)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = F * 1.3
            aItem.Height = H * 1.2
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("CONE")
            aItem = PipeCad.CurrentItem()
            aItem.Tdiameter = H * 0.6
            aItem.Bdiameter = H * 1.8
            aItem.Height = G - D - H * 2
            aItem.Position = Position(0, aItem.Height * -0.5 - H * 0.6, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            aHeight1 = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = H * 0.4
            aItem.Height = A - C - A / 3.5
            aItem.Position = Position(0, -0.6 * aItem.Height, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = H * 1.2
            aItem.Height = H * 0.4
            aItem.Position = Position(0, D - G + H * 0.2, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = H * 1.2
            aItem.Height = H * 0.4
            aItem.Position = Position(0, -G, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = aDiameter
            aItem.Height = aHeight
            aItem.Position = Position(0, C + A / 3.5 - A, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = aDiameter
            aItem.Height = aHeight * 0.1
            aItem.Radius = 25
            aItem.Position = Position(0, C + A / 3.5 - A + aHeight * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = aDiameter
            aItem.Height = aHeight * 0.1
            aItem.Radius = 25
            aItem.Position = Position(0, C + A / 3.5 - A - aHeight * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = aDiameter
            aItem.Ylength = aHeight * 0.8
            aItem.Zlength = E
            aItem.Position = Position(0, C + A / 3.5 - A, E * -0.5)

            PipeCad.CreateItem("NOZZ", aName + "-N1")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = D
            aNozzItem.Position = Position(0, D, 0)
            aNozzItem.Orientation = Orientation(1, 0, 0, 0, 0, 1)

            aCatref = PipeCad.GetItem("/AAZFBD0HH")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N2")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = F
            aNozzItem.Position = Position(0, 0, F)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0FF")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CommitTransaction()
        elif aType == 1:
            # Centrifugal Pump Horizontal Inlet/Vertical Outlet
            A = float(self.tableWidget.item(0, 1).text())
            B = float(self.tableWidget.item(1, 1).text())
            C = float(self.tableWidget.item(2, 1).text())
            D = float(self.tableWidget.item(3, 1).text())
            E = float(self.tableWidget.item(4, 1).text())
            F = float(self.tableWidget.item(5, 1).text())
            G = float(self.tableWidget.item(6, 1).text())
            H = float(self.tableWidget.item(7, 1).text())
            J = float(self.tableWidget.item(8, 1).text())
            K = float(self.tableWidget.item(9, 1).text())
            L = float(self.tableWidget.item(10, 1).text())

            PipeCad.StartTransaction("Build Centrifugal Pump")
            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = B
            aItem.Ylength = A
            aItem.Zlength = C
            aItem.Position = Position(0, H - A * 0.5, C * -0.5 - D)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 2
            aItem.Height = (J - F * 0.5) * 0.67
            aItem.Position = Position(0, F * 0.5 - aItem.Height * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = D * 1.25
            aItem.Ylength = (J - F * 0.5) * 0.67
            aItem.Zlength = D
            aItem.Position = Position(0, F * 0.5 - aHeight * 0.5, D * -0.5)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 1.5
            aItem.Height = (J - F * 0.5) * 0.33
            aItem.Position = Position(0, F * 0.5 - aHeight - aItem.Height * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            aHeight1 = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.3
            aItem.Height = K
            aItem.Position = Position(0, F * 0.5 - aHeight - aHeight1 - aItem.Height * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 1.5
            aItem.Height = L
            aItem.Position = Position(0, F - J - K - aItem.Height * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("NOZZ", aName + "-N1")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = F
            aNozzItem.Position = Position(0, F, 0)
            aNozzItem.Orientation = Orientation(1, 0, 0, 0, 0, 1)

            aCatref = PipeCad.GetItem("/AAZFBD0NN")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N2")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = E
            aNozzItem.Position = Position(-G, 0, E)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0HH")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CommitTransaction()
        elif aType == 2:
            # Centre Line Mounted, Vertical Nozzles
            A = float(self.tableWidget.item(0, 1).text())
            B = float(self.tableWidget.item(1, 1).text())
            C = float(self.tableWidget.item(2, 1).text())
            D = float(self.tableWidget.item(3, 1).text())
            E = float(self.tableWidget.item(4, 1).text())
            F = float(self.tableWidget.item(5, 1).text())
            G = float(self.tableWidget.item(6, 1).text())
            H = float(self.tableWidget.item(7, 1).text())
            J = float(self.tableWidget.item(8, 1).text())

            PipeCad.StartTransaction("Build Centrifugal Pump")
            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = B
            aItem.Ylength = A
            aItem.Zlength = A * 0.065
            aItem.Position = Position(0, C - A * 0.5, aItem.Zlength * 0.5 - E)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = B * 0.9
            aItem.Ylength = H * 1.1
            aItem.Zlength = J * 0.6 + E
            aItem.Position = Position(0, 0, J * 0.3 - E * 0.5)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = J * 2
            aItem.Height = H * 1.8
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("CONE")
            aItem = PipeCad.CurrentItem()
            aItem.Tdiameter = J * 1.2
            aItem.Bdiameter = J * 2
            aItem.Height = H
            aItem.Position = Position(0, -0.5 * aItem.Height - 0.5 * aHeight, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            aHeight1 = aItem.Height

            PipeCad.CreateItem("CONE")
            aItem = PipeCad.CurrentItem()
            aItem.Tdiameter = J * 1.2
            aItem.Bdiameter = J * 2
            aItem.Height = H
            aItem.Position = Position(0, 0.5 * aItem.Height + 0.5 * aHeight, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.03
            aItem.Height = D * 0.684 - H * 3.8
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - (D * 0.684 - H * 3.8) / 2, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.1
            aItem.Height = D * 0.03
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - aItem.Height * 0.5 - (D * 0.64 - H * 1.9 - 127 -C) / 2, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.1
            aItem.Height = D * 0.03
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - aItem.Height * 0.5 - D * 0.045 - (D * 0.64 - H * 1.9 + 127 -C) / 2, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.2
            aItem.Height = D * 0.22
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - D * 0.684 + H * 3.8 - D * 0.15, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.2
            aItem.Height = D * 0.04
            aItem.Radius = 100
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - D * 0.684 + H * 3.8 - D * 0.04, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = D * 0.2
            aItem.Height = D * 0.04
            aItem.Radius = 100
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - D * 0.684 + H * 3.8 - D * 0.26, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            PipeCad.CreateItem("BOX")
            aItem = PipeCad.CurrentItem()
            aItem.Xlength = D * 0.15
            aItem.Ylength = D * 0.15
            aItem.Zlength = E
            aItem.Position = Position(0, -0.5 * aHeight - aHeight1 - D * 0.684 + H * 3.8 - D * 0.15, -0.5 * E)

            PipeCad.CreateItem("NOZZ", aName + "-N1")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = F
            aNozzItem.Position = Position(-G, 0, F)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0NN")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N2")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = F
            aNozzItem.Position = Position(J, 0, F)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0HH")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CommitTransaction()
        # endif

        QDialog.accept(self)
    # accept

aPumpDlg = PumpDialog(PipeCad)

def Show():
    aPumpDlg.textName.setText("")
    aPumpDlg.show()
# Show
