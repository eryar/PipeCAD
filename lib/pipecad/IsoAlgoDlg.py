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
# Date: 08:20 2021-11-22

import os
import json

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *
from pipecad import PcfExporter


class AdministrativeDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Administrative Options"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Comments"))
        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.textComments = QPlainTextEdit()
        self.horizontalLayout.addWidget(self.textComments)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.buttonReset = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Reset"))

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonReset)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

    # setupUi

    def setOptionFile(self, theFileName):
        self.optionFileName = theFileName

        self.initData()
    # setOptionFile

    def initData(self):

        # Load option file.
        with open(self.optionFileName, 'r') as aJsonFile:
            self.jsonDict = json.load(aJsonFile)
        # with

        self.textComments.setPlainText(self.jsonDict["Comments"])

    # initData

    def accept(self):

        self.jsonDict["Comments"] = self.textComments.plainText

        with open(self.optionFileName, "w") as aJsonFile:
            json.dump(self.jsonDict, aJsonFile, indent=4, ensure_ascii=False)
        # with

        QDialog.accept(self)
    # accept

# AdminstrativeDialog


class SheetLayoutDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Sheet Layout Options"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Size"))
        self.gridLayout = QGridLayout(self.groupBox)

        self.labelDwgSize = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Drawing size"))
        self.comboDwgSize = QComboBox()
        self.comboDwgSize.addItem("A0", "10:841:1189")
        self.comboDwgSize.addItem("A1", "1:594:841")
        self.comboDwgSize.addItem("A2", "2:420:594")
        self.comboDwgSize.addItem("A3", "3:297:420")
        self.comboDwgSize.addItem("A4", "4:210:297")
        self.comboDwgSize.addItem("A", "8:215.9:279.4")
        self.comboDwgSize.addItem("B", "7:279.4:431.8")
        self.comboDwgSize.addItem("C", "6:431.8:558.8")
        self.comboDwgSize.addItem("D", "5:558.8:86.6")
        self.comboDwgSize.addItem("E", "9:863.6:1117.6")
        self.comboDwgSize.addItem("User", "11:0:0")

        self.comboDwgSize.currentIndexChanged.connect(self.dwgSizeChanged)

        self.labelDwgHeight = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Height"))
        self.textDwgHeight = QLineEdit()

        self.labelDwgWidth = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Width"))
        self.textDwgWidth = QLineEdit()

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addWidget(self.labelDwgSize, 0, 0)
        self.gridLayout.addWidget(self.comboDwgSize, 0, 1)
        self.gridLayout.addWidget(self.labelDwgHeight, 0, 2)
        self.gridLayout.addWidget(self.textDwgHeight, 0, 3)
        self.gridLayout.addWidget(self.labelDwgWidth, 0, 4)
        self.gridLayout.addWidget(self.textDwgWidth, 0, 5)
        self.gridLayout.addItem(self.horizontalSpacer, 0, 6)

        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Graphics"))
        self.gridLayout = QGridLayout(self.groupBox)

        self.labelViewDirection = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "View direction"))
        self.comboViewDirection = QComboBox()
        self.comboViewDirection.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "North arrow to bottom right"), 1)
        self.comboViewDirection.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "North arrow to top right"), 2)
        self.comboViewDirection.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "North arrow to top left"), 3)
        self.comboViewDirection.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "North arrow to bottom left"), 4)

        self.checkNorthArrow = QCheckBox(QT_TRANSLATE_NOOP("IsoAlgo", "Box arround North arrow"))

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addWidget(self.labelViewDirection, 0, 0)
        self.gridLayout.addWidget(self.comboViewDirection, 0, 1)
        self.gridLayout.addWidget(self.checkNorthArrow, 0, 2)
        self.gridLayout.addItem(self.horizontalSpacer, 0, 3)

        self.labelIsometricType = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Isometric type"))
        self.comboIsometricType = QComboBox()
        self.comboIsometricType.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "Fabrication"))
        self.checkIsometricPicture = QCheckBox(QT_TRANSLATE_NOOP("IsoAlgo", "Isometric picture"))

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addWidget(self.labelIsometricType, 1, 0)
        self.gridLayout.addWidget(self.comboIsometricType, 1, 1)
        self.gridLayout.addWidget(self.checkIsometricPicture, 1, 2)
        self.gridLayout.addItem(self.horizontalSpacer, 1, 3)

        self.labelPipelineThickness = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Pipeline thickness"))
        self.textPipelineThickness = QLineEdit("6")

        self.gridLayout.addWidget(self.labelPipelineThickness, 2, 0)
        self.gridLayout.addWidget(self.textPipelineThickness, 2, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Flow arrows and Margins"))
        self.verticalLayoutFlow = QVBoxLayout(self.groupBox)

        self.checkComponentFlow = QCheckBox(QT_TRANSLATE_NOOP("IsoAlgo", "Component flow arrows"))

        self.labelPipelineFlow = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Pipeline flow arrows"))
        self.comboPipelineFlow = QComboBox()
        self.comboPipelineFlow.addItem("On")
        self.comboPipelineFlow.addItem("Automatic")
        self.comboPipelineFlow.addItem("Off")

        self.labelArrowScale = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Scale"))
        self.textArrowScale = QLineEdit("8")

        self.horizontalLayoutFlow = QHBoxLayout()
        self.horizontalLayoutFlow.addWidget(self.checkComponentFlow)
        self.horizontalLayoutFlow.addWidget(self.labelPipelineFlow)
        self.horizontalLayoutFlow.addWidget(self.comboPipelineFlow)
        self.horizontalLayoutFlow.addWidget(self.labelArrowScale)
        self.horizontalLayoutFlow.addWidget(self.textArrowScale)

        self.verticalLayoutFlow.addLayout(self.horizontalLayoutFlow)

        self.gridLayout = QGridLayout()

        self.labelMarginLeft = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Margin Left"))
        self.textMarginLeft = QLineEdit("5")

        self.labelMarginRight = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Margin Right"))
        self.textMarginRight = QLineEdit("5")

        self.gridLayout.addWidget(self.labelMarginLeft, 0, 0)
        self.gridLayout.addWidget(self.textMarginLeft, 0, 1)
        self.gridLayout.addWidget(self.labelMarginRight, 0, 2)
        self.gridLayout.addWidget(self.textMarginRight, 0, 3)

        self.labelMarginTop = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Margin Top"))
        self.textMarginTop = QLineEdit("5")

        self.labelMarginBottom = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Margin Bottom"))
        self.textMarginBottom = QLineEdit("5")

        self.gridLayout.addWidget(self.labelMarginTop, 1, 0)
        self.gridLayout.addWidget(self.textMarginTop, 1, 1)
        self.gridLayout.addWidget(self.labelMarginBottom, 1, 2)
        self.gridLayout.addWidget(self.textMarginBottom, 1, 3)

        self.verticalLayoutFlow.addLayout(self.gridLayout)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.buttonReset = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Reset"))

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonReset)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def setOptionFile(self, theFileName):
        self.optionFileName = theFileName

        self.comboDwgSize.setCurrentIndex(2)
    # setOptionFile

    def dwgSizeChanged(self):
        aSize = self.comboDwgSize.currentData
        aSplit = aSize.split(":")
        if len(aSplit) != 3:
            return
        # if

        if aSplit[0] != "11":
            self.textDwgHeight.setText(aSplit[1])
            self.textDwgWidth.setText(aSplit[2])
        # if
    # dwgSizeChanged

