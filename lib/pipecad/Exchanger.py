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

class ExchangerDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(500, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Standard Heat Exchangers"))

        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.textName.setMaximumWidth(180)
        
        self.labelType = QLabel("Type")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.comboBoxType = QComboBox()
        self.comboBoxType.addItem("Dished One End")
        self.comboBoxType.addItem("Dished Both Ends")
        self.comboBoxType.addItem("Flanged Both Ends")
        self.comboBoxType.addItem("Dished Both Ends With Nozzles")
        self.comboBoxType.addItem("Dished And Flanged With Nozzles")

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
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
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
            # Dished One End
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-exc001.png"))
            self.tableWidget.setRowCount(7)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Flange Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Exchanger Diameter"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Flange Thickness"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Head Height"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Exchanger Length"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Dish Height"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Dish Radius"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1200"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("1000"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("700"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("4000"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("250"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("100"))
        elif theIndex == 1:
            # Dished Both Ends
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-exc002.png"))
            self.tableWidget.setRowCount(8)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Flange Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Exchanger Diameter"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Flange Thickness"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Head Height"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Exchanger Length"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Second Head Height"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Dish Height"))
            self.tableWidget.setItem(7, 0, QTableWidgetItem("H = Dish Radius"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1200"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("1000"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("700"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("4000"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("700"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("250"))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("100"))

        elif theIndex == 2:
            # Flanged Both Ends
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-exc003.png"))
            self.tableWidget.setRowCount(6)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Flange Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Exchanger Diameter"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Flange Thickness"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Head Height"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Exchanger Length"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Second Head Height"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1200"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("1000"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("700"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("4000"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("750"))

        elif theIndex == 3:
            # Dished Both Ends With Nozzles
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-exc004.png"))
            self.tableWidget.setRowCount(10)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Flange Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Exchanger Diameter"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Flange Thickness"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Head Height"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Exchanger Length"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Dish Height"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Dish Radius"))
            self.tableWidget.setItem(7, 0, QTableWidgetItem("H = Nozzle Height"))
            self.tableWidget.setItem(8, 0, QTableWidgetItem("J = Distance N1/N2 to N3/N4"))
            self.tableWidget.setItem(9, 0, QTableWidgetItem("K = Distance N3/N4 to N5/N6"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1200"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("1000"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("700"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("5500"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("250"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("650"))
            self.tableWidget.setItem(8, 1, QTableWidgetItem("1700"))
            self.tableWidget.setItem(9, 1, QTableWidgetItem("1600"))
        elif theIndex == 4:
            # Dished And Flanged With Nozzles
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-exc005.png"))
            self.tableWidget.setRowCount(10)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("A = Flange Diameter"))
            self.tableWidget.setItem(1, 0, QTableWidgetItem("B = Exchanger Diameter"))
            self.tableWidget.setItem(2, 0, QTableWidgetItem("C = Flange Thickness"))
            self.tableWidget.setItem(3, 0, QTableWidgetItem("D = Head Height"))
            self.tableWidget.setItem(4, 0, QTableWidgetItem("E = Exchanger Length"))
            self.tableWidget.setItem(5, 0, QTableWidgetItem("F = Dish Height"))
            self.tableWidget.setItem(6, 0, QTableWidgetItem("G = Dish Radius"))
            self.tableWidget.setItem(7, 0, QTableWidgetItem("H = Nozzle Height"))
            self.tableWidget.setItem(8, 0, QTableWidgetItem("J = Distance Between N2 and N3"))
            self.tableWidget.setItem(9, 0, QTableWidgetItem("K = Distance Between N1 and N4"))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("1200"))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("1000"))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("500"))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("5500"))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("250"))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("100"))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("650"))
            self.tableWidget.setItem(8, 1, QTableWidgetItem("1700"))
            self.tableWidget.setItem(9, 1, QTableWidgetItem("2800"))
        else:
            self.labelDiagram.setPixmap(QPixmap(":/PipeCad/Resources/std-exc000.png"))
            self.tableWidget.setRowCount(0)

        # Disable edit for column 1
        for r in range (self.tableWidget.rowCount):
            self.tableWidget.item(r, 0).setFlags(Qt.NoItemFlags)
    # typeChanged

    def accept(self):
        aName = self.textName.text
        aType = self.comboBoxType.currentIndex

        if len(aName) < 1:
            QMessageBox.warning(self, "", u"Please input Heat Exchanger Name!")
            return

        if aType == 0:
            # Dished One End
            A = float(self.tableWidget.item(0, 1).text())
            B = float(self.tableWidget.item(1, 1).text())
            C = float(self.tableWidget.item(2, 1).text())
            D = float(self.tableWidget.item(3, 1).text())
            E = float(self.tableWidget.item(4, 1).text())
            F = float(self.tableWidget.item(5, 1).text())
            G = float(self.tableWidget.item(6, 1).text())

            PipeCad.StartTransaction("Build Exchanger")
            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = D - C * 2
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * (aHeight + C), 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * (aHeight + C) - C - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, aHeight * 0.5 + C * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, aHeight * 0.5 + C * 1.5 + 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = E - C
            aItem.Position = Position(0, -0.5 * aHeight - C * 1.5 - E * 0.5 - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = F
            aItem.Radius = G
            aItem.Position = Position(0, -0.5 * aHeight - C - E - 10, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            PipeCad.CommitTransaction()
        elif aType == 1:
            # Dished Both Ends
            A = float(self.tableWidget.item(0, 1).text())
            B = float(self.tableWidget.item(1, 1).text())
            C = float(self.tableWidget.item(2, 1).text())
            D = float(self.tableWidget.item(3, 1).text())
            E = float(self.tableWidget.item(4, 1).text())
            F = float(self.tableWidget.item(5, 1).text())
            G = float(self.tableWidget.item(6, 1).text())
            H = float(self.tableWidget.item(7, 1).text())

            PipeCad.StartTransaction("Build Dished Exchanger")
            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = D - C * 2
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - C * 0.5, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - C * 1.5 - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = G
            aItem.Radius = 100
            aItem.Position = Position(0, 0.5 * aHeight, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = E - C
            aItem.Position = Position(0, -0.5 * aHeight - C * 1.5 - E * 0.5 - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - C * 1.5 - E - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - C * 2.5 - E - 20, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = F - C
            aItem.Position = Position(0, -0.5 * aHeight - C * 3 - E - aItem.Height * 0.5 - 20, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = G
            aItem.Radius = 100
            aItem.Position = Position(0, -0.5 * aHeight - C * 2 - E - F - 20, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            PipeCad.CommitTransaction()
        elif aType == 2:
            # Flanged Both Ends
            A = float(self.tableWidget.item(0, 1).text())
            B = float(self.tableWidget.item(1, 1).text())
            C = float(self.tableWidget.item(2, 1).text())
            D = float(self.tableWidget.item(3, 1).text())
            E = float(self.tableWidget.item(4, 1).text())
            F = float(self.tableWidget.item(5, 1).text())

            PipeCad.StartTransaction("Build Flanged Exchanger")

            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = D - C * 2
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 0.5 * C, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 1.5 * C - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, 0.5 * aHeight + 0.5 * C, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, 0.5 * aHeight + 1.5 * C + 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = E - C * 2
            aItem.Position = Position(0, -0.5 * aHeight - 2 * C - aItem.Height * 0.5 - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            aHeight1 = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 2.5 * C - aHeight1 - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 3.5 * C - aHeight1 - 20, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = F - C * 2
            aItem.Position = Position(0, -0.5 * aHeight - 4 * C- aHeight1 - aItem.Height * 0.5 - 20, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            aHeight2 = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 4.5 * C - aHeight1 - aHeight2 - 20, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 5.5 * C - aHeight1 - aHeight2 - 30, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CommitTransaction()
        elif aType == 3:
            # Dished Both Ends With Nozzles
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

            PipeCad.StartTransaction("Build Flanged Exchanger")

            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = (D - F) * 2
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 0.5 * C, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 1.5 * C - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = F
            aItem.Radius = G
            aItem.Position = Position(0, 0.5 * aHeight, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = E - F - D - aHeight * 0.5 - 10 - C * 2
            aItem.Position = Position(0, -0.5 * (E - F - 10 - C * 2 - aHeight * 0.5) - C * 3 - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            aHeight1 = aItem.Height

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = F
            aItem.Radius = G
            aItem.Position = Position(0, -aHeight1 - 0.5 * aHeight - C * 2 - 10, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            PipeCad.CreateItem("NOZZ", aName + "-N1")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, 0, H)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N2")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, 0, -H)
            aNozzItem.Orientation = Orientation(0, -1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N3")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, -J, -H)
            aNozzItem.Orientation = Orientation(0, -1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N4")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, -J, H)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N5")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, -J - K, H)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N6")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, -J - K, -H)
            aNozzItem.Orientation = Orientation(0, -1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CommitTransaction()
        elif aType == 4:
            # Dished And Flanged Ends With Nozzles
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

            PipeCad.StartTransaction("Build Dished And Flanged Exchanger")

            PipeCad.CreateItem("EQUI", aName)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = (D - C * 2 - 10) * 2
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            aHeight = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 0.5 * C, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -0.5 * aHeight - 1.5 * C - 10, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = E - F - D - aHeight * 0.5 - 10 - C * 2
            aItem.Position = Position(0, C + 25 - E / 2, 0)
            aItem.Orientation = Orientation(0, 0, -1, 0, 1, 0)

            aHeight1 = aItem.Height

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, 0.5 * aHeight + 0.5 * C, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, 0.5 * aHeight + 1.5 * C + 10, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("DISH")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = F
            aItem.Radius = G
            aItem.Position = Position(0, -aHeight1 - 1.5 * aHeight - C * 4 - 20, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, -1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -aHeight1 - 0.5 * aHeight - 2.5 * C - 10, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = A
            aItem.Height = C
            aItem.Position = Position(0, -aHeight1 - 0.5 * aHeight - 3.5 * C - 20, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("CYLI")
            aItem = PipeCad.CurrentItem()
            aItem.Diameter = B
            aItem.Height = aHeight
            aItem.Position = Position(0, -aHeight1 - aHeight - 4 * C - 20, 0)
            aItem.Orientation = Orientation(0, 0, 1, 0, 1, 0)

            PipeCad.CreateItem("NOZZ", aName + "-N1")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, 0, H)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N2")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, 0, -H)
            aNozzItem.Orientation = Orientation(0, -1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N3")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, -J, -H)
            aNozzItem.Orientation = Orientation(0, -1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CreateItem("NOZZ", aName + "-N4")
            aNozzItem = PipeCad.CurrentItem()
            aNozzItem.Height = H
            aNozzItem.Position = Position(0, -K, H)
            aNozzItem.Orientation = Orientation(0, 1, 0, 1, 0, 0)

            aCatref = PipeCad.GetItem("/AAZFBD0TT")
            if aCatref is not None:
                aNozzItem.Catref = aCatref
            # if

            PipeCad.CommitTransaction()
        # endif

        QDialog.accept(self)
    # accept

aExchangerDlg = ExchangerDialog(PipeCad)

def Show():
    aExchangerDlg.textName.setText("")
    aExchangerDlg.show()
# Show
