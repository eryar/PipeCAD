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

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Plots"))
        self.gridLayout = QGridLayout(self.groupBox)

        self.labelPlotDirectory = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Directory"))
        self.textPlotDirectory = QLineEdit()

        self.labelDxf = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "DXF"))
        self.checkDxf = QCheckBox(QT_TRANSLATE_NOOP("IsoAlgo", "Output"))

        self.gridLayout.addWidget(self.labelPlotDirectory, 0, 0)
        self.gridLayout.addWidget(self.textPlotDirectory, 0, 1)

        self.gridLayout.addWidget(self.labelDxf, 1, 0)
        self.gridLayout.addWidget(self.checkDxf, 1, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.buttonReset = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Reset"))
        self.buttonReset.clicked.connect(self.resetData)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonReset)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

    # setupUi

    def setOptionFile(self, theFileName):
        self.optionFileName = theFileName

        self.resetData()
    # setOptionFile

    def resetData(self):

        # Load option file.
        with open(self.optionFileName, 'r') as aJsonFile:
            self.jsonDict = json.load(aJsonFile)
        # with

        self.textComments.setPlainText(self.jsonDict["Comments"])

        self.textPlotDirectory.setText(self.jsonDict["PlotDirectory"])
        self.checkDxf.setChecked(self.jsonDict["OutputDXF"])

    # resetData

    def accept(self):

        self.jsonDict["Comments"] = self.textComments.plainText
        self.jsonDict["PlotDirectory"] = self.textPlotDirectory.text
        self.jsonDict["OutputDXF"] = self.checkDxf.checked

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
        self.verticalLayoutGraphics = QVBoxLayout(self.groupBox)

        self.gridLayout = QGridLayout()
        self.verticalLayoutGraphics.addLayout(self.gridLayout)

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

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Graphics Area"))
        self.gridLayout = QGridLayout(self.groupBox)

        self.labelDwgLeft = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Left"))
        self.textDwgLeft = QLineEdit("5")

        self.labelDwgRight = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Right"))
        self.textDwgRight = QLineEdit("5")

        self.gridLayout.addWidget(self.labelDwgLeft, 0, 0)
        self.gridLayout.addWidget(self.textDwgLeft, 0, 1)
        self.gridLayout.addWidget(self.labelDwgRight, 0, 2)
        self.gridLayout.addWidget(self.textDwgRight, 0, 3)

        self.labelDwgTop = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Top"))
        self.textDwgTop = QLineEdit("5")

        self.labelDwgBottom = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Bottom"))
        self.textDwgBottom = QLineEdit("5")

        self.gridLayout.addWidget(self.labelDwgBottom, 1, 0)
        self.gridLayout.addWidget(self.textDwgBottom, 1, 1)
        self.gridLayout.addWidget(self.labelDwgTop, 1, 2)
        self.gridLayout.addWidget(self.textDwgTop, 1, 3)

        self.verticalLayoutGraphics.addWidget(self.groupBox)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Flow arrows"))
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

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.buttonReset = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Reset"))
        self.buttonReset.clicked.connect(self.resetData)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonReset)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def setOptionFile(self, theFileName):
        self.optionFileName = theFileName

        #self.comboDwgSize.setCurrentIndex(2)
        self.resetData()
    # setOptionFile

    def resetData(self):
        # Load option file.
        with open(self.optionFileName, 'r') as aJsonFile:
            self.jsonDict = json.load(aJsonFile)
        # with

        aSheetLayout = self.jsonDict["SheetLayout"]

        # Drawing Size
        aDwgSize = aSheetLayout["DwgSize"]

        try:
            aSizeIndex = aDwgSize["Index"]
        except Exception as e:
            aSizeIndex = 2
        # try

        self.comboDwgSize.setCurrentIndex(aSizeIndex)
        self.textDwgHeight.setText(aDwgSize["Height"])
        self.textDwgWidth.setText(aDwgSize["Width"])

        # Graphics
        aNorthDir = aSheetLayout["NorthDirection"]
        self.comboViewDirection.setCurrentIndex(aNorthDir)
        self.textPipelineThickness.setText(aSheetLayout["PipelineWidth"])

        # Graphics Area
        aDwgArea = aSheetLayout["DwgArea"]
        self.textDwgLeft.setText(aDwgArea["Left"])
        self.textDwgRight.setText(aDwgArea["Right"])
        self.textDwgTop.setText(aDwgArea["Top"])
        self.textDwgBottom.setText(aDwgArea["Bottom"])

        # Flow Arrow.
        aFlowArrow = aSheetLayout["FlowArrow"]
        aComponentFlow = aFlowArrow["Component"]
        aPipelineFlow = aFlowArrow["Pipeline"]

        self.checkComponentFlow.setChecked(aComponentFlow == 0)
        if aPipelineFlow == 1:
            self.comboPipelineFlow.setCurrentIndex(2)
            self.textArrowScale.setText("1")
        elif aPipelineFlow == 0:
            self.comboPipelineFlow.setCurrentIndex(0)
            self.textArrowScale.setText("8")
        else:
            self.comboPipelineFlow.setCurrentIndex(1)
            self.textArrowScale.setText(str(aPipelineFlow))
        # if

    # resetData

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

    def accept(self):
        aSheetLayout = self.jsonDict["SheetLayout"]

        # Drawing Size
        aDwgSize = {"Index": self.comboDwgSize.currentIndex,
                    "Height": float(self.textDwgHeight.text),
                    "Width": float(self.textDwgWidth.text) }

        aSheetLayout["DwgSize"] = aDwgSize

        # Graphics
        aSheetLayout["NorthDirection"] = self.comboViewDirection.currentIndex
        aSheetLayout["PipelineWidth"] = float(self.textPipelineThickness.text)

        # Graphics Area
        aDwgArea = {"Left": float(self.textDwgLeft.text), 
                    "Bottom": float(self.textDwgBottom.text),
                    "Right": float(self.textDwgRight.text),
                    "Top": float(self.textDwgTop.text)
                    }

        aSheetLayout["DwgArea"] = aDwgArea

        # Flow Arrow
        aFlowArrow = aSheetLayout["FlowArrow"]

        if self.checkComponentFlow.checked:
            aFlowArrow["Component"] = 0
        else:
            aFlowArrow["Component"] = 1
        # if

        aFlowIndex = self.comboPipelineFlow.currentIndex
        if aFlowIndex == 0:
            aFlowArrow["Pipeline"] = 8
        elif aFlowIndex == 1:
            aFlowArrow["Pipeline"] = int(self.textArrowScale.text)
        else:
            aFlowArrow["Pipeline"] = 1
        # if

        with open(self.optionFileName, "w") as aJsonFile:
            json.dump(self.jsonDict, aJsonFile, indent=4, ensure_ascii=False)
        # with

        QDialog.accept(self)
    # accept