# SheetLayoutDialog

class IsoModifyDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Modify Option File"))
        self.setMinimumWidth(280)

        self.verticalLayout = QVBoxLayout(self)

        self.labelInfo = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Options by functional area"))
        self.verticalLayout.addWidget(self.labelInfo)

        self.administrativeDlg = AdministrativeDialog(self)

        self.buttonAdministrative = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Administrative"))
        self.buttonAdministrative.clicked.connect(self.administrativeOption)
        self.verticalLayout.addWidget(self.buttonAdministrative)

        self.sheetLayoutDlg = SheetLayoutDialog(self)
        self.buttonSheetLayout = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Sheet Layout"))
        self.buttonSheetLayout.clicked.connect(self.sheetLayoutOption)
        self.verticalLayout.addWidget(self.buttonSheetLayout)

        self.buttonDimensioning = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Dimensioning"))
        self.verticalLayout.addWidget(self.buttonDimensioning)

        self.buttonAnnotation = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Annotation"))
        self.verticalLayout.addWidget(self.buttonAnnotation)

        self.buttonMaterialList = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Material List"))
        self.verticalLayout.addWidget(self.buttonMaterialList)

        self.buttonMaterialColumns = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Material Columns"))
        self.verticalLayout.addWidget(self.buttonMaterialColumns)

        self.buttonWeldNumbering = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Weld Numbering"))
        self.verticalLayout.addWidget(self.buttonWeldNumbering)

        self.buttonRevisionTable = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Revision Table"))
        self.verticalLayout.addWidget(self.buttonRevisionTable)

        self.buttonAttributeText = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Attribute Frame Texts"))
        self.verticalLayout.addWidget(self.buttonAttributeText)

        self.buttonStandardText = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Standard Frame Texts"))
        self.verticalLayout.addWidget(self.buttonStandardText)

        self.buttonComponentTags = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Component Tags"))
        self.verticalLayout.addWidget(self.buttonComponentTags)

        aVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(aVerticalSpacer)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel, self)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def initData(self, theOptionFile):
        self.optionFile = theOptionFile

        aFileInfo = QFileInfo(theOptionFile)
        self.setWindowTitle("FILE " + aFileInfo.fileName())
    # initData

    def administrativeOption(self):
        self.administrativeDlg.setOptionFile(self.optionFile)
        self.administrativeDlg.show()
    # administrativeOption

    def sheetLayoutOption(self):
        self.sheetLayoutDlg.setOptionFile(self.optionFile)
        self.sheetLayoutDlg.show()
    # sheetLayoutOption

    def reject(self):
        self.administrativeDlg.close()
        self.sheetLayoutDlg.close()

        QDialog.reject(self)
    # reject
