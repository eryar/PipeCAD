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

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *
from pipecad import PcfExporter


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

        self.refreshList()
    # initData

    def refreshList(self):
        self.listWidget.clear()

        aOptionPath = self.projectDir

        aIndex = self.comboDirectory.currentIndex
        if aIndex == 1:
            aOptionPath = self.localDir
        # if

        aOptionDir = QDir(aOptionPath)
        aOptionFiles = aOptionDir.entryList(QDir.Files)
        for aOptionFile in aOptionFiles:
            aListItem = QListWidgetItem(aOptionFile, self.listWidget)
        # for
    # refreshList

    def createOptionFile(self):
        aIndex = self.comboDirectory.currentIndex
        aFileName = QInputDialog.getText(self, QT_TRANSLATE_NOOP("IsoAlgo", "Create Option File"), QT_TRANSLATE_NOOP("IsoAlgo", "Please input isometrics option file name"))
        if len(aFileName) < 1:
            return
        # if

        if aIndex == 0:
            # Project
            if len(self.projectDir) > 1:
                aFile = open(self.projectDir + "/" + aFileName, "w")
                aFile.close()
            # if
        else:
            # Local
            if len(self.localDir) > 1:
                aFile = open(self.localDir + "/" + aFileName, "w")
                aFile.close()
            # if
        # if

        self.refreshList()
    # createOptionFile

    def modifyOptionFile(self):
        pass
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
