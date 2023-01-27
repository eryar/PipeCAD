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

class VesselDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(500, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Standard Vessels"))

        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.textName.setMaximumWidth(180)
        
        self.labelType = QLabel("Type")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.comboBoxType = QComboBox()
        self.comboBoxType.addItem("Storage Tanks Flat Top")
        self.comboBoxType.addItem("Storage Tanks Dished Top")
        self.comboBoxType.addItem("Storage Tanks Conical Top")
        self.comboBoxType.addItem("Storage Vessels Horizontal with Dished Ends")
        self.comboBoxType.addItem("Storage Vessels Horizontal One End Dished & Flanged")
        self.comboBoxType.addItem("Storage Vessels Horizontal Coned One End")
        self.comboBoxType.addItem("Storage Vessels Vertical with Dished Top & Bottom")

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
        self.tableWidget.setMinimumWidth(180)
        self.labelDiagram = QLabel()
        self.labelDiagram.setMinimumWidth(400)
        
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Dimension", "Value"])
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)

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
            # Flat Top Tank
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-tank001.png"))
            self.tableWidget.setRowCount(2)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Height"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("5000"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("3500"))
        elif theIndex == 1:
            # Dished Top Tank
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-tank002.png"))
            self.tableWidget.setRowCount(4)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Height"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Dish Height"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Dish Radius"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("5000"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("3500"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("800"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("100"))
        elif theIndex == 2:
            # Conical Top Tank
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-tank003.png"))
            self.tableWidget.setRowCount(4)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Height"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Cone Height"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Cone Top Diameter"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("5000"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("3500"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("800"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("300"))
        else:
            self.tableWidget.setRowCount(0)
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-tank000.png"))

        # Disable edit for column 1
        for r in range (self.tableWidget.rowCount):
            self.tableWidget.item(r, 0).setFlags(Qt.NoItemFlags)
    # typeChanged

    def accept(self):
        aName = self.textName.text
        aType = self.comboBoxType.currentIndex

        if aType == 0:
            # Flat Top Tank
            aDiameter = float(self.tableWidget.item(0, 1).text())
            aHeight = float(self.tableWidget.item(1, 1).text())

            PipeCad.StartTransaction("Build Flat Top Tank")
            PipeCad.CreateItem("EQUI", aName)
            PipeCad.CreateItem("CYLI")

            aCylinder = PipeCad.CurrentItem()
            aCylinder.Diameter = aDiameter
            aCylinder.Height = aHeight
            aCylinder.Position = Position(0, 0, aHeight * 0.5)

            PipeCad.CommitTransaction()
        elif aType == 1:
            # Dished Top Tank
            aDiameter = float(self.tableWidget.item(0, 1).text())
            aHeight = float(self.tableWidget.item(1, 1).text())
            aDishHeight = float(self.tableWidget.item(2, 1).text())
            aDishRadius = float(self.tableWidget.item(3, 1).text())

            PipeCad.StartTransaction("Build Dished Top Tank")
            PipeCad.CreateItem("EQUI", aName)
            PipeCad.CreateItem("CYLI")

            aCylinder = PipeCad.CurrentItem()
            aCylinder.Diameter = aDiameter
            aCylinder.Height = aHeight
            aCylinder.Position = Position(0, 0, aHeight * 0.5)

            PipeCad.CreateItem("DISH")
            aDish = PipeCad.CurrentItem()
            aDish.Diameter = aDiameter
            aDish.Height = aDishHeight
            aDish.Radius = aDishRadius
            aDish.Position = Position(0, 0, aHeight)

            PipeCad.CommitTransaction()
        elif aType == 2:
            # Conical Top Tank
            aDiameter = float(self.tableWidget.item(0, 1).text())
            aHeight = float(self.tableWidget.item(1, 1).text())
            aConeHeight = float(self.tableWidget.item(2, 1).text())
            aTopDiameter = float(self.tableWidget.item(3, 1).text())

            PipeCad.StartTransaction("Build Conical Top Tank")
            PipeCad.CreateItem("EQUI", aName)
            PipeCad.CreateItem("CYLI")

            aCylinder = PipeCad.CurrentItem()
            aCylinder.Diameter = aDiameter
            aCylinder.Height = aHeight
            aCylinder.Position = Position(0, 0, aHeight * 0.5)

            PipeCad.CreateItem("CONE")
            aCone = PipeCad.CurrentItem()
            aCone.Bdiameter = aDiameter
            aCone.Tdiameter = aTopDiameter
            aCone.Height = aConeHeight
            aCone.Position = Position(0, 0, aHeight + aConeHeight * 0.5)

            PipeCad.CommitTransaction()
        # endif

        QDialog.accept(self)
    # accept

aVesselDlg = VesselDialog(PipeCad)

def Show():
    aVesselDlg.textName.setText("")
    aVesselDlg.show()
# Show
