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
# Copyright (C) 2022 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 15:13 2022-09-15

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


class GraphicsDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("View", "Graphics Settings"))

        self.verticalLayout = QVBoxLayout(self)

        self.tabWidget = QTabWidget()

        # Tab Colour
        self.tabColour = QWidget()
        self.verticalLayoutTab = QVBoxLayout(self.tabColour)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("View", "Background"))

        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.buttonBgColor = QPushButton()
        self.buttonBgColor.setMaximumWidth(32)
        self.buttonBgColor.setAutoFillBackground(True)
        self.buttonBgColor.setFlat(True)
        self.buttonBgColor.clicked.connect(self.selectBackgroundColor)

        self.checkGraduated = QCheckBox(QT_TRANSLATE_NOOP("View", "Graduated"))

        self.horizontalLayout.addWidget(self.buttonBgColor)
        self.horizontalLayout.addWidget(self.checkGraduated)

        self.verticalLayoutTab.addWidget(self.groupBox)

        self.tabWidget.addTab(self.tabColour, QT_TRANSLATE_NOOP("View", "Colour"))

        # Tab Representation
        self.tabRepresentation = QWidget()
        self.verticalLayoutTab = QVBoxLayout(self.tabRepresentation)

        self.formLayout = QFormLayout()
        self.labelTolerance = QLabel(QT_TRANSLATE_NOOP("View", "Arc Tolerance"))
        self.textTolerance = QLineEdit(str(PipeCad.GetArcTolerance()))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelTolerance)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textTolerance)

        self.verticalLayoutTab.addLayout(self.formLayout)

        self.tabWidget.addTab(self.tabRepresentation, QT_TRANSLATE_NOOP("View", "Representation"))

        self.verticalLayout.addWidget(self.tabWidget)

        # Action Box.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def reload(self):
        # Background Color
        aBackgroundColor = PipeCad.GetBackgroundColor()

        aPalette = self.buttonBgColor.palette
        aPalette.setColor(QPalette.Button, aBackgroundColor)
        self.buttonBgColor.setPalette(aPalette)

        self.checkGraduated.setChecked(PipeCad.IsGradientBackground())

        # Arc Tolerance
        self.textTolerance.setText(str(PipeCad.GetArcTolerance()))
    # reload

    def selectBackgroundColor(self):
        aColor = PipeCad.GetBackgroundColor()
        aColor = QColorDialog.getColor(aColor, self)
        if aColor.isValid():
            aPalette = self.buttonBgColor.palette
            aPalette.setColor(QPalette.Button, aColor)
            self.buttonBgColor.setPalette(aPalette)
        # if
    # selectBackgroundColor

    def accept(self):
        # Colour
        aBackgroundColor = self.buttonBgColor.palette.color(QPalette.Button)
        PipeCad.SetBackgroundColor(aBackgroundColor, self.checkGraduated.checked)

        # Representation
        aTolerance = float(self.textTolerance.text)

        PipeCad.SetArcTolerance(aTolerance)

        QDialog.accept(self)
    # accept

# GraphicsDialog

# Singleton Instance.
aGraphicsDlg = GraphicsDialog(PipeCad)

def SetGraphics():
    aGraphicsDlg.reload()
    aGraphicsDlg.show()
# SetGraphics


class SnapDialog(QDialog):
    """docstring for SnapDialog"""
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("View", "Snap Options"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("View", "Object Snaps"))

        self.gridLayout = QGridLayout(self.groupBox)

        # Object Snaps
        self.checkSnapEnd = QCheckBox(QT_TRANSLATE_NOOP("View", "End"))
        self.checkSnapMiddle = QCheckBox(QT_TRANSLATE_NOOP("View", "Middle"))
        self.checkSnapCenter = QCheckBox(QT_TRANSLATE_NOOP("View", "Center"))
        self.checkSnapPpoint = QCheckBox(QT_TRANSLATE_NOOP("View", "Ppoint"))

        self.checkSnapEnd.setChecked(PipeCad.TestSnapOption(PipeCad.SnapEnd))
        self.checkSnapMiddle.setChecked(PipeCad.TestSnapOption(PipeCad.SnapMiddle))
        self.checkSnapCenter.setChecked(PipeCad.TestSnapOption(PipeCad.SnapCenter))
        self.checkSnapPpoint.setChecked(PipeCad.TestSnapOption(PipeCad.SnapPpoint))

        self.gridLayout.addWidget(self.checkSnapEnd, 0, 0)
        self.gridLayout.addWidget(self.checkSnapMiddle, 1, 0)
        self.gridLayout.addWidget(self.checkSnapCenter, 2, 0)
        self.gridLayout.addWidget(self.checkSnapPpoint, 3, 0)

        self.verticalLayout.addWidget(self.groupBox)

        # Action Box.
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aSnapOptions = PipeCad.SnapOptions()

        if self.checkSnapEnd.checked:
            aSnapOptions = aSnapOptions | PipeCad.SnapEnd
        # if

        if self.checkSnapMiddle.checked:
            aSnapOptions = aSnapOptions | PipeCad.SnapMiddle
        # if

        if self.checkSnapCenter.checked:
            aSnapOptions = aSnapOptions | PipeCad.SnapCenter
        # if

        if self.checkSnapPpoint.checked:
            aSnapOptions = aSnapOptions | PipeCad.SnapPpoint
        # if

        PipeCad.SetSnapOptions(aSnapOptions)

        QDialog.accept(self)
    # accept
# SnapOptionsDialog        

def SetSnapOptions():
    aSnapDlg = SnapDialog(PipeCad)
    aSnapDlg.exec()
# SetSnapOptions
