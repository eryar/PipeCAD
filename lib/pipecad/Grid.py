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
        self.setWindowTitle(QT_TRANSLATE_NOOP("Grid", "Grid Definition"))

        self.aidNumber = PipeCad.NextAidNumber()

        # Name and description.
        self.formLayout = QFormLayout()

        self.labelName = QLabel()
        self.labelName.setText(QT_TRANSLATE_NOOP("Grid", "Name"))
        self.textName = QLineEdit()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel()
        self.labelDescription.setText(QT_TRANSLATE_NOOP("Grid", "Description"))
        self.textDescription = QLineEdit()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDescription)
        
        # Gridline table.
        self.horizontalLayoutGroup = QHBoxLayout()
        self.groupBoxX = QGroupBox()
        self.groupBoxX.setTitle(QT_TRANSLATE_NOOP("Grid", "X Gridlines"))
        self.horizontalLayoutX = QHBoxLayout(self.groupBoxX)
        self.tableWidgetX = QTableWidget(self.groupBoxX)
        self.tableWidgetX.setColumnCount(2)
        self.tableWidgetX.setAlternatingRowColors(True)
        self.tableWidgetX.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidgetX.verticalHeader().hide()
        self.tableWidgetX.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetX.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetX.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidgetX.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetX.setHorizontalHeaderItem(0, QTableWidgetItem("Key"))
        self.tableWidgetX.setHorizontalHeaderItem(1, QTableWidgetItem("Distance"))

        self.actionAddX = QAction(QIcon(":/PipeCad/Resources/plus-white.png"), QT_TRANSLATE_NOOP("Grid", "Add"), self.tableWidgetX)
        self.actionDelX = QAction(QIcon(":/PipeCad/Resources/minus-white.png"), QT_TRANSLATE_NOOP("Grid", "Delete"), self.tableWidgetX)

        self.actionAddX.triggered.connect(self.addX)
        self.actionDelX.triggered.connect(self.delX)

        self.tableWidgetX.addAction(self.actionAddX)
        self.tableWidgetX.addAction(self.actionDelX)

        self.horizontalLayoutX.addWidget(self.tableWidgetX)
        self.horizontalLayoutGroup.addWidget(self.groupBoxX)

        self.groupBoxY = QGroupBox(GridDialog)
        self.groupBoxY.setTitle(QT_TRANSLATE_NOOP("Grid", "Y Gridlines"))
        self.horizontalLayoutY = QHBoxLayout(self.groupBoxY)
        self.tableWidgetY = QTableWidget(self.groupBoxY)
        self.tableWidgetY.setColumnCount(2)
        self.tableWidgetY.setAlternatingRowColors(True)
        self.tableWidgetY.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidgetY.verticalHeader().hide()
        self.tableWidgetY.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetY.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetY.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidgetY.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetY.setHorizontalHeaderItem(0, QTableWidgetItem("Key"))
        self.tableWidgetY.setHorizontalHeaderItem(1, QTableWidgetItem("Distance"))

        self.actionAddY = QAction(QIcon(":/PipeCad/Resources/plus-white.png"), QT_TRANSLATE_NOOP("Grid", "Add"), self.tableWidgetY)
        self.actionDelY = QAction(QIcon(":/PipeCad/Resources/minus-white.png"), QT_TRANSLATE_NOOP("Grid", "Delete"), self.tableWidgetY)

        self.actionAddY.triggered.connect(self.addY)
        self.actionDelY.triggered.connect(self.delY)

        self.tableWidgetY.addAction(self.actionAddY)
        self.tableWidgetY.addAction(self.actionDelY)

        self.horizontalLayoutY.addWidget(self.tableWidgetY)
        self.horizontalLayoutGroup.addWidget(self.groupBoxY)

        self.groupBoxZ = QGroupBox(GridDialog)
        self.groupBoxZ.setTitle(QT_TRANSLATE_NOOP("Grid", "Elevations"))
        self.horizontalLayoutZ = QHBoxLayout(self.groupBoxZ)
        self.tableWidgetZ = QTableWidget(self.groupBoxZ)
        self.tableWidgetZ.setColumnCount(2)
        self.tableWidgetZ.setAlternatingRowColors(True)
        self.tableWidgetZ.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidgetZ.verticalHeader().hide()
        self.tableWidgetZ.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetZ.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetZ.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidgetZ.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetZ.setHorizontalHeaderItem(0, QTableWidgetItem("Key"))
        self.tableWidgetZ.setHorizontalHeaderItem(1, QTableWidgetItem("Distance"))

        self.actionAddZ = QAction(QIcon(":/PipeCad/Resources/plus-white.png"), QT_TRANSLATE_NOOP("Grid", "Add"), self.tableWidgetZ)
        self.actionDelZ = QAction(QIcon(":/PipeCad/Resources/minus-white.png"), QT_TRANSLATE_NOOP("Grid", "Delete"), self.tableWidgetZ)

        self.actionAddZ.triggered.connect(self.addZ)
        self.actionDelZ.triggered.connect(self.delZ)

        self.tableWidgetZ.addAction(self.actionAddZ)
        self.tableWidgetZ.addAction(self.actionDelZ)

        self.horizontalLayoutZ.addWidget(self.tableWidgetZ)
        self.horizontalLayoutGroup.addWidget(self.groupBoxZ)

        # Actions
        self.horizontalLayoutAction = QHBoxLayout()
        
        self.label = QLabel()
        self.label.setText(QT_TRANSLATE_NOOP("Grid", "Gridline"))
        
        self.horizontalLayoutAction.addWidget(self.label)

        self.comboBoxType = QComboBox()
        self.comboBoxType.addItem("X")
        self.comboBoxType.addItem("Y")
        self.comboBoxType.addItem("Elevation")

        self.horizontalLayoutAction.addWidget(self.comboBoxType)

        self.labelKey = QLabel()
        self.labelKey.setText(QT_TRANSLATE_NOOP("Grid", "Key"))

        self.horizontalLayoutAction.addWidget(self.labelKey)

        self.lineEditKey = QLineEdit()
        self.horizontalLayoutAction.addWidget(self.lineEditKey)

        self.labelDistance = QLabel()
        self.labelDistance.setText(QT_TRANSLATE_NOOP("Grid", "Distance"))

        self.horizontalLayoutAction.addWidget(self.labelDistance)

        self.lineEditDistance = QLineEdit()
        self.horizontalLayoutAction.addWidget(self.lineEditDistance)

        self.comboBoxAction = QComboBox()
        self.comboBoxAction.addItem(QT_TRANSLATE_NOOP("Grid", "Insert After"))
        self.comboBoxAction.addItem(QT_TRANSLATE_NOOP("Grid", "Insert Before"))
        self.comboBoxAction.addItem(QT_TRANSLATE_NOOP("Grid", "Remove"))
        self.comboBoxAction.activated.connect(self.applyAction)

        self.horizontalLayoutAction.addWidget(self.comboBoxAction)

        self.pushButtonPreview = QPushButton()
        self.pushButtonPreview.setText(QT_TRANSLATE_NOOP("Grid", "Preview"))
        self.pushButtonPreview.clicked.connect(self.preview)

        self.horizontalLayoutAction.addWidget(self.pushButtonPreview)

        self.pushButtonBuild = QPushButton()
        self.pushButtonBuild.setText(QT_TRANSLATE_NOOP("Grid", "Build"))
        self.pushButtonBuild.clicked.connect(self.build)

        self.horizontalLayoutAction.addWidget(self.pushButtonBuild)

        self.pushButtonCancel = QPushButton()
        self.pushButtonCancel.setText(QT_TRANSLATE_NOOP("Grid", "Cancel"))
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

    def addGridline(self, theTableWidget):
        aRow = theTableWidget.currentRow() + 1
        theTableWidget.insertRow(aRow)
        theTableWidget.setItem(aRow, 0, QTableWidgetItem(self.lineEditKey.text))
        theTableWidget.setItem(aRow, 1, QTableWidgetItem(self.lineEditDistance.text))
        theTableWidget.setCurrentCell(aRow, 0)
    # addGrid

    def delGridline(self, theTableWidget):
        aRow = theTableWidget.currentRow()
        theTableWidget.removeRow(aRow)
    # delGridline

    def addX(self):
        self.addGridline(self.tableWidgetX)
    # addX

    def delX(self):
        self.delGridline(self.tableWidgetX)
    # delX

    def addY(self):
        self.addGridline(self.tableWidgetY)
    # addY

    def delY(self):
        self.delGridline(self.tableWidgetY)
    # delY

    def addZ(self):
        self.addGridline(self.tableWidgetZ)
    # addZ

    def delZ(self):
        self.delGridline(self.tableWidgetZ)
    # delZ

    def preview(self):
    
        PipeCad.RemoveAid(self.aidNumber)
        
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

        if len(aLx) == 0 or len(aLy) == 0 or len(aLz) == 0:
            return
        # if
        
        # Draw aid line in elevations.
        for e in range (self.tableWidgetZ.rowCount):
            aZ = float(self.tableWidgetZ.item(e, 1).text())

            # Draw aid line in x direction.
            aPs = Position(aLx[0], aLy[0] -1000, aZ)
            aPe = Position(aLx[0], aLy[-1] + 1000, aZ)
            
            for i in range(self.tableWidgetX.rowCount):
                aT = self.tableWidgetX.item(i, 0).text()
                aX = float(self.tableWidgetX.item(i, 1).text())
                
                aPs.X = aX
                aPe.X = aX
                PipeCad.AddAidLine(aPs, aPe, self.aidNumber)
                PipeCad.AddAidText(aPs, aT, self.aidNumber)
            # for
            
            # Draw aid line in y direction.
            aPs = Position(aLx[0] -1000, aLy[0], aZ)
            aPe = Position(aLx[-1] + 1000, aLy[0], aZ)

            for i in range(self.tableWidgetY.rowCount):
                aT = self.tableWidgetY.item(i, 0).text()
                aY = float(self.tableWidgetY.item(i, 1).text())
                
                aPs.Y = aY
                aPe.Y = aY
                PipeCad.AddAidLine(aPs, aPe, 1)
                PipeCad.AddAidText(aPs, aT, 1)
            # for
        # for
        
        PipeCad.UpdateViewer()
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

        try:
            
            PipeCad.StartTransaction("Create Grid")
            PipeCad.CreateItem("STRU", aName)

            aStruItem = PipeCad.CurrentItem()

            PipeCad.CreateItem("FRMW", aName + "/0")
            aFrmwItem = PipeCad.CurrentItem()
            aFrmwItem.Description = self.textDescription.text
            aSbfrItem = aFrmwItem

            # Draw aid line in elevations.
            for e in range (self.tableWidgetZ.rowCount):
                aT = self.tableWidgetZ.item(e, 0).text()
                aZ = float(self.tableWidgetZ.item(e, 1).text())

                # Draw aid line in x direction.
                aPs = Position(0, aLy[0] -1000, aZ)
                aPe = Position(0, aLy[-1] + 1000, aZ)

                PipeCad.SetCurrentItem(aSbfrItem)
                PipeCad.CreateItem("SBFR", aName + "/" + str(e + 1))
                aSbfrItem = PipeCad.CurrentItem()
                aSbfrItem.Description = aT
                
                for i in range(self.tableWidgetX.rowCount):
                    aT = self.tableWidgetX.item(i, 0).text()
                    aX = float(self.tableWidgetX.item(i, 1).text())
                    
                    aPs.X = aX
                    aPe.X = aX

                    PipeCad.CreateItem("SCTN", aSbfrItem.Name + "/X" + str(i+1))
                    aSctnItem = PipeCad.CurrentItem()
                    aSctnItem.Description = aT
                    aSctnItem.StartPosition = aPs
                    aSctnItem.EndPosition = aPe
                # for
                
                # Draw aid line in y direction.
                aPs = Position(aLx[0] -1000, 0, aZ)
                aPe = Position(aLx[-1] + 1000, 0, aZ)
                
                for i in range(self.tableWidgetY.rowCount):
                    aT = self.tableWidgetY.item(i, 0).text()
                    aY = float(self.tableWidgetY.item(i, 1).text())
                    
                    aPs.Y = aY
                    aPe.Y = aY

                    PipeCad.CreateItem("SCTN", aSbfrItem.Name + "/Y" + str(i+1))
                    aSctnItem = PipeCad.CurrentItem()
                    aSctnItem.Description = aT
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
        PipeCad.RemoveAid(self.aidNumber)
        QDialog.reject(self)
    # reject

