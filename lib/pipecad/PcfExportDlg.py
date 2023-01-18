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
# Date: 11:20 2021-11-15

import os

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class PcfExporterDlg(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()
    # __init__

    def setupUi(self):
        #self.resize(500, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Design", "Export PCF"))
        
        self.verticalLayout = QVBoxLayout(self)

        self.listWidget = QListWidget()
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setUniformItemSizes(True)

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.buttonPipe = QPushButton("Add Pipe")
        self.buttonBranch = QPushButton("Add Branch")
        self.buttonRemove = QPushButton("Remove")
        self.buttonClear = QPushButton("Clear")

        self.buttonPipe.clicked.connect(self.addPipe)
        self.buttonBranch.clicked.connect(self.addBranch)
        self.buttonRemove.clicked.connect(self.removeList)
        self.buttonClear.clicked.connect(self.clearList)

        self.horizontalLayout.addWidget(self.buttonPipe)
        self.horizontalLayout.addWidget(self.buttonBranch)
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.horizontalLayout.addWidget(self.buttonClear)

        self.verticalLayout.addLayout(self.horizontalLayout)

        aIsoEnv = os.getenv(PipeCad.CurrentProject.Code + "ISO").replace("/","\\")

        if len(aIsoEnv) < 0:
            aIsoEnv = "D:/PipeCAD/PCF/"
        # if

        self.horizontalLayout = QHBoxLayout()
        self.textPath = QLineEdit(aIsoEnv)
        self.toolPath = QPushButton("...")
        self.toolPath.clicked.connect(self.setPath)
        self.horizontalLayout.addWidget(self.textPath)
        self.horizontalLayout.addWidget(self.toolPath)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    # setupUi

    def setPath(self):
        aPath = QFileDialog.getExistingDirectory(self, "PCF Directory", self.textPath.text)
        if len(aPath) > 0:
            self.textPath.setText(aPath)
        # if
    # setPath

    def addPipe(self):
        aPipeItem = PipeCad.CurrentItem()

        if aPipeItem.Type != "PIPE":
            QMessageBox.warning(self, "", "Please select PIPE!")
            return
        # if

        aMemberList = aPipeItem.Member
        for aMember in aMemberList:
            if len(self.listWidget.findItems(aMember.Name, Qt.MatchExactly)) == 0:
                aListItem = QListWidgetItem(aMember.Name, self.listWidget)
                aListItem.setData(Qt.UserRole, aMember)
            # if
        # for
    # addPipe

    def addBranch(self):
        aBranItem = PipeCad.CurrentItem()

        if aBranItem.Type != "BRAN":
            QMessageBox.information(self, "", "Please select BRAN!")
            return
        # if

        if len(self.listWidget.findItems(aBranItem.Name, Qt.MatchExactly)) == 0:
            aListItem = QListWidgetItem(aBranItem.Name, self.listWidget)
            aListItem.setData(Qt.UserRole, aBranItem)
        # if

    # addBranch

    def removeList(self):
        aRow = self.listWidget.currentRow
        self.listWidget.removeRow(aRow)
    # removeList

    def clearList(self):
        self.listWidget.clear()
    # clearList
# PcfExporterDlg

aPcfExporterDlg = PcfExporterDlg(PipeCad)

def Show():
    aPcfExporterDlg.show()
# Show