# IsoModifyDialog

class IsoSetupDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)
        
        self.setupUi()
    # __init__
    
    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Isometrics Options"))

        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.labelDirectory = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Options file directory"))
        self.comboDirectory = QComboBox()
        self.comboDirectory.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "Project"))
        self.comboDirectory.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "Local"))
        self.comboDirectory.activated.connect(self.refreshList)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelDirectory)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboDirectory)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Options Files"))
        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.listWidget = QListWidget()
        self.listWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setUniformItemSizes(True)

        self.horizontalLayout.addWidget(self.listWidget)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.buttonCreate = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Create"))
        self.buttonModify = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Modify"))
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel, self)

        self.buttonCreate.clicked.connect(self.createOptionFile)
        self.buttonModify.clicked.connect(self.modifyOptionFile)

        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonCreate)
        self.horizontalLayout.addWidget(self.buttonModify)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.initData()
    # setupUi

    def initData(self):
        self.projectDir = os.getenv(PipeCad.CurrentProject.Code + "ISO") + "/STD"
        if os.path.exists(self.projectDir) == False:
            os.mkdir(self.projectDir)
        # if

        self.localDir = QCoreApplication.applicationDirPath() + "/settings/iso"
        if os.path.exists(self.localDir) == False:
            os.mkdir(self.localDir)
        # if

        self.comboDirectory.setItemData(0, self.projectDir)
        self.comboDirectory.setItemData(1, self.localDir)

        self.refreshList()
    # initData

    def refreshList(self):
        self.listWidget.clear()

        aOptionPath = self.comboDirectory.currentData

        aOptionDir = QDir(aOptionPath)
        aOptionFiles = aOptionDir.entryList(QDir.Files)
        for aOptionFile in aOptionFiles:
            aListItem = QListWidgetItem(aOptionFile, self.listWidget)
            aListItem.setData(Qt.UserRole, aOptionPath + "/" + aOptionFile)
        # for
    # refreshList

    def createOptionFile(self):
        aOptionPath = self.comboDirectory.currentData
        aFileName = QInputDialog.getText(self, QT_TRANSLATE_NOOP("IsoAlgo", "Create Option File"), QT_TRANSLATE_NOOP("IsoAlgo", "Please input isometrics option file name"))
        if len(aFileName) < 1:
            return
        # if

        aOptionFile = aOptionPath + "/" + aFileName
        if os.path.exists(aOptionFile):
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("IsoAlgo", aOptionFile + " exists!"))
            return
        # if

        # Create default IsoAlgo option file.
        aDwgSize = {"Height": 420, "Width": 594}
        aFlowArrow = {"Component": 0, "Pipeline": 8}

        aSheetLayout = {"DwgSize": aDwgSize,
                        "PipelineWidth": 1.0,
                        "NorthDirection": 1,
                        "FlowArrow": aFlowArrow
                    }

        aOptionJson = {"AppName": "IsoAlgo", 
                       "Version": PipeCad.GetVersion(),
                       "Comments": "Comments",
                       "SheetLayout": aSheetLayout
                    }

        with open(aOptionFile, "w") as aJsonFile:
            json.dump(aOptionJson, aJsonFile, indent=4, ensure_ascii=False)
        # with

        self.refreshList()
    # createOptionFile

    def modifyOptionFile(self):
        aCurrentItem = self.listWidget.currentItem()
        if aCurrentItem is None:
            return
        # if

        aModifyDlg = IsoModifyDialog(PipeCad)
        aModifyDlg.initData(aCurrentItem.data(Qt.UserRole))
        aModifyDlg.show()

        self.reject()
    # modifyOptionFile
