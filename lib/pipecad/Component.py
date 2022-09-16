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
# Date: 15:16 2021-09-27

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.pipecad import *

from pipecad import *


class ComponentDialog():
    def __init__(self, parent = None):
        self.dockWidget = QDockWidget()
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidget.visibilityChanged.connect(self.visibilityChanged)
        self.currentItem = None
        self.Arrive = 1
        self.Leave = 2
        self.ArriveBore = ""
        self.LeaveBore = ""
        self.altSpec = None
        self.tagId = PipeCad.NextAidNumber()
        self.branchTagId = PipeCad.NextAidNumber()
    # __init__

    def visibilityChanged(self, theVisibility):
        if theVisibility:
            PipeCad.currentItemChanged.connect(self.currentItemChanged)
        else:
            PipeCad.currentItemChanged.disconnect()
            PipeCad.removeDockWidget(self.dockWidget)

            PipeCad.RemoveAid(self.tagId)
            PipeCad.RemoveAid(self.branchTagId)
        # if
    # visibilityChanged

    def createComponent(self):

        aToggleAction = self.dockWidget.toggleViewAction()
        aToggleAction.setText("Create Component")
        self.dockWidget.setWindowTitle("Create Component")
        self.dockWidget.show()

        self.dockContent = QWidget()
        self.verticalLayout = QVBoxLayout(self.dockContent)
        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Branch
        self.horizontalLayout = QHBoxLayout()
        self.labelBranch = QLabel("Branch: ")
        self.labelBranch.setSizePolicy(aSizePolicy)
        self.textBranch = QLabel()
        self.buttonBranch = QPushButton("Set Branch")
        self.buttonBranch.setSizePolicy(aSizePolicy)
        self.buttonBranch.clicked.connect(self.setBranch)

        self.horizontalLayout.addWidget(self.labelBranch)
        self.horizontalLayout.addWidget(self.textBranch)
        self.horizontalLayout.addWidget(self.buttonBranch)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Branch Spec.
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel()
        self.textSpec.setSizePolicy(aSizePolicy)
        self.labelBore = QLabel("Bore: ")
        self.labelBore.setSizePolicy(aSizePolicy)
        self.textBore = QLabel()

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.labelBore)
        self.horizontalLayout.addWidget(self.textBore)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Alternative Spec.
        self.horizontalLayout = QHBoxLayout()
        self.checkBoxSpec = QCheckBox("Alternative Spec:")
        self.labelAltSpec = QLabel("None")
        self.buttonAltSpec = QPushButton("Select")
        self.buttonAltSpec.clicked.connect(self.selectAltSpec)

        self.horizontalLayout.addWidget(self.checkBoxSpec)
        self.horizontalLayout.addWidget(self.labelAltSpec)
        self.horizontalLayout.addWidget(self.buttonAltSpec)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        # Type and Sub-Type Filter.
        self.formLayout = QFormLayout()

        self.comboType = QComboBox()
        self.comboType.currentTextChanged.connect(self.typeChanged)

        self.comboFilter = QComboBox()
        self.comboFilter.currentTextChanged.connect(self.subTypeChanged)

        self.formLayout.addRow("Type", self.comboType)
        self.formLayout.addRow("Skey", self.comboFilter)

        self.verticalLayout.addLayout(self.formLayout)

        # Component Table.
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Bore"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Description"))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.verticalHeader().hide()

        self.verticalLayout.addWidget(self.tableWidget)

        # Reducer Info.
        self.reducerInfo = QGroupBox("Reducer Infomation")

        self.horizontalLayout = QHBoxLayout(self.reducerInfo)
        self.labelLeaveBore = QLabel("Leave Bore")
        self.comboLeaveBore = QComboBox()
        self.buttonReducer12 = QPushButton()
        self.buttonReducer21 = QPushButton()

        self.buttonGroup = QButtonGroup(self.reducerInfo)
        self.buttonGroup.addButton(self.buttonReducer12)
        self.buttonGroup.addButton(self.buttonReducer21)

        #self.buttonReducer12.setFlat(True)
        #self.buttonReducer21.setFlat(True)

        self.buttonReducer12.setCheckable(True)
        self.buttonReducer21.setCheckable(True)

        self.buttonReducer12.setChecked(True)

        self.buttonReducer12.setMaximumWidth(24)
        self.buttonReducer21.setMaximumWidth(24)

        self.buttonReducer12.setToolTip("Arrive major bore, leave minor bore")
        self.buttonReducer21.setToolTip("Arrive minor bore, leave major bore")

        self.buttonReducer12.setIcon(QIcon(":/PipeCad/Resources/reducer12-16.png"))
        self.buttonReducer21.setIcon(QIcon(":/PipeCad/Resources/reducer21-16.png"))

        self.buttonReducer12.clicked.connect(lambda: self.setArriveLeave(1, 2))
        self.buttonReducer21.clicked.connect(lambda: self.setArriveLeave(2, 1))

        self.horizontalSpacer = QSpacerItem(16, 16, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addWidget(self.labelLeaveBore)
        self.horizontalLayout.addWidget(self.comboLeaveBore)
        self.horizontalLayout.addWidget(self.buttonReducer12)
        self.horizontalLayout.addWidget(self.buttonReducer21)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addWidget(self.reducerInfo)

        # Tee Info.
        self.connectionInfo = QGroupBox("Connection Infomation")
        self.horizontalLayout = QHBoxLayout(self.connectionInfo)
        self.labelConnectBore = QLabel("Conn. Bore")
        self.comboConnectBore = QComboBox()
        self.buttonConnect1 = QPushButton()
        self.buttonConnect2 = QPushButton()
        self.buttonConnect3 = QPushButton()

        self.buttonGroup = QButtonGroup(self.connectionInfo)
        self.buttonGroup.addButton(self.buttonConnect1)
        self.buttonGroup.addButton(self.buttonConnect2)
        self.buttonGroup.addButton(self.buttonConnect3)

        self.buttonConnect1.setCheckable(True)
        self.buttonConnect2.setCheckable(True)
        self.buttonConnect3.setCheckable(True)

        self.buttonConnect1.setChecked(True)

        self.buttonConnect1.setMaximumWidth(24)
        self.buttonConnect2.setMaximumWidth(24)
        self.buttonConnect3.setMaximumWidth(24)

        self.buttonConnect1.setToolTip("Flow through tee")
        self.buttonConnect2.setToolTip("Leave by connection")
        self.buttonConnect3.setToolTip("Arrive by connection")

        self.buttonConnect1.setIcon(QIcon(":/PipeCad/Resources/tee12-16.png"))
        self.buttonConnect2.setIcon(QIcon(":/PipeCad/Resources/tee13-16.png"))
        self.buttonConnect3.setIcon(QIcon(":/PipeCad/Resources/tee32-16.png"))

        self.buttonConnect1.clicked.connect(lambda: self.setArriveLeave(1, 2))
        self.buttonConnect2.clicked.connect(lambda: self.setArriveLeave(1, 3))
        self.buttonConnect3.clicked.connect(lambda: self.setArriveLeave(3, 1))

        self.horizontalSpacer = QSpacerItem(16, 16, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addWidget(self.labelConnectBore)
        self.horizontalLayout.addWidget(self.comboConnectBore)
        self.horizontalLayout.addWidget(self.buttonConnect1)
        self.horizontalLayout.addWidget(self.buttonConnect2)
        self.horizontalLayout.addWidget(self.buttonConnect3)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addWidget(self.connectionInfo)

        # Creation from
        self.horizontalLayout = QHBoxLayout()
        self.labelCreation = QLabel("Creation from ")
        self.labelCreation.setSizePolicy(aSizePolicy)
        self.textCreation = QLabel()
        self.horizontalLayout.addWidget(self.labelCreation)
        self.horizontalLayout.addWidget(self.textCreation)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.horizontalLine)

        self.horizontalLayout = QHBoxLayout()
        self.radioForwards = QRadioButton("Forwards")
        self.radioBackwards = QRadioButton("Backwards")
        self.radioForwards.setChecked(True)

        self.radioForwards.toggled.connect(self.currentItemChanged)
        self.radioBackwards.toggled.connect(self.currentItemChanged)

        self.horizontalLayout.addWidget(self.radioForwards)
        self.horizontalLayout.addWidget(self.radioBackwards)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.buttonConnect = QPushButton("Connect")
        self.buttonPlace = QPushButton("Place")
        self.buttonPlace.setToolTip("Place component in tube line")
        self.buttonFlip = QPushButton("Flip")

        self.buttonConnect.clicked.connect(self.connectComponent)
        self.buttonPlace.clicked.connect(self.placeComponent)
        self.buttonFlip.clicked.connect(self.flipComponent)

        self.horizontalLayout.addWidget(self.buttonConnect)
        self.horizontalLayout.addWidget(self.buttonPlace)
        self.horizontalLayout.addWidget(self.buttonFlip)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Location Tool.
        self.groupBox = QGroupBox("Location")
        self.formLayout = QFormLayout(self.groupBox)

        self.comboRotate = QComboBox()
        self.comboThrough = QComboBox()
        self.comboDistance = QComboBox()
        self.textDistance = QLineEdit("0")

        self.comboRotate.addItem("Rotate 30", 30)
        self.comboRotate.addItem("Rotate 45", 45)
        self.comboRotate.addItem("Rotate 90", 90)
        self.comboRotate.addItem("Rotate 180", 180)
        self.comboRotate.setMinimumWidth(100)
        self.comboRotate.activated.connect(self.rotateComponent)

        self.comboThrough.addItem("Thro CE")
        self.comboThrough.addItem("Thro Cursor")
        self.comboThrough.addItem("Thro Arrive")
        self.comboThrough.addItem("Thro Leave")
        self.comboThrough.activated.connect(self.throughComponent)

        # Select Spool - input an offset distance between opposing faces.
        # Select Distance - input an offset distance between component origins
        self.comboDistance.addItem("Spool")
        self.comboDistance.addItem("Distance")
        self.comboDistance.setMinimumWidth(100)
        self.comboDistance.activated.connect(self.moveComponent)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.comboRotate)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboThrough)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.comboDistance)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDistance)

        self.verticalLayout.addWidget(self.groupBox)

        self.dockWidget.setWidget(self.dockContent)
        PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

        # Set data.
        self.setBranch()
    # createComponent

    def currentItemChanged(self):
        self.currentItem = PipeCad.CurrentItem()

        aTagPosition = Position(0, 0, 0)
        aTagDirection = Direction(0, 0, 1)

        if self.currentItem.Type == "BRAN":
            if self.radioForwards.checked:
                self.ArriveBore = self.currentItem.Hbore
                aTagPosition = self.currentItem.Hposition
                aTagDirection = self.currentItem.Hdirection
            elif self.radioBackwards.checked:
                self.ArriveBore = self.currentItem.Tbore
                aTagPosition = self.currentItem.Tposition
                aTagDirection = self.currentItem.Tdirection
            # if
        elif self.currentItem.Owner.Type == "BRAN":
            if self.radioForwards.checked:
                aPoint = self.currentItem.LeavePoint
                if aPoint is not None:
                    self.ArriveBore = aPoint.Bore
                    aTagPosition = aPoint.Position
                    aTagDirection = aPoint.Direction
                # if
            elif self.radioBackwards.checked:
                aPoint = self.currentItem.ArrivePoint
                if aPoint is not None:
                    self.ArriveBore = aPoint.Bore
                    aTagPosition = aPoint.Position
                    aTagDirection = aPoint.Direction
                # if
            # if
        else:
            return
        # if

        self.textCreation.setText("<font color=Brown>" + self.currentItem.Name + "</font>")
        self.textBore.setText("<font color=Brown>" + self.ArriveBore + "</font>")

        # Tag position and direction.
        # print("Tag current position")
        aOffset = float(self.ArriveBore)
        aOrthDir = aTagDirection.Orthogonal()
        aPosition = aTagPosition.Offset(aOrthDir, aOffset)

        PipeCad.RemoveAid(self.tagId)
        PipeCad.AddAidText(aPosition, self.currentItem.Type, self.tagId)
        PipeCad.AddAidArrow(aPosition, aTagDirection, aOffset, 2, 0.4, self.tagId)
        PipeCad.AddAidCylinder(aPosition, aOrthDir.Reversed(), aOffset * 2, 2, self.tagId)
        PipeCad.UpdateViewer()
    # currentItemChanged

    def setBranch(self):
        self.branItem = None
        self.compItem = None

        aItem = PipeCad.CurrentItem()
        if aItem.Type == "BRAN":
            self.branItem = aItem
            if self.radioForwards.checked :
                self.ArriveBore = self.branItem.Hbore
            elif self.radioBackwards.checked:
                self.ArriveBore = self.branItem.Tbore
        elif aItem.Owner.Type == "BRAN":
            self.branItem = aItem.Owner
            self.compItem = aItem

            if self.radioForwards.checked:
                self.ArriveBore = aItem.LeavePoint.Bore
            elif self.radioBackwards.checked:
                self.ArriveBore = aItem.ArrivePoint.Bore
            # if
        # if

        if self.branItem is None:
            QMessageBox.warning(PipeCad, "", QT_TRANSLATE_NOOP("Design", "This command can only be used at a Branch or piping component."))
            return
        # if

        # Branch
        self.textBranch.setText("<font color=Brown>" + self.branItem.Name + "</font>")
        self.textSpec.setText("<font color=Brown>" + self.branItem.Pspec.Name + "</font>")
        self.textBore.setText("<font color=Brown>" + self.ArriveBore + "</font>")

        self.currentItem = PipeCad.CurrentItem()
        self.textCreation.setText("<font color=Brown>" + self.currentItem.Name + "</font>")

        # Mark head and tail.
        PipeCad.RemoveAid(self.branchTagId)
        PipeCad.AddAidText(self.branItem.Hposition, "Head", self.branchTagId)
        PipeCad.AddAidText(self.branItem.Tposition, "Tail", self.branchTagId)
        PipeCad.UpdateViewer()

        self.currentItemChanged()

        # Type
        self.comboType.clear()

        aSpecItem = self.branItem.Pspec
        if aSpecItem is not None:
            for aSeleItem in (aSpecItem.Member):
                aType = aSeleItem.Description
                if len(aType) > 0 :
                    self.comboType.addItem(aType, aSeleItem)
                # if
            # for
        # if

        # Sort type.
        self.comboType.model().sort(0, Qt.AscendingOrder)
    # setBranch

    def selectAltSpec(self):
        QMessageBox.information(PipeCad, "", "Select Alternative Spec")
    # selectAltSpec

    def typeChanged(self):
        self.reducerInfo.hide()
        self.connectionInfo.hide()

        self.comboLeaveBore.clear()
        self.comboConnectBore.clear()

        aSeleItem = self.comboType.currentData
        if aSeleItem is None:
            return
        # if

        self.comboFilter.clear()
        for aSubItem in (aSeleItem.Member):
            self.comboFilter.addItem(aSubItem.Purpose, aSubItem)

        aType = self.comboType.currentText
        if aType == "Reducer":
            self.reducerInfo.show()
        elif aType in ("Tee", "Olet"):
            self.connectionInfo.show()
        # if

    # typeChanged

    def subTypeChanged(self):
        self.Arrive = 1
        self.Leave = 2
        self.tableWidget.setRowCount(0)

        aSubItem = self.comboFilter.currentData
        if aSubItem is None:
            return

        aType = self.comboType.currentText

        for aSpcoItem in aSubItem.Member:
            if aSpcoItem.Answer == self.ArriveBore:
                aScomItem = aSpcoItem.Catref
                if aScomItem is not None:
                    aRow = self.tableWidget.rowCount
                    self.tableWidget.insertRow(aRow)

                    aParams = aScomItem.Param.split(" ")
                    aBore = aParams[0]
                    if aType == "Reducer":
                        aBore = aParams[1]
                        self.comboLeaveBore.addItem(aBore)
                    elif aType in ("Tee", "Olet"):
                        aBore = aParams[1]
                        self.comboConnectBore.addItem(aBore)
                    # if

                    # Save spco.
                    aSkeyItem = QTableWidgetItem(aBore)
                    aSkeyItem.setData(Qt.UserRole, aSpcoItem)

                    self.tableWidget.setItem(aRow, 0, aSkeyItem)
                    self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aSpcoItem.Dtxr))
                # if
            # if
        # for
    # subTypeChanged

    def setArriveLeave(self, theArrive, theLeave):
        self.Arrive = theArrive
        self.Leave = theLeave
        
        self.comboLeaveBore.clear()
        self.tableWidget.setRowCount(0)

        aSubItem = self.comboFilter.currentData
        if aSubItem is None:
            return

        aType = self.comboType.currentText

        for aSpcoItem in aSubItem.Member:
            aValid = False
            aScomItem = aSpcoItem.Catref
            aSdteItem = aSpcoItem.Detref
            if aSdteItem is not None and aScomItem is not None:

                if aType == "Reducer":
                    aParams = aScomItem.Param.split(" ")
                    aArriveBore = aParams[0]
                    aLeaveBore = aParams[1]
                    aBa = int(aArriveBore)
                    aBl = int(aLeaveBore)
                    aBore = aArriveBore

                    if theArrive == 1:
                        if aArriveBore == self.ArriveBore and aBl < aBa:
                            aBore = aLeaveBore
                            aValid = True
                        elif aLeaveBore == self.ArriveBore and aBa < aBl:
                            aBore = aArriveBore
                            aValid = True
                    else:
                        if aArriveBore == self.ArriveBore and aBl > aBa:
                            aBore = aLeaveBore
                            aValid = True
                        elif aLeaveBore == self.ArriveBore and aBa > aBl:
                            aBore = aArriveBore
                            aValid = True
                            
                elif aType == "Tee":
                    aParams = aScomItem.Param.split(" ")
                    aArriveBore = aParams[0]
                    aLeaveBore = aParams[1]

                    if theArrive == 3:
                        if aLeaveBore == self.ArriveBore:
                            aBore = aArriveBore
                            aValid = True
                    else:
                        if aArriveBore == self.ArriveBore:
                            aBore = aLeaveBore
                            aValid = True

                if aValid:
                    self.comboLeaveBore.addItem(aBore)

                    aRow = self.tableWidget.rowCount
                    self.tableWidget.insertRow(aRow)

                    # Save spco.
                    aSkeyItem = QTableWidgetItem(aBore)
                    aSkeyItem.setData(Qt.UserRole, aSpcoItem)

                    self.tableWidget.setItem(aRow, 0, aSkeyItem)
                    self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aSdteItem.Rtext))
    # setArriveLeave

    def findTubeSpco(self, theBore):
        aSpecItem = self.branItem.Pspec
        if self.checkBoxSpec.checked:
            aSpecItem = self.altSpec

        if aSpecItem is None:
            return aSpecItem

        aTubeSele = None
        for aSeleItem in (aSpecItem.Member):
            aType = aSeleItem.Answer
            if aType == "TUBE":
                aTubeSele = aSeleItem
                break

        if aTubeSele is None:
            return None

        aSpcoList = PipeCad.CollectItem("SPCO", aTubeSele)
        for aSpcoItem in aSpcoList:
            if aSpcoItem.Answer == theBore:
                return aSpcoItem

    # findTubeSpco

    def connectComponent(self):
        aTypeItem = self.comboType.currentData
        if aTypeItem is None:
            return
        # if

        aRow = self.tableWidget.currentRow()
        aSpcoItem = self.tableWidget.item(aRow, 0).data(Qt.UserRole)

        aPoint = None
        if self.radioForwards.checked:
            if self.currentItem.Type == "BRAN":
                aPoint = self.currentItem.Hpoint
            else:
                aPoint = self.currentItem.LeavePoint

            PipeCad.SetCurrentItem(self.currentItem)
        else:
            if self.currentItem.Type == "BRAN":
                aPoint = self.currentItem.Tpoint
                aMemberList = self.currentItem.Member
                if len(aMemberList) > 0:
                    PipeCad.SetCurrentItem(aMemberList[-1])
                else:
                    PipeCad.SetCurrentItem(self.currentItem)
                # if
            else:
                aPoint = self.currentItem.ArrivePoint
                aIndex = self.currentItem.Index - 1
                if aIndex >= 0:
                    PipeCad.SetCurrentItem(self.currentItem.Owner.Member[aIndex])
                else:
                    PipeCad.SetCurrentItem(self.currentItem.Owner)
                # if
            # if
        # if

        PipeCad.StartTransaction("Create Commponent")
        PipeCad.CreateItem(aTypeItem.Answer)
        aCompItem = PipeCad.CurrentItem()
        aCompItem.Spref = aSpcoItem
        aCompItem.Arrive = self.Arrive
        aCompItem.Leave = self.Leave
        aCompItem.Lstube = self.findTubeSpco(aCompItem.LeavePoint.Bore)
        aCompItem.Connect(aPoint)

        # Transpose Arrive/Leave if flow is backwards
        if self.radioBackwards.checked:
            aCompItem.Arrive = self.Leave
            aCompItem.Leave = self.Arrive
            aCompItem.Owner.updateTubi()
        # if

        PipeCad.CommitTransaction()

        self.currentItemChanged()
    # connectComponent

    def placeComponent(self):
        pass
    # placeComponent

    def flipComponent(self):
        aCompItem = PipeCad.CurrentItem()
        aCompItem.Flip()
    # flipComponent

    def rotateComponent(self):
        aAngle = self.comboRotate.currentData

        if self.radioForwards.checked:
            PipeCad.Rotate(self.currentItem.ArrivePoint, aAngle)
        else:
            PipeCad.Rotate(self.currentItem.LeavePoint, aAngle)
        # if
    # rotateComponent

    def moveComponent(self):
        aOffset = float(self.textDistance.text)
        aIndex = self.comboDistance.currentIndex
        if aIndex == 0:
            # Spool: offset distance between opposing faces.
            aSequence = self.currentItem.Sequence - 1
            if aSequence >= 0:
                aPrev = self.branItem.Member[aSequence]
                aPs = aPrev.LeavePoint.Position
                aDir = aPrev.LeavePoint.Direction
            else:
                aPs = self.branItem.Hposition
                aDir = self.branItem.Hdirection
            # if

            aPa = self.currentItem.ArrivePoint.Position
            aPc = self.currentItem.Position
            aOffset += aPc.Distance(aPa)

            PipeCad.Translate(aPs, aDir, aOffset)
        else:
            # Distance: offset distance between component origins
            aSequence = self.currentItem.Sequence - 1
            if aSequence >= 0:
                aPrev = self.branItem.Member[aSequence]
                aPs = aPrev.Position
                aDir = aPrev.LeavePoint.Direction
            else:
                aPs = self.branItem.Hposition
                aDir = self.branItem.Hdirection

            PipeCad.Translate(aPs, aDir, aOffset)
    # moveComponent

    def throughComponent(self):
        aCompItem = PipeCad.CurrentItem()
        if aCompItem.Owner.Type != "BRAN":
            return

        aPickItem = PipeCad.PickItem()
        if aPickItem is None:
            return
        # if

        aType = self.comboThrough.currentText
        if aType == "Thro Arrive":
            aCompItem.through(aCompItem.ArrivePoint, aPickItem)
        elif aType == "Thro Leave":
            aCompItem.through(aCompItem.LeavePoint, aPickItem)
        # if
    # throughComponent

    def modifyComponent(self):
        pass
    # modifyComponent

# Create Dialog.
aComponentDlg = ComponentDialog(PipeCad)

def Create():
    aComponentDlg.createComponent()
# CreateComponent

def Modify():
    aComponentDlg.modifyComponent()
# ModifyComponent