# SheetLayoutDialog


class DimensioningDialog(QDialog):
    def __init__(self, theParent = None):
        QDialog.__init__(self, theParent)

        self.setupUi()
    # __init__

    def setupUi(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Dimensioning Options"))

        self.verticalLayout = QVBoxLayout(self)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Units"))
        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Dimensions"))
        self.verticalLayoutGroup = QVBoxLayout(self.groupBox)

        self.gridLayout = QGridLayout()

        # Labels.
        self.labelDimensionType = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Dimension type"))
        self.labelDimensionComponent = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Component"))
        self.labelDimensionOverall = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Overall"))
        self.labelDimensionSupport = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Support"))

        self.gridLayout.addWidget(self.labelDimensionType, 0, 0)
        self.gridLayout.addWidget(self.labelDimensionComponent, 0, 1)
        self.gridLayout.addWidget(self.labelDimensionOverall, 0, 2)
        self.gridLayout.addWidget(self.labelDimensionSupport, 0, 3)

        # Representation
        self.labelRepresentation = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Representation"))
        self.comboDimensionComponent = QComboBox()
        self.comboDimensionComponent.addItem("Off")
        self.comboDimensionComponent.addItem("String")
        self.comboDimensionComponent.addItem("Composite")

        self.comboDimensionOverall = QComboBox()
        self.comboDimensionOverall.addItem("Off")
        self.comboDimensionOverall.addItem("Normal")
        self.comboDimensionOverall.addItem("Centreline")
        self.comboDimensionOverall.addItem("Critical")

        self.comboDimensionSupport = QComboBox()
        self.comboDimensionSupport.addItem("Off")
        self.comboDimensionSupport.addItem("String")
        self.comboDimensionSupport.addItem("Overall")

        self.gridLayout.addWidget(self.labelRepresentation, 1, 0)
        self.gridLayout.addWidget(self.comboDimensionComponent, 1, 1)
        self.gridLayout.addWidget(self.comboDimensionOverall, 1, 2)
        self.gridLayout.addWidget(self.comboDimensionSupport, 1, 3)

        # Standouts
        self.labelStandouts = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Standouts"))
        self.textDimensionComponent = QLineEdit("11.0")
        self.textDimensionOverall = QLineEdit("16.0")
        self.textDimensionSupport = QLineEdit("6.0")

        self.gridLayout.addWidget(self.labelStandouts, 2, 0)
        self.gridLayout.addWidget(self.textDimensionComponent, 2, 1)
        self.gridLayout.addWidget(self.textDimensionOverall, 2, 2)
        self.gridLayout.addWidget(self.textDimensionSupport, 2, 3)

        self.verticalLayoutGroup.addLayout(self.gridLayout)

        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Fall Indicator"))
        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("IsoAlgo", "Skew Box"))
        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.buttonReset = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Reset"))
        self.buttonReset.clicked.connect(self.resetData)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.horizontalLayout.addWidget(self.buttonReset)
        self.horizontalLayout.addWidget(self.buttonBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # setupUi

    def setOptionFile(self, theFileName):
        pass
    # setOptionFile

    def resetData(self):
        pass
    # resetData

# DimensionDialog


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

        self.dimensioningDlg = DimensioningDialog(self)

        self.buttonDimensioning = QPushButton(QT_TRANSLATE_NOOP("IsoAlgo", "Dimensioning"))
        self.buttonDimensioning.clicked.connect(self.dimensioningOption)
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

        aVerticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
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

    def dimensioningOption(self):
        self.dimensioningDlg.setOptionFile(self.optionFile)
        self.dimensioningDlg.show()
    # dimensionOption

    def reject(self):
        self.administrativeDlg.close()
        self.sheetLayoutDlg.close()
        self.dimensioningDlg.close()

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

        if self.listWidget.count > 0:
            self.listWidget.setCurrentRow(0)
        # if
    # refreshList

    def createOptionFile(self):
        aOptionPath = self.comboDirectory.currentData
        aFileName = QInputDialog.getText(self, QT_TRANSLATE_NOOP("IsoAlgo", "Create Option File"), QT_TRANSLATE_NOOP("IsoAlgo", "Please input isometrics option file name"))
        if len(aFileName) < 1:
            return
        # if

        aOptionFile = aOptionPath + "/" + aFileName
        if os.path.exists(aOptionFile):
            if QMessageBox.question(self, "", QT_TRANSLATE_NOOP("IsoAlgo", "Overwrite " + aOptionFile + "?")) == QMessageBox.No:
                return
            # if
        # if

        # Create default IsoAlgo option file.
        aDwgSize = {"Height": 420, "Width": 594}
        aDwgArea = {"Left": 20.0, "Bottom": 20.0, "Right": 360.0, "Top": 380 }
        aFlowArrow = {"Component": 0, "Pipeline": 8}

        aSheetLayout = {"DwgSize": aDwgSize,
                        "DwgArea": aDwgArea,
                        "PipelineWidth": 1.0,
                        "NorthDirection": 1,
                        "FlowArrow": aFlowArrow
                    }

        aOptionJson = {"AppName": "IsoAlgo", 
                       "Version": PipeCad.GetVersion(),
                       "Comments": "Comments",
                       "PlotDirectory": QCoreApplication.applicationDirPath() + "/ISO",
                       "OutputDXF": True,
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

        self.labelOption = QLabel(QT_TRANSLATE_NOOP("IsoAlgo", "Option File"))
        self.comboOptionPath = QComboBox()
        self.comboOptionPath.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "Project"))
        self.comboOptionPath.addItem(QT_TRANSLATE_NOOP("IsoAlgo", "Local"))
        self.comboOptionPath.activated.connect(self.refreshList)

        self.comboOptionFile = QComboBox()

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

        self.horizontalLayout.addWidget(self.labelOption)
        self.horizontalLayout.addWidget(self.comboOptionPath)
        self.horizontalLayout.addWidget(self.comboOptionFile)
        self.horizontalLayout.addWidget(self.buttonPreview)
        self.horizontalLayout.addWidget(self.buttonExport)
        self.horizontalLayout.addWidget(self.buttonPCF)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.initData()
        self.resize(860, 600)
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

        self.comboOptionPath.setItemData(0, self.projectDir)
        self.comboOptionPath.setItemData(1, self.localDir)

        self.refreshList()
    # initData

    def refreshList(self):
        self.comboOptionFile.clear()

        aOptionPath = self.comboOptionPath.currentData

        aOptionDir = QDir(aOptionPath)
        aOptionFiles = aOptionDir.entryList(QDir.Files)
        for aOptionFile in aOptionFiles:
            self.comboOptionFile.addItem(aOptionFile, aOptionPath + "/" + aOptionFile)
        # for

        if self.comboOptionFile.count > 0:
            self.comboOptionFile.setCurrentIndex(0)
        # if
    # refreshList

    def previewIso(self):
        aTreeItem = PipeCad.CurrentItem()
        aName = aTreeItem.Name
        if len(aName) < 1:
            aName = aTreeItem.RefNo.replace("/", "_")
        # if

        aOptionFile = self.comboOptionFile.currentData
        # Load option file.
        with open(aOptionFile, 'r') as aJsonFile:
            self.jsonDict = json.load(aJsonFile)
        # with

        aIsoEnv = self.jsonDict["PlotDirectory"]
        if len(aIsoEnv) < 1:
            aIsoEnv = os.getenv(PipeCad.CurrentProject.Code + "ISO")
        # if
        
        if len(aName) > 1 and len(aIsoEnv) > 1:
            aFileName = aIsoEnv + "/" + aName + ".pcf"
            PcfExporter.ExportPcf(aTreeItem, aFileName)
            self.setWindowTitle(QT_TRANSLATE_NOOP("IsoAlgo", "Pipe Isometrics: ") + aName)

            self.isoGraphicsView.SetOptionFile(aOptionFile)
            self.isoGraphicsView.PreviewIso(aFileName)
        # if
    # previewIso

    def previewPcf(self):
        aFileName = QFileDialog.getOpenFileName(self, "Select Pipe File", self.filePath, "Piping Files (*.idf *.pcf)")
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