# IsoSetupDialog

# Singleton Instance.
aSetupDlg = IsoSetupDialog(PipeCad)

def Setup():
    aSetupDlg.show()
# Setup

class IsoAlgoDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.filePath = os.getenv(PipeCad.CurrentProject.Code + "ISO")
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Pipe Isometrics"))
        self.setWindowFlags(Qt.Window)

        self.verticalLayout = QVBoxLayout(self)
        
        self.isoGraphicsView = QIsoGraphicsView(self)
        self.verticalLayout.addWidget(self.isoGraphicsView)
        
        # Action buttons.
        self.horizontalLayout = QHBoxLayout(self)

        self.buttonPreview = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Preview"))
        self.buttonPreview.setToolTip(QT_TRANSLATE_NOOP("IsoAlgo", "Preview Pipe Isometrics"))
        self.buttonPreview.clicked.connect(self.previewIso)

        self.buttonExport = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Export"))
        self.buttonExport.setToolTip(QT_TRANSLATE_NOOP("IsoAlgo", "Export Pipe Isometrics to DXF"))
        self.buttonExport.clicked.connect(self.exportIso)

        self.buttonPCF = QPushButton("IDF/PCF")
        self.buttonPCF.setToolTip(QT_TRANSLATE_NOOP("IsoAlgo", "Preview the selected IDF/PCF"))
        self.buttonPCF.clicked.connect(self.previewPcf)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel, self)

        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonPreview)
        self.horizontalLayout.addWidget(self.buttonExport)
        self.horizontalLayout.addWidget(self.buttonPCF)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.resize(860, 600)
    # setupUi

    def previewIso(self):
        aIsoEnv = os.getenv(PipeCad.CurrentProject.Code + "ISO")

        aTreeItem = PipeCad.CurrentItem()
        aName = aTreeItem.Name
        if len(aName) < 1:
            aName = aTreeItem.RefNo.replace("/", "_")
        # if
        
        if len(aName) > 1 and len(aIsoEnv) > 1:
            aFileName = aIsoEnv + "/" + aName + ".pcf"
            PcfExporter.ExportPcf(aTreeItem, aFileName)
            self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Pipe Isometrics: ") + aName)
            self.isoGraphicsView.PreviewIso(aFileName)
        # if
    # previewIso

    def previewPcf(self):
        aFileName = QFileDialog.getOpenFileName(self, "Select PCF File", self.filePath, "Piping Files (*.idf *.pcf)")
        if len(aFileName) > 0:
            self.filePath = aFileName
            self.isoGraphicsView.PreviewIso(aFileName)
        # if
    # previewPcf

    def exportIso(self):
        aIsoEnv = os.getenv(PipeCad.CurrentProject.Code + "ISO")
        os.chdir(aIsoEnv)
        os.system("start.")
    # exportIso

# IsoAlgoDialog

# Singleton Instance.
aIsoAlgoDlg = IsoAlgoDialog(PipeCad)

def Show():
    aIsoAlgoDlg.show()
# Show
