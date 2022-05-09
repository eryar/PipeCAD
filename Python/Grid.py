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


class GridDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(self.tr("Grid Definition"))

        # Name and description.
        self.formLayout = QFormLayout()

        self.labelName = QLabel()
        self.labelName.setText(u"Name")
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel()
        self.labelDescription.setText(u"Description")
        self.lineEditDescription = QLineEdit()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditDescription)
        
        # Gridline table.
        self.horizontalLayoutGroup = QHBoxLayout()
        self.groupBoxX = QGroupBox()
        self.groupBoxX.setTitle(u"X Gridlines")
        self.horizontalLayoutX = QHBoxLayout(self.groupBoxX)
        self.tableWidgetX = QTableWidget(self.groupBoxX)
        self.tableWidgetX.setColumnCount(2)
        self.tableWidgetX.setAlternatingRowColors(True)
        self.tableWidgetX.verticalHeader().hide()
        self.tableWidgetX.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetX.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetX.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidgetX.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetX.setHorizontalHeaderItem(0, QTableWidgetItem("Key"))
        self.tableWidgetX.setHorizontalHeaderItem(1, QTableWidgetItem("Distance"))

        self.horizontalLayoutX.addWidget(self.tableWidgetX)
        self.horizontalLayoutGroup.addWidget(self.groupBoxX)

        self.groupBoxY = QGroupBox(GridDialog)
        self.groupBoxY.setTitle(u"Y Gridlines")
        self.horizontalLayoutY = QHBoxLayout(self.groupBoxY)
        self.tableWidgetY = QTableWidget(self.groupBoxY)
        self.tableWidgetY.setColumnCount(2)
        self.tableWidgetY.setAlternatingRowColors(True)
        self.tableWidgetY.verticalHeader().hide()
        self.tableWidgetY.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetY.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetY.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidgetY.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetY.setHorizontalHeaderItem(0, QTableWidgetItem("Key"))
        self.tableWidgetY.setHorizontalHeaderItem(1, QTableWidgetItem("Distance"))

        self.horizontalLayoutY.addWidget(self.tableWidgetY)
        self.horizontalLayoutGroup.addWidget(self.groupBoxY)

        self.groupBoxZ = QGroupBox(GridDialog)
        self.groupBoxZ.setTitle(u"Elevations")
        self.horizontalLayoutZ = QHBoxLayout(self.groupBoxZ)
        self.tableWidgetZ = QTableWidget(self.groupBoxZ)
        self.tableWidgetZ.setColumnCount(2)
        self.tableWidgetZ.setAlternatingRowColors(True)
        self.tableWidgetZ.verticalHeader().hide()
        self.tableWidgetZ.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetZ.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetZ.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidgetZ.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetZ.setHorizontalHeaderItem(0, QTableWidgetItem("Key"))
        self.tableWidgetZ.setHorizontalHeaderItem(1, QTableWidgetItem("Distance"))

        self.horizontalLayoutZ.addWidget(self.tableWidgetZ)
        self.horizontalLayoutGroup.addWidget(self.groupBoxZ)

        # Actions
        self.horizontalLayoutAction = QHBoxLayout()
        
        self.label = QLabel()
        self.label.setText(u"Gridline")
        
        self.horizontalLayoutAction.addWidget(self.label)

        self.comboBoxType = QComboBox()
        self.comboBoxType.addItem("X")
        self.comboBoxType.addItem("Y")
        self.comboBoxType.addItem("Elevation")

        self.horizontalLayoutAction.addWidget(self.comboBoxType)

        self.labelKey = QLabel()
        self.labelKey.setText(u"Key")

        self.horizontalLayoutAction.addWidget(self.labelKey)

        self.lineEditKey = QLineEdit()
        self.horizontalLayoutAction.addWidget(self.lineEditKey)

        self.labelDistance = QLabel()
        self.labelDistance.setText(u"Distance")

        self.horizontalLayoutAction.addWidget(self.labelDistance)

        self.lineEditDistance = QLineEdit()
        self.horizontalLayoutAction.addWidget(self.lineEditDistance)

        self.comboBoxAction = QComboBox()
        self.comboBoxAction.addItem("Insert After")
        self.comboBoxAction.addItem("Insert Before")
        self.comboBoxAction.addItem("Remove")
        self.comboBoxAction.activated.connect(self.applyAction)

        self.horizontalLayoutAction.addWidget(self.comboBoxAction)

        self.pushButtonPreview = QPushButton()
        self.pushButtonPreview.setText(u"Preview")
        self.pushButtonPreview.clicked.connect(self.preview)

        self.horizontalLayoutAction.addWidget(self.pushButtonPreview)

        self.pushButtonBuild = QPushButton()
        self.pushButtonBuild.setText(u"Build")
        self.pushButtonBuild.clicked.connect(self.build)

        self.horizontalLayoutAction.addWidget(self.pushButtonBuild)

        self.pushButtonCancel = QPushButton()
        self.pushButtonCancel.setText(u"Cancel")
        self.pushButtonCancel.clicked.connect(self.reject)

        self.horizontalLayoutAction.addWidget(self.pushButtonCancel)
        
        aMainLayout = QVBoxLayout()
        aMainLayout.addLayout(self.formLayout)
        aMainLayout.addLayout(self.horizontalLayoutGroup)
        aMainLayout.addLayout(self.horizontalLayoutAction)

        self.setLayout(aMainLayout)
        self.resize(600, 380)
    # setupUi
    
    def applyAction(self, theIndex):
        aTypeIndex = self.comboBoxType.currentIndex
        
        aTableWidget = self.tableWidgetX
        if aTypeIndex == 0:
            # X gridlines
            aTableWidget = self.tableWidgetX
        elif aTypeIndex == 1:
            # Y gridlines
            aTableWidget = self.tableWidgetY
        else:
            # Z gridlines
            aTableWidget = self.tableWidgetZ
            
        if theIndex == 0:
            aRow = aTableWidget.currentRow() + 1
            aTableWidget.insertRow(aRow)
            aTableWidget.setItem(aRow, 0, QTableWidgetItem(self.lineEditKey.text))
            aTableWidget.setItem(aRow, 1, QTableWidgetItem(self.lineEditDistance.text))
            aTableWidget.setCurrentCell(aRow, 0)
        elif theIndex == 2:
            aRow = aTableWidget.currentRow()
            aTableWidget.removeRow(aRow)
    # applyAction

    def preview(self):
    
        PipeCad.ClearAid()
        
        aLx = []
        aLy = []
        aLz = []
        
        # Total x length
        for i in range(self.tableWidgetX.rowCount):
            aLx.append(float(self.tableWidgetX.item(i, 1).text()))
        # for
        
        # Total y length
        for i in range(self.tableWidgetY.rowCount):
            aLy.append(float(self.tableWidgetY.item(i, 1).text()))
        # for
        
        # Total z length
        for i in range(self.tableWidgetZ.rowCount):
            aLz.append(float(self.tableWidgetZ.item(i, 1).text()))
        # for
        
        aMx = max(aLx)
        aMy = max(aLy)
        aMz = max(aLz)
        
        # Draw aid line in elevations.
        for e in range (self.tableWidgetZ.rowCount):
            aZ = float(self.tableWidgetZ.item(e, 1).text())

            # Draw aid line in x direction.
            aPs = Position(0, -1000, aZ)
            aPe = Position(0, aMy + 1000, aZ)
            PipeCad.AddAidLine(aPs, aPe, 1)
            
            for i in range(self.tableWidgetX.rowCount):
                aT = self.tableWidgetX.item(i, 0).text()
                aX = float(self.tableWidgetX.item(i, 1).text())
                
                aPs.x = aX
                aPe.x = aX
                PipeCad.AddAidLine(aPs, aPe, 1)
                PipeCad.AddAidText(aPe, aT, 1)
            # for
            
            # Draw aid line in y direction.
            aPs = Position(-1000, 0, aZ)
            aPe = Position(aMx + 1000, 0, aZ)
            PipeCad.AddAidLine(aPs, aPe, 1)
            for i in range(self.tableWidgetY.rowCount):
                aT = self.tableWidgetY.item(i, 0).text()
                aY = float(self.tableWidgetY.item(i, 1).text())
                
                aPs.y = aY
                aPe.y = aY
                PipeCad.AddAidLine(aPs, aPe, 1)
                PipeCad.AddAidText(aPs, aT, 1)
            # for
        # for
        
        PipeCad.Update()
    # preview
        
    def build(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", "Please enter grid name!")
            return
        # if

        aLx = []
        aLy = []
        aLz = []
        
        # Total x length
        for i in range(self.tableWidgetX.rowCount):
            aLx.append(float(self.tableWidgetX.item(i, 1).text()))
        # for
        
        # Total y length
        for i in range(self.tableWidgetY.rowCount):
            aLy.append(float(self.tableWidgetY.item(i, 1).text()))
        # for
        
        # Total z length
        for i in range(self.tableWidgetZ.rowCount):
            aLz.append(float(self.tableWidgetZ.item(i, 1).text()))
        # for
        
        aMx = max(aLx)
        aMy = max(aLy)
        aMz = max(aLz)

        try:
            
            PipeCad.StartTransaction("Create Grid")
            PipeCad.CreateItem("STRU", aName)

            aStruItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("FRMW", aName + "/0")
            aFrmwItem = PipeCad.CurrentItem()
            aSbfrItem = aFrmwItem

            # Draw aid line in elevations.
            for e in range (self.tableWidgetZ.rowCount):
                aZ = float(self.tableWidgetZ.item(e, 1).text())

                # Draw aid line in x direction.
                aPs = Position(0, -1000, aZ)
                aPe = Position(0, aMy + 1000, aZ)

                PipeCad.SetCurrentItem(aSbfrItem)
                PipeCad.CreateItem("SBFR", aName + "/" + str(e + 1))
                aSbfrItem = PipeCad.CurrentItem()

                PipeCad.CreateItem("SCTN", aSbfrItem.Name + "/X0")
                aSctnItem = PipeCad.CurrentItem()
                aSctnItem.StartPosition = aPs
                aSctnItem.EndPosition = aPe
                
                for i in range(self.tableWidgetX.rowCount):
                    aT = self.tableWidgetX.item(i, 0).text()
                    aX = float(self.tableWidgetX.item(i, 1).text())
                    
                    aPs.x = aX
                    aPe.x = aX

                    PipeCad.CreateItem("SCTN", aSbfrItem.Name + "/X" + str(i+1))
                    aSctnItem = PipeCad.CurrentItem()
                    aSctnItem.StartPosition = aPs
                    aSctnItem.EndPosition = aPe
                # for
                
                # Draw aid line in y direction.
                aPs = Position(-1000, 0, aZ)
                aPe = Position(aMx + 1000, 0, aZ)

                PipeCad.CreateItem("SCTN", aSbfrItem.Name + "/Y0")
                aSctnItem = PipeCad.CurrentItem()
                aSctnItem.StartPosition = aPs
                aSctnItem.EndPosition = aPe
                
                for i in range(self.tableWidgetY.rowCount):
                    aT = self.tableWidgetY.item(i, 0).text()
                    aY = float(self.tableWidgetY.item(i, 1).text())
                    
                    aPs.y = aY
                    aPe.y = aY

                    PipeCad.CreateItem("SCTN", aSbfrItem.Name + "/Y" + str(i+1))
                    aSctnItem = PipeCad.CurrentItem()
                    aSctnItem.StartPosition = aPs
                    aSctnItem.EndPosition = aPe
                # for
            # for

            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # build

    def reject(self):
        PipeCad.ClearAid()
        QDialog.reject(self)
    # reject

# Singleton Instance.
aGridDialog = GridDialog(PipeCad)

def Create():
    aGridDialog.show()
# Create

def Show():
    print("show grid")
# Show
