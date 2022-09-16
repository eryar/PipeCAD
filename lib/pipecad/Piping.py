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
# Date: 13:06 2021-09-25

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *

class PipeDialog():
    def __init__(self, parent = None):
        self.dockWidget = QDockWidget()
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidget.visibilityChanged.connect(self.visibilityChanged)

        self.pipeItem = None
        self.branItem = None
    # __init__

    def visibilityChanged(self, theVisibility):
        if not theVisibility:
            PipeCad.removeDockWidget(self.dockWidget)
        # if
    # visibilityChanged

    def createPipe(self):
        aToggleAction = self.dockWidget.toggleViewAction()
        aToggleAction.setText("Create Pipe")

        self.dockWidget.setWindowTitle("Create Pipe")
        self.dockWidget.show()

        self.dockContent = QWidget()
        PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

        self.verticalLayout = QVBoxLayout(self.dockContent)

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel()
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelName = QLabel("Pipe Name")
        self.textName = QLineEdit()
        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Pipe spec.
        self.labelSpec = QLabel("Select Pipe Specification")
        self.verticalLayout.addWidget(self.labelSpec)

        self.listWidget = QListWidget()
        self.listWidget.setAlternatingRowColors(True)

        aSpecItems = PipeCad.CollectItem("SPEC")
        aSpecList = list(x for x in aSpecItems if x.Purpose == "PIPE")
        for aSpecItem in aSpecList:
            aListItem = QListWidgetItem(aSpecItem.Name)
            aListItem.setData(Qt.UserRole, aSpecItem)
            self.listWidget.addItem(aListItem)
        # for

        self.listWidget.currentRowChanged.connect(self.specChanged)
        self.verticalLayout.addWidget(self.listWidget)

        # Basic Pipe Process Data.
        self.labelSpec = QLabel("Basic Pipe Process Data")
        self.verticalLayout.addWidget(self.labelSpec)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        self.formLayout = QFormLayout()

        self.labelBore = QLabel("Bore")
        self.comboBore = QComboBox()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelBore)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBore)

        self.labelInsu = QLabel("Insulation")
        self.comboInsu = QComboBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelInsu)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboInsu)

        self.labelTracing = QLabel("Tracing")
        self.comboTracing = QComboBox()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelTracing)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboTracing)

        self.labelTemp = QLabel("Temperature")
        self.lineTemp = QLineEdit("-10000.00")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelTemp)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineTemp)

        self.labelPressure = QLabel("Pressure")
        self.linePressure = QLineEdit("0.00")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelPressure)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.linePressure)

        self.verticalLayout.addLayout(self.formLayout)

        # Button box.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

        self.dockWidget.setWidget(self.dockContent)

        # Populate pipe data.
        if self.pipeItem is not None:
            self.textName.setText(self.pipeItem.Name)
            aItemList = self.listWidget.findItems(self.pipeItem.Pspec, Qt.MatchExactly)
            if len(aItemList) > 0:
                self.listWidget.setCurrentItem(aItemList[0])
            self.comboBore.setCurrentText(self.pipeItem.Bore)
        else:
            self.listWidget.setCurrentRow(0)
        # if
    # setupUi

    def modifyPipe(self, thePipeItem):
        aToggleAction = self.dockWidget.toggleViewAction()
        aToggleAction.setText("Modify Pipe")

        self.dockWidget.setWindowTitle("Modify Pipe")
        self.dockWidget.show()

        self.pipeItem = thePipeItem

        self.dockContent = QWidget()
        PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
        
        self.verticalLayout = QVBoxLayout(self.dockContent)

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel("<font color=Brown>" + thePipeItem.Name + "</font>")
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe spec
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel("<font color=Brown>" + thePipeItem.Pspec.Name + "</font>")
        self.buttonSpec = QPushButton("Set Detail")
        self.buttonSpec.setSizePolicy(aSizePolicy)
        self.buttonSpec.clicked.connect(self.createPipe)

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Table.
        aMember = thePipeItem.Member
        self.tableWidgetBranch = QTableWidget()
        self.tableWidgetBranch.setColumnCount(3)
        self.tableWidgetBranch.setRowCount(len(aMember))
        aHeaderItem = QTableWidgetItem("Branch")
        self.tableWidgetBranch.setHorizontalHeaderItem(0, aHeaderItem)
        aHeaderItem = QTableWidgetItem("Head")
        self.tableWidgetBranch.setHorizontalHeaderItem(1, aHeaderItem)
        aHeaderItem = QTableWidgetItem("Tail")
        self.tableWidgetBranch.setHorizontalHeaderItem(2, aHeaderItem)
        self.tableWidgetBranch.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetBranch.setAlternatingRowColors(True)
        self.tableWidgetBranch.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidgetBranch.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetBranch.setGridStyle(Qt.SolidLine)
        self.tableWidgetBranch.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetBranch.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidgetBranch.verticalHeader().setMinimumSectionSize(16)
        self.tableWidgetBranch.verticalHeader().setDefaultSectionSize(18)
        self.tableWidgetBranch.verticalHeader().hide() 

        for i in range (len(aMember)):
            aBranItem = aMember[i]
            self.tableWidgetBranch.setItem(i, 0, QTableWidgetItem(aBranItem.Name))
            if aBranItem.Href is not None:
                self.tableWidgetBranch.setItem(i, 1, QTableWidgetItem(aBranItem.Href.Name))
            else:
                self.tableWidgetBranch.setItem(i, 1, QTableWidgetItem("Undefined"))
            # if

            if aBranItem.Tref is not None:
                self.tableWidgetBranch.setItem(i, 2, QTableWidgetItem(aBranItem.Tref.Name))
            else:
                self.tableWidgetBranch.setItem(i, 2, QTableWidgetItem("Undefined"))
            # if
        # for

        self.tableWidgetBranch.itemSelectionChanged.connect(self.currentBranchChanged)
        self.verticalLayout.addWidget(self.tableWidgetBranch)

        # New Branch.
        self.horizontalLayout = QHBoxLayout()
        self.buttonBranch = QPushButton("New Branch")
        self.buttonBranch.clicked.connect(self.createBranch)
        self.horizontalLayout.addWidget(self.buttonBranch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Current Branch
        self.horizontalLayout = QHBoxLayout()
        self.labelBranch = QLabel("Branch: ")
        self.labelBranch.setSizePolicy(aSizePolicy)
        self.textBranch = QLabel()
        self.horizontalLayout.addWidget(self.labelBranch)
        self.horizontalLayout.addWidget(self.textBranch)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lineBranchDetail = QFrame()
        self.lineBranchDetail.setFrameShape(QFrame.HLine)
        self.lineBranchDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.lineBranchDetail)

        # Branch spec
        self.horizontalLayout = QHBoxLayout()
        self.labelBranchSpec = QLabel("Spec: ")
        self.labelBranchSpec.setSizePolicy(aSizePolicy)
        self.textBranchSpec = QLabel()
        self.buttonBranchSpec = QPushButton("Set Detail")
        self.buttonBranchSpec.setSizePolicy(aSizePolicy)
        self.buttonBranchSpec.clicked.connect(self.setBranchSpec)

        self.horizontalLayout.addWidget(self.labelBranchSpec)
        self.horizontalLayout.addWidget(self.textBranchSpec)
        self.horizontalLayout.addWidget(self.buttonBranchSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Head Detail
        self.lableHeadDetail = QLabel("Head Detail: ")
        self.lineHeadDetail = QFrame()
        self.lineHeadDetail.setFrameShape(QFrame.HLine)
        self.lineHeadDetail.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.lableHeadDetail)
        self.verticalLayout.addWidget(self.lineHeadDetail)

        self.horizontalLayout = QHBoxLayout()
        self.labelHeadBore = QLabel("Bore: ")
        self.labelHeadBore.setSizePolicy(aSizePolicy)
        self.textHeadBore = QLabel("")
        self.labelHeadType = QLabel("Connection Type: ")
        self.labelHeadType.setSizePolicy(aSizePolicy)
        self.textHeadType = QLabel("")
        self.horizontalLayout.addWidget(self.labelHeadBore)
        self.horizontalLayout.addWidget(self.textHeadBore)
        self.horizontalLayout.addWidget(self.labelHeadType)
        self.horizontalLayout.addWidget(self.textHeadType)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.labelHeadDirection = QLabel("Direction: ")
        self.labelHeadDirection.setSizePolicy(aSizePolicy)
        self.textHeadDirection = QLabel("")
        self.horizontalLayout.addWidget(self.labelHeadDirection)
        self.horizontalLayout.addWidget(self.textHeadDirection)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.labelHeadPosition = QLabel("Position: ")
        self.labelHeadPosition.setSizePolicy(aSizePolicy)
        self.textHeadPosition = QLabel("")
        self.horizontalLayout.addWidget(self.labelHeadPosition)
        self.horizontalLayout.addWidget(self.textHeadPosition)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonChangeHead = QPushButton("Change")
        self.buttonChangeHead.setSizePolicy(aSizePolicy)
        self.buttonChangeHead.clicked.connect(self.changeHeadDetail)
        self.horizontalLayout.addWidget(self.buttonChangeHead)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Head Connection
        self.labelHeadConnection = QLabel("Head Connection:")
        self.lineHeadConnection = QFrame()
        self.lineHeadConnection.setFrameShape(QFrame.HLine)
        self.lineHeadConnection.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.labelHeadConnection)
        self.verticalLayout.addWidget(self.lineHeadConnection)

        self.horizontalLayout = QHBoxLayout()
        self.textHeadConnection = QLabel("Undefined")
        self.buttonHeadConnection = QPushButton("Change")
        self.buttonHeadConnection.clicked.connect(self.changeHeadConnection)
        self.buttonHeadConnection.setSizePolicy(aSizePolicy)
        self.horizontalLayout.addWidget(self.textHeadConnection)
        self.horizontalLayout.addWidget(self.buttonHeadConnection)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Tail Detail
        self.lableTailDetail = QLabel("Tail Detail: ")
        self.lineTailDetail = QFrame()
        self.lineTailDetail.setFrameShape(QFrame.HLine)
        self.lineTailDetail.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.lableTailDetail)
        self.verticalLayout.addWidget(self.lineTailDetail)

        self.horizontalLayout = QHBoxLayout()
        self.labelTailBore = QLabel("Bore: ")
        self.textTailBore = QLabel("")
        self.labelTailType = QLabel("Connection Type: ")
        self.textTailType = QLabel("")
        self.horizontalLayout.addWidget(self.labelTailBore)
        self.horizontalLayout.addWidget(self.textTailBore)
        self.horizontalLayout.addWidget(self.labelTailType)
        self.horizontalLayout.addWidget(self.textTailType)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.labelTailDirection = QLabel("Direction: ")
        self.labelTailDirection.setSizePolicy(aSizePolicy)
        self.textTailDirection = QLabel("")
        self.horizontalLayout.addWidget(self.labelTailDirection)
        self.horizontalLayout.addWidget(self.textTailDirection)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.labelTailPosition = QLabel("Position: ")
        self.labelTailPosition.setSizePolicy(aSizePolicy)
        self.textTailPosition = QLabel("")
        self.horizontalLayout.addWidget(self.labelTailPosition)
        self.horizontalLayout.addWidget(self.textTailPosition)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonChangeTail = QPushButton("Change")
        self.buttonChangeTail.setSizePolicy(aSizePolicy)
        self.buttonChangeTail.clicked.connect(self.changeTailDetail)
        self.horizontalLayout.addWidget(self.buttonChangeTail)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Tail Connection
        self.labelTailConnection = QLabel("Tail Connection:")
        self.lineTailConnection = QFrame()
        self.lineTailConnection.setFrameShape(QFrame.HLine)
        self.lineTailConnection.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.labelTailConnection)
        self.verticalLayout.addWidget(self.lineTailConnection)

        self.horizontalLayout = QHBoxLayout()
        self.textTailConnection = QLabel("Undefined")
        self.buttonTailConnection = QPushButton("Change")
        self.buttonTailConnection.setSizePolicy(aSizePolicy)
        self.buttonTailConnection.clicked.connect(self.changeTailConnection)
        self.horizontalLayout.addWidget(self.textTailConnection)
        self.horizontalLayout.addWidget(self.buttonTailConnection)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.dockWidget.setWidget(self.dockContent)

        # Set current branch.
        if self.branItem is not None:
            self.setCurrentBranch(self.branItem)
        else:
            self.tableWidgetBranch.setCurrentCell(0, 0)
    # modifyPipe

    def specChanged(self, theRow):

        self.comboBore.clear()

        aSpecItem = self.listWidget.currentItem().data(Qt.UserRole)
        if aSpecItem is None:
            return

        aSpcoList = PipeCad.CollectItem("SPCO", aSpecItem)

        aBoreDict = dict()

        for aSpcoItem in aSpcoList:
            aScomItem = aSpcoItem.Catref
            if aScomItem is not None and aSpcoItem.Owner.Purpose == "TUBE":
                aParams = aScomItem.Param.split()
                aBoreDict[int(aParams[0])] = aSpcoItem
            # if
        # for

        for aBore in sorted(aBoreDict):
            self.comboBore.addItem(aBore, aBoreDict[aBore])
        # for

    # specChanged

    #def show(self):
        #PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
        #self.dockWidget.show()

    def setPipe(self):
        aPipeItem = PipeCad.CurrentItem()
        self.modifyPipe(aPipeItem)
    # setPipe

    def createBranch(self):
        aCurrentItem = self.pipeItem

        # Generate branch name.
        aMemberList = self.pipeItem.Member
        aMemberSize = len(aMemberList)
        if aMemberSize > 0:
            aCurrentItem = aMemberList[-1]
        # if

        aBranchName = ""
        if len(self.pipeItem.Name) > 0:
            aBranchName = self.pipeItem.Name + "-B" + str(aMemberSize + 1)
        # if

        try:
            # Set hstube for create pipe.
            aHstube = self.comboBore.currentData
        except Exception as e:
            # Ignore hstube for modify pipe.
            aHstube = None
        # try

        PipeCad.SetCurrentItem(aCurrentItem)
        PipeCad.StartTransaction("Create Branch")
        PipeCad.CreateItem("BRAN", aBranchName)

        self.branItem = PipeCad.CurrentItem()
        self.branItem.Pspec = self.pipeItem.Pspec
        self.branItem.Hbore = self.pipeItem.Bore
        self.branItem.Tbore = self.pipeItem.Bore

        if aHstube is not None:
            self.branItem.Hstube = aHstube
        # if

        PipeCad.CommitTransaction()

        self.modifyPipe(self.pipeItem)
    # createBranch

    def currentBranchChanged(self):
        aIndex = self.tableWidgetBranch.currentRow()
        aBranItem = self.pipeItem.Member[aIndex]
        self.setCurrentBranch(aBranItem)

    def setCurrentBranch(self, theBranItem):
        self.branItem = theBranItem

        self.textBranch.setText("<font color=Brown>" + theBranItem.Name + "</font>")
        self.textBranchSpec.setText("<font color=Brown>" + theBranItem.Pspec.Name + "</font>")

        # Head Detail
        self.textHeadBore.setText("<font color=Brown>" + theBranItem.Hbore + "</font>")
        self.textHeadType.setText("<font color=Brown>" + theBranItem.Hconnect + "</font>")
        self.textHeadDirection.setText("<font color=Brown>" + theBranItem.Hdirection.string() + "</font>")
        self.textHeadPosition.setText("<font color=Brown>" + theBranItem.Hposition.string() + "</font>")

        if theBranItem.Href is not None:
            self.textHeadConnection.setText("<font color=Brown>" + theBranItem.Href.Name + "</font>")
        else:
            self.textHeadConnection.setText("Undefined")
        # if

        # Tail Detail.
        self.textTailBore.setText("<font color=Brown>" + theBranItem.Tbore + "</font>")
        self.textTailType.setText("<font color=Brown>" + theBranItem.Tconnect + "</font>")
        self.textTailDirection.setText("<font color=Brown>" + theBranItem.Tdirection.string() + "</font>")
        self.textTailPosition.setText("<font color=Brown>" + theBranItem.Tposition.string() + "</font>")

        if theBranItem.Tref is not None:
            self.textTailConnection.setText("<font color=Brown>" + theBranItem.Tref.Name + "</font>")
        else:
            self.textTailConnection.setText("Undefined")
        # if
    # setCurrentBranch

    def setBranchSpec(self):
        self.dockContent = QWidget()

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.verticalLayout = QVBoxLayout(self.dockContent)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel(self.pipeItem.Name)
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe spec
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel("")
        if self.pipeItem.Pspec is not None:
            self.textSpec.setText(self.pipeItem.Pspec.Name)
        # if
        self.buttonSpec = QPushButton("Set Detail")
        self.buttonSpec.setSizePolicy(aSizePolicy)
        self.buttonSpec.clicked.connect(self.createPipe)

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)        

        # Branch Table.
        self.verticalLayout.addWidget(self.tableWidgetBranch)

        # New Branch.
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.buttonBranch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Detail
        self.labelBranch = QLabel("Branch: ")
        self.verticalLayout.addWidget(self.labelBranch)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Branch name
        self.horizontalLayout = QHBoxLayout()
        self.labelName = QLabel("Branch Name")
        self.textName = QLineEdit()
        self.horizontalLayout.addWidget(self.labelName)
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Spec
        self.labelSpec = QLabel("Select Branch Specification")
        self.verticalLayout.addWidget(self.labelSpec)

        self.listWidget = QListWidget()
        self.listWidget.setAlternatingRowColors(True)

        aSpecItems = PipeCad.CollectItem("SPEC")
        aSpecList = list(x for x in aSpecItems if x.Purpose == "PIPE")
        for aSpecItem in aSpecList:
            self.listWidget.addItem(aSpecItem.Name)
        # for

        self.listWidget.currentRowChanged.connect(self.specChanged)
        self.verticalLayout.addWidget(self.listWidget)

        # Basic Branch Process Data.
        self.labelSpec = QLabel("Basic Branch Process Data")
        self.verticalLayout.addWidget(self.labelSpec)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        self.formLayout = QFormLayout()

        self.comboBore = QComboBox()

        self.labelInsu = QLabel("Insulation")
        self.comboInsu = QComboBox()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelInsu)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboInsu)

        self.labelTracing = QLabel("Tracing")
        self.comboTracing = QComboBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelTracing)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboTracing)

        self.labelTemp = QLabel("Temperature")
        self.lineTemp = QLineEdit("-10000.00")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelTemp)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineTemp)

        self.labelPressure = QLabel("Pressure")
        self.linePressure = QLineEdit("0.00")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelPressure)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.linePressure)

        self.verticalLayout.addLayout(self.formLayout)

        # Button box.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.acceptBranch)
        self.buttonBox.rejected.connect(self.rejectBranch)

        self.verticalLayout.addWidget(self.buttonBox)

        self.dockWidget.setWidget(self.dockContent)

        # Populate Branch Data.
        if self.branItem is not None:
            self.textName.setText(self.branItem.Name)

            if self.branItem.Pspec is not None:
                aItemList = self.listWidget.findItems(self.branItem.Pspec.Name, Qt.MatchExactly)
                if len(aItemList) > 0:
                    self.listWidget.setCurrentItem(aItemList[0])
                # if
            # if
        else:
            self.listWidget.setCurrentRow(0)


    def changeHeadDetail(self):
        self.dockContent = QWidget()

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.verticalLayout = QVBoxLayout(self.dockContent)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel(self.pipeItem.Name)
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe spec
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel(self.pipeItem.Pspec.Name)
        self.buttonSpec = QPushButton("Set Detail")
        self.buttonSpec.setSizePolicy(aSizePolicy)
        self.buttonSpec.clicked.connect(self.createPipe)

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)        

        # Branch Table.
        self.verticalLayout.addWidget(self.tableWidgetBranch)

        # New Branch.
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.buttonBranch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Detail
        self.labelSpec = QLabel("Modify Branch Head: ")
        self.verticalLayout.addWidget(self.labelSpec)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        self.formLayout = QFormLayout()

        self.labelBore = QLabel("Bore:")
        self.comboBore = QComboBox()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelBore)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBore)

        self.labelConnection = QLabel("Connection:")
        self.comboConnection = QComboBox()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelConnection)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboConnection)

        self.labelDirection = QLabel("Direction")
        self.textDirection = QLineEdit("1 0 0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelDirection)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textDirection)

        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.labelPosition = QLabel("Position wrt World:")
        self.buttonPick = QPushButton("Pick")
        self.buttonPick.setSizePolicy(aSizePolicy)
        self.buttonPick.clicked.connect(self.pickHeadPosition)
        self.horizontalLayout.addWidget(self.labelPosition)
        self.horizontalLayout.addWidget(self.buttonPick)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Position
        self.formLayout = QFormLayout()
        self.labelX = QLabel("Position X:")
        self.textX = QLineEdit("0")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelX)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textX)

        self.labelY = QLabel("Position Y:")
        self.textY = QLineEdit("0")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelY)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textY)

        self.labelZ = QLabel("Position Z:")
        self.textZ = QLineEdit("0")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelZ)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textZ)

        self.verticalLayout.addLayout(self.formLayout)

        # Button box.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.acceptHeadDetail)
        self.buttonBox.rejected.connect(self.rejectBranch)

        self.verticalLayout.addWidget(self.buttonBox)

        self.dockWidget.setWidget(self.dockContent)

        # Populate Branch Head Data.
        if self.branItem is not None:

            aSpecItem = self.branItem.Pspec
            if aSpecItem is not None:
                aSpcoList = PipeCad.CollectItem("SPCO", aSpecItem)

                aBoreDict = dict()

                for aSpcoItem in aSpcoList:
                    aScomItem = aSpcoItem.Catref
                    if aScomItem is not None and aSpcoItem.Owner.Purpose == "TUBE":
                        aParams = aScomItem.Param.split()
                        aBoreDict[int(aParams[0])] = aSpcoItem

                for aBore in sorted(aBoreDict):
                    self.comboBore.addItem(aBore, aBoreDict[aBore])
                # for
            # if

            self.comboConnection.addItem(self.branItem.Hconnect)
            self.comboConnection.addItem(self.branItem.Tconnect)

            self.comboBore.setCurrentText(self.branItem.Hbore)
            self.comboConnection.setCurrentText(self.branItem.Hconnect)
            self.textDirection.setText(self.branItem.Hdirection.string())

            aPos = self.branItem.Hposition.string().split()
            self.textX.setText(aPos[0])
            self.textY.setText(aPos[1])
            self.textZ.setText(aPos[2])
    # changeHeadDetail

    def pickHeadPosition(self):
        aPoint = PipeCad.PickPoint("Pick position for branch head, press ESC to cancel")
        if aPoint is None:
            return
        # if

        self.textX.setText(str(aPoint.X))
        self.textY.setText(str(aPoint.Y))
        self.textZ.setText(str(aPoint.Z))
    # pickHeadPosition

    def changeHeadConnection(self):
        self.dockContent = QWidget()

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.verticalLayout = QVBoxLayout(self.dockContent)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel(self.pipeItem.Name)
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe spec
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel(self.pipeItem.Pspec.Name)
        self.buttonSpec = QPushButton("Set Detail")
        self.buttonSpec.setSizePolicy(aSizePolicy)
        self.buttonSpec.clicked.connect(self.createPipe)

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)        

        # Branch Table.
        self.verticalLayout.addWidget(self.tableWidgetBranch)

        # New Branch.
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.buttonBranch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Head Connection
        self.labelSpec = QLabel("Connect Branch Head To: ")
        self.verticalLayout.addWidget(self.labelSpec)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        if self.branItem.Href is not None:
            self.labelConnection = QLabel("")
            if self.branItem.Href is not None:
                self.labelConnection.setText(self.branItem.Href.Name)
            # if
            self.verticalLayout.addWidget(self.labelConnection)

            self.horizontalLayout = QHBoxLayout()
            self.buttonDisconnect = QPushButton("Disconnect")
            self.buttonReconnect = QPushButton("Reconnect")
            self.buttonBack = QPushButton("Back")
            self.buttonBack.clicked.connect(self.rejectBranch)
            self.horizontalLayout.addWidget(self.buttonDisconnect)
            self.horizontalLayout.addWidget(self.buttonReconnect)
            self.horizontalLayout.addWidget(self.buttonBack)

            self.verticalLayout.addLayout(self.horizontalLayout)
        else:
            self.tableWidgetConnection = QTableWidget()
            self.tableWidgetConnection.setColumnCount(4)

            self.tableWidgetConnection.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
            self.tableWidgetConnection.setHorizontalHeaderItem(1, QTableWidgetItem("Bore"))
            self.tableWidgetConnection.setHorizontalHeaderItem(2, QTableWidgetItem("Type"))
            self.tableWidgetConnection.setHorizontalHeaderItem(3, QTableWidgetItem("Connection"))

            self.tableWidgetConnection.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidgetConnection.setAlternatingRowColors(True)
            self.tableWidgetConnection.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.tableWidgetConnection.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tableWidgetConnection.setGridStyle(Qt.SolidLine)
            self.tableWidgetConnection.horizontalHeader().setStretchLastSection(True)
            self.tableWidgetConnection.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tableWidgetConnection.verticalHeader().setMinimumSectionSize(16)
            self.tableWidgetConnection.verticalHeader().setDefaultSectionSize(18)
            self.tableWidgetConnection.verticalHeader().hide()
            self.tableWidgetConnection.itemSelectionChanged.connect(self.connectionChanged)

            self.verticalLayout.addWidget(self.tableWidgetConnection)

            self.horizontalLayout = QHBoxLayout()

            self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.horizontalLayout.addItem(self.horizontalSpacer)

            self.buttonHeadPick = QPushButton("Pick")
            self.buttonHeadPick.clicked.connect(self.pickConnection)

            self.buttonConnect = QPushButton("Connect")
            self.buttonBack = QPushButton("Back")
            self.buttonConnect.clicked.connect(self.connectHead)
            self.buttonBack.clicked.connect(self.rejectBranch)

            self.horizontalLayout.addWidget(self.buttonHeadPick)
            self.horizontalLayout.addWidget(self.buttonConnect)
            self.horizontalLayout.addWidget(self.buttonBack)

            self.verticalLayout.addLayout(self.horizontalLayout)

        self.dockWidget.setWidget(self.dockContent)
    # changeHeadConnection

    def pickConnection(self):
        aPickItem = PipeCad.PickItem()
        if aPickItem is None:
            return
        # if

        if aPickItem.Type == "NOZZ":
            aPoint = aPickItem.linkPoint("P1")

            aTableItem = QTableWidgetItem(aPickItem.Name)
            aTableItem.setData(Qt.UserRole, aPickItem)

            aPointItem = QTableWidgetItem(aPoint.Bore)
            aPointItem.setData(Qt.UserRole, aPoint)

            self.tableWidgetConnection.setRowCount(1)
            self.tableWidgetConnection.setItem(0, 0, aTableItem)
            self.tableWidgetConnection.setItem(0, 1, aPointItem)
            self.tableWidgetConnection.setItem(0, 2, QTableWidgetItem(aPoint.Type))
            self.tableWidgetConnection.setItem(0, 3, QTableWidgetItem(""))
            self.tableWidgetConnection.setCurrentCell(0, 0)
        elif aPickItem.Type in ("TEE", "OLET"):
            aIndex = 6 - aPickItem.Arrive- aPickItem.Leave
            aPoint = aPickItem.linkPoint("P" + str(aIndex))

            aPickName = aPickItem.Name
            if len(aPickName) < 1:
                aPickName = aPickItem.RefNo
            # if

            aTableItem = QTableWidgetItem(aPickName)
            aTableItem.setData(Qt.UserRole, aPickItem)

            aPointItem = QTableWidgetItem(aPoint.Bore)
            aPointItem.setData(Qt.UserRole, aPoint)

            self.tableWidgetConnection.setRowCount(1)
            self.tableWidgetConnection.setItem(0, 0, aTableItem)
            self.tableWidgetConnection.setItem(0, 1, aPointItem)
            self.tableWidgetConnection.setItem(0, 2, QTableWidgetItem(aPoint.Type))
            self.tableWidgetConnection.setItem(0, 3, QTableWidgetItem(""))
            self.tableWidgetConnection.setCurrentCell(0, 0)
        # if

    # pickConnection

    def connectionChanged(self):
        pass

    def connectHead(self):
        aRow = self.tableWidgetConnection.currentRow()
        aPoint = self.tableWidgetConnection.item(aRow, 1).data(Qt.UserRole)

        # Set Hstube.
        aHstube = None
        aSpecItem = self.branItem.Pspec
        if aSpecItem is not None:
            aSpcoList = PipeCad.CollectItem("SPCO", aSpecItem)

            for aSpcoItem in aSpcoList:
                aScomItem = aSpcoItem.Catref
                if aScomItem is not None and aSpcoItem.Owner.Purpose == "TUBE":
                    aParams = aScomItem.Param.split()
                    if aParams[0] == aPoint.Bore:
                        aHstube = aSpcoItem
                    # if
                # if
            # for
        # if

        PipeCad.StartTransaction("Set Head Connection")
        self.branItem.Hposition = aPoint.Position
        self.branItem.Hdirection = aPoint.Direction
        self.branItem.Href = self.tableWidgetConnection.item(aRow, 0).data(Qt.UserRole)
        self.branItem.Hbore = aPoint.Bore
        self.branItem.Hconnect = self.tableWidgetConnection.item(aRow, 2).text()
        if aHstube is not None:
            self.branItem.Hstube = aHstube
        # if
        PipeCad.CommitTransaction()

        self.rejectBranch()

    def changeTailDetail(self):
        self.dockContent = QWidget()

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.verticalLayout = QVBoxLayout(self.dockContent)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel(self.pipeItem.Name)
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe spec
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel(self.pipeItem.Pspec.Name)
        self.buttonSpec = QPushButton("Set Detail")
        self.buttonSpec.setSizePolicy(aSizePolicy)
        self.buttonSpec.clicked.connect(self.createPipe)

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)        

        # Branch Table.
        self.verticalLayout.addWidget(self.tableWidgetBranch)

        # New Branch.
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.buttonBranch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Detail
        self.labelSpec = QLabel("Modify Branch Head: ")
        self.verticalLayout.addWidget(self.labelSpec)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        self.formLayout = QFormLayout()

        self.labelBore = QLabel("Bore:")
        self.comboBore = QComboBox()

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelBore)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBore)

        self.labelConnection = QLabel("Connection:")
        self.comboConnection = QComboBox()
        self.comboConnection.setDuplicatesEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelConnection)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboConnection)

        self.labelDirection = QLabel("Direction")
        self.textDirection = QLineEdit("1 0 0")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelDirection)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textDirection)

        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.labelPosition = QLabel("Position wrt World:")
        self.buttonPick = QPushButton("Pick")
        self.buttonPick.setSizePolicy(aSizePolicy)
        self.buttonPick.clicked.connect(self.pickTailPosition)
        self.horizontalLayout.addWidget(self.labelPosition)
        self.horizontalLayout.addWidget(self.buttonPick)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Position
        self.formLayout = QFormLayout()
        self.labelX = QLabel("Position X:")
        self.textX = QLineEdit("0")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelX)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textX)

        self.labelY = QLabel("Position Y:")
        self.textY = QLineEdit("0")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelY)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textY)

        self.labelZ = QLabel("Position Z:")
        self.textZ = QLineEdit("0")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelZ)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textZ)

        self.verticalLayout.addLayout(self.formLayout)

        # Button box.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.acceptTailDetail)
        self.buttonBox.rejected.connect(self.rejectBranch)

        self.verticalLayout.addWidget(self.buttonBox)

        self.dockWidget.setWidget(self.dockContent)

        # Populate Branch Head Data.
        if self.branItem is not None:

            aSpecItem = self.branItem.Pspec
            if aSpecItem is not None:
                aSpcoList = PipeCad.CollectItem("SPCO", aSpecItem)

                aBoreDict = dict()

                for aSpcoItem in aSpcoList:
                    aScomItem = aSpcoItem.Catref
                    if aScomItem is not None:
                        aParams = aScomItem.Param.split()
                        aBoreDict[int(aParams[0])] = aSpcoItem

                for aBore in sorted(aBoreDict):
                    self.comboBore.addItem(aBore, aBoreDict[aBore])
                # for
            # if

            self.comboConnection.addItem(self.branItem.Tconnect)
            self.comboConnection.addItem(self.branItem.Hconnect)

            self.comboBore.setCurrentText(self.branItem.Tbore)
            self.comboConnection.setCurrentText(self.branItem.Tconnect)
            self.textDirection.setText(self.branItem.Tdirection.string())

            aPos = self.branItem.Tposition.string().split()
            self.textX.setText(aPos[0])
            self.textY.setText(aPos[1])
            self.textZ.setText(aPos[2])
        # if
    # changeTailDetail

    def pickTailPosition(self):
        aPoint = PipeCad.PickPoint("Pick position for branch tail, press ESC to cancel")
        if aPoint is None:
            return
        # if

        self.textX.setText(str(aPoint.X))
        self.textY.setText(str(aPoint.Y))
        self.textZ.setText(str(aPoint.Z))
    # pickTailPosition

    def changeTailConnection(self):
        
        self.dockContent = QWidget()

        aSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.verticalLayout = QVBoxLayout(self.dockContent)

        # Pipe name
        self.horizontalLayout = QHBoxLayout()
        self.labelPipe = QLabel("Pipe: ")
        self.labelPipe.setSizePolicy(aSizePolicy)
        self.textPipe = QLabel(self.pipeItem.Name)
        self.buttonPipe = QPushButton("Set Pipe")
        self.buttonPipe.setSizePolicy(aSizePolicy)
        self.buttonPipe.clicked.connect(self.setPipe)

        self.horizontalLayout.addWidget(self.labelPipe)
        self.horizontalLayout.addWidget(self.textPipe)
        self.horizontalLayout.addWidget(self.buttonPipe)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        # Pipe spec
        self.horizontalLayout = QHBoxLayout()
        self.labelSpec = QLabel("Spec: ")
        self.labelSpec.setSizePolicy(aSizePolicy)
        self.textSpec = QLabel(self.pipeItem.Pspec.Name)
        self.buttonSpec = QPushButton("Set Detail")
        self.buttonSpec.setSizePolicy(aSizePolicy)
        self.buttonSpec.clicked.connect(self.createPipe)

        self.horizontalLayout.addWidget(self.labelSpec)
        self.horizontalLayout.addWidget(self.textSpec)
        self.horizontalLayout.addWidget(self.buttonSpec)

        self.verticalLayout.addLayout(self.horizontalLayout)        

        # Branch Table.
        self.verticalLayout.addWidget(self.tableWidgetBranch)

        # New Branch.
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.buttonBranch)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Branch Tail Connection
        self.labelSpec = QLabel("Connect Branch Tail To: ")
        self.verticalLayout.addWidget(self.labelSpec)

        self.linePipeDetail = QFrame()
        self.linePipeDetail.setFrameShape(QFrame.HLine)
        self.linePipeDetail.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.linePipeDetail)

        if self.branItem.Tref is not None:
            self.labelConnection = QLabel("")
            if self.branItem.Tref is not None:
                self.labelConnection.setText(self.branItem.Tref.Name)
            # if

            self.verticalLayout.addWidget(self.labelConnection)

            self.horizontalLayout = QHBoxLayout()
            self.buttonDisconnect = QPushButton("Disconnect")
            self.buttonReconnect = QPushButton("Reconnect")
            self.buttonBack = QPushButton("Back")
            self.buttonBack.clicked.connect(self.rejectBranch)
            self.horizontalLayout.addWidget(self.buttonDisconnect)
            self.horizontalLayout.addWidget(self.buttonReconnect)
            self.horizontalLayout.addWidget(self.buttonBack)

            self.verticalLayout.addLayout(self.horizontalLayout)
        else:
            self.tableWidgetConnection = QTableWidget()
            self.tableWidgetConnection.setColumnCount(4)

            self.tableWidgetConnection.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
            self.tableWidgetConnection.setHorizontalHeaderItem(1, QTableWidgetItem("Bore"))
            self.tableWidgetConnection.setHorizontalHeaderItem(2, QTableWidgetItem("Type"))
            self.tableWidgetConnection.setHorizontalHeaderItem(3, QTableWidgetItem("Connection"))

            self.tableWidgetConnection.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidgetConnection.setAlternatingRowColors(True)
            self.tableWidgetConnection.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.tableWidgetConnection.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tableWidgetConnection.setGridStyle(Qt.SolidLine)
            self.tableWidgetConnection.horizontalHeader().setStretchLastSection(True)
            self.tableWidgetConnection.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tableWidgetConnection.verticalHeader().setMinimumSectionSize(16)
            self.tableWidgetConnection.verticalHeader().setDefaultSectionSize(18)
            self.tableWidgetConnection.verticalHeader().hide()
            self.tableWidgetConnection.itemSelectionChanged.connect(self.connectionChanged)

            self.verticalLayout.addWidget(self.tableWidgetConnection)

            self.horizontalLayout = QHBoxLayout()

            self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.horizontalLayout.addItem(self.horizontalSpacer)

            self.buttonTailPick = QPushButton("Pick")
            self.buttonTailPick.clicked.connect(self.pickConnection)

            self.buttonConnect = QPushButton("Connect")
            self.buttonBack = QPushButton("Back")
            self.buttonConnect.clicked.connect(self.connectTail)
            self.buttonBack.clicked.connect(self.rejectBranch)

            self.horizontalLayout.addWidget(self.buttonTailPick)
            self.horizontalLayout.addWidget(self.buttonConnect)
            self.horizontalLayout.addWidget(self.buttonBack)

            self.verticalLayout.addLayout(self.horizontalLayout)

        self.dockWidget.setWidget(self.dockContent)
    # changeTailConnection

    def connectTail(self):
        aRow = self.tableWidgetConnection.currentRow()
        if aRow == -1:
            # Connect branch last component.
            aMemberList = self.branItem.Member
            if len(aMemberList) > 1:
                QMessageBox.information(PipeCad, "", "Connect branch tail to last component!")
                aPoint = aMemberList[-1].LeavePoint
                PipeCad.StartTransaction("Set Tail Connection")
                self.branItem.Tposition = aPoint.Position
                self.branItem.Tdirection = aPoint.Direction.Reversed()
                self.branItem.Tbore = aPoint.Bore
                self.branItem.Tconnect = aPoint.Type
                PipeCad.CommitTransaction()
        else:
            aPoint = self.tableWidgetConnection.item(aRow, 1).data(Qt.UserRole)
            PipeCad.StartTransaction("Set Tail Connection")
            self.branItem.Tposition = aPoint.Position
            self.branItem.Tdirection = aPoint.Direction
            self.branItem.Tref = self.tableWidgetConnection.item(aRow, 0).data(Qt.UserRole)
            self.branItem.Tbore = aPoint.Bore
            self.branItem.Tconnect = self.tableWidgetConnection.item(aRow, 2).text()
            PipeCad.CommitTransaction()

        self.rejectBranch()
    # connectTail

    def accept(self):

        if self.pipeItem is not None:
            PipeCad.StartTransaction("Modify Pipe")
            self.pipeItem.Name = self.textName.text
            self.pipeItem.Pspec = self.listWidget.currentItem().text()
            self.pipeItem.Bore = self.comboBore.currentText

            PipeCad.CommitTransaction()

            self.modifyPipe(self.pipeItem)

        else:
            aCurrentItem = PipeCad.CurrentItem()
            if aCurrentItem.Type == "ZONE" or aCurrentItem.Type == "PIPE":

                PipeCad.StartTransaction("Create Pipe")

                PipeCad.CreateItem("PIPE", self.textName.text)
                self.pipeItem = PipeCad.CurrentItem()
                self.pipeItem.Pspec = self.listWidget.currentItem().data(Qt.UserRole)
                self.pipeItem.Bore = self.comboBore.currentText

                self.createBranch()
                
                PipeCad.CommitTransaction()

                self.modifyPipe(self.pipeItem)
            
            else:
                QMessageBox.warning(PipeCad, "", "Unable to create pipe at this point within the hierarchy!")
                return


    def reject(self):
        #PipeCad.removeDockWidget(self.dockWidget)
        if self.pipeItem is not None:
            self.modifyPipe(self.pipeItem)
        else:
            self.dockWidget.hide()

    def acceptBranch(self):
        PipeCad.StartTransaction("Modify Branch")
        self.branItem.Name = self.textName.text
        self.branItem.Pspec = self.listWidget.currentItem().text()
        self.branItem.temperature = float(self.lineTemp.text)
        self.branItem.pressure = float(self.linePressure.text)
        PipeCad.CommitTransaction()

        self.modifyPipe(self.pipeItem)
    # acceptBranch

    def rejectBranch(self):
        self.modifyPipe(self.pipeItem)
    # rejectBranch

    def acceptHeadDetail(self):
        PipeCad.StartTransaction("Modify Branch Head")
        self.branItem.Hbore = self.comboBore.currentText
        self.branItem.Hconnect = self.comboConnection.currentText
        self.branItem.Hdirection = Direction(self.textDirection.text)
        self.branItem.Hposition = Position(self.textX.text + " " + self.textY.text + " " + self.textZ.text)
        PipeCad.CommitTransaction()

        self.modifyPipe(self.pipeItem)
    # acceptHeadDetail

    def acceptTailDetail(self):
        PipeCad.StartTransaction("Modify Branch Tail")
        self.branItem.Tbore = self.comboBore.currentText
        self.branItem.Tconnect = self.comboConnection.currentText
        self.branItem.Tdirection = Direction(self.textDirection.text)
        self.branItem.Tposition = Position(self.textX.text + " " + self.textY.text + " " + self.textZ.text)
        PipeCad.CommitTransaction()

        self.modifyPipe(self.pipeItem)
    # acceptTailDetail


aPipeDlg = PipeDialog(PipeCad)

def Create():
    aPipeDlg.pipeItem = None
    aPipeDlg.createPipe()
# CreatePipe

def Modify():
    aPipeItem = None
    aTreeItem = PipeCad.CurrentItem()

    aType = aTreeItem.Type
    if aType == "PIPE":
        aPipeItem = aTreeItem
    elif aType == "BRAN":
        aPipeItem = aTreeItem.Owner
        aPipeDlg.branItem = aTreeItem
    elif aTreeItem.Owner is not None and aTreeItem.Owner.Type == "BRAN":
        aPipeItem = aTreeItem.Owner.Owner
        aPipeDlg.branItem = aTreeItem.Owner

    if aPipeItem is None:
        QMessageBox.warning(PipeCad, "", "Please Select PIPE or BRANCH to modify!")
        return
    else:
        aPipeDlg.modifyPipe(aPipeItem)

# ModifyPipe