# Singleton Instance.
aGridDialog = GridDialog(PipeCad)

def Create():
    aGridDialog.show()
# Create

class TagDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Display Gridlines"))

        self.verticalLayout = QVBoxLayout(self)

        # Grid list
        self.horizontalLayout = QHBoxLayout()

        self.gridList = QListWidget()
        self.gridList.setAlternatingRowColors(True)
        self.gridList.setSelectionMode(QAbstractItemView.SingleSelection)

        self.elevList = QListWidget()
        self.elevList.setAlternatingRowColors(True)
        self.elevList.setSelectionMode(QAbstractItemView.ContiguousSelection)

        self.horizontalLayout.addWidget(self.gridList)
        self.horizontalLayout.addWidget(self.elevList)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Action buttons.
        self.horizontalLayout = QHBoxLayout()

        self.buttonReload = QPushButton(QT_TRANSLATE_NOOP("Design", "Reload"))
        self.buttonReload.clicked.connect(self.reload)

        self.labelTag = QLabel(QT_TRANSLATE_NOOP("Design", "Tag With"))
        self.comboTag = QComboBox()
        self.comboTag.addItem(QT_TRANSLATE_NOOP("Design", "Key"))
        self.comboTag.addItem(QT_TRANSLATE_NOOP("Design", "Name"))

        self.buttonAdd = QPushButton(QT_TRANSLATE_NOOP("Design", "Add"))
        self.buttonAdd.clicked.connect(self.addGridTag)

        self.buttonRemove = QPushButton(QT_TRANSLATE_NOOP("Design", "Remove"))
        self.buttonRemove.clicked.connect(self.removeGridTag)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel, self)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonReload)
        self.horizontalLayout.addWidget(self.labelTag)
        self.horizontalLayout.addWidget(self.comboTag)
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def reload(self):
        self.gridList.clear()
        self.elevList.clear()

        self.struItem = PipeCad.CurrentItem()
        if self.struItem.Type != "STRU":
            self.struItem = None
            QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Design", "Please select gridline STRU!"))
            return
        # if

        self.aidNumber = PipeCad.NextAidNumber()

        aFrmwItems = PipeCad.CollectItem("FRMW", self.struItem)
        for aFrmwItem in aFrmwItems:
            aGridItem = QListWidgetItem(aFrmwItem.Description, self.gridList)
            aGridItem.setData(Qt.UserRole, aFrmwItem)

            aSbfrItems = PipeCad.CollectItem("SBFR", aFrmwItem)
            for aSbfrItem in aSbfrItems:
                aElevItem = QListWidgetItem(aSbfrItem.Description, self.elevList)
                aElevItem.setData(Qt.UserRole, aSbfrItem)
            # for
        # for

    # reload

    def addGridTag(self):
        PipeCad.RemoveAid(self.aidNumber)

        aSbfrItems = self.elevList.selectedItems()
        for aSbfrItem in aSbfrItems:
            aSctnItems = PipeCad.CollectItem("SCTN", aSbfrItem.data(Qt.UserRole))
            if self.comboTag.currentIndex == 0:
                for aSctnItem in aSctnItems:
                    PipeCad.AddAidText(aSctnItem.StartPosition, aSctnItem.Description, self.aidNumber)
                # for
            else:
                for aSctnItem in aSctnItems:
                    PipeCad.AddAidText(aSctnItem.StartPosition, aSctnItem.Name, self.aidNumber)
                # for
            # if
        # for
        PipeCad.UpdateViewer()
    # addGridTag

    def removeGridTag(self):
        PipeCad.RemoveAid(self.aidNumber)
        PipeCad.UpdateViewer()
    # removeGridTag

# TagDialog

# Singleton Instance.
aTagDlg = TagDialog(PipeCad)

def Display():
    aTagDlg.reload()
    aTagDlg.show()
# Show
