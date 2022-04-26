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
from PythonQt.PipeCAD import *

from PipeCAD import *
from PipeCAD import PcfExporter

class IsoAlgoDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
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

        self.buttonPCF = QPushButton("PCF")
        self.buttonPCF.setToolTip(QT_TRANSLATE_NOOP("IsoAlgo", "Preview the selected PCF"))
        self.buttonPCF.clicked.connect(self.previewPcf)

        self.buttonPreview = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Preview"))
        self.buttonPreview.setToolTip(QT_TRANSLATE_NOOP("IsoAlgo", "Preview Pipe Isometrics"))
        self.buttonPreview.clicked.connect(self.previewIso)

        self.buttonExport = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Export"))
        self.buttonExport.setToolTip(QT_TRANSLATE_NOOP("IsoAlgo", "Export Pipe Isometrics to DXF"))
        self.buttonExport.clicked.connect(self.exportIso)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)

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
        if len(aName) > 1 and len(aIsoEnv) > 1:
            aFileName = aIsoEnv + "/" + aName + ".pcf"
            PcfExporter.ExportPcf(aTreeItem, aFileName)
            self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Pipe Isometrics: ") + aName)
            self.isoGraphicsView.PreviewIso(aFileName)
        # if
    # previewIso

    def previewPcf(self):
        aIsoEnv = os.getenv(PipeCad.CurrentProject.Code + "ISO")
        aFileName = QFileDialog.getOpenFileName(self, "Select PCF File", aIsoEnv)
        if len(aFileName) > 0:
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
