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
# Date: 11:20 2021-09-25

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

class SdteDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.modifyItem = None
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(500, 360)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Paragon", "Detail Text Definition"))

        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()

        self.comboBox = QComboBox()
        self.comboBox.addItem("Create")
        self.comboBox.addItem("Modify")
        self.comboBox.activated.connect(self.activateName)

        self.horizontalLayout.addWidget(self.comboBox)

        self.textName = QLineEdit()
        self.horizontalLayout.addWidget(self.textName)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setAlternatingRowColors(True)

        self.treeWidget.currentItemChanged.connect(self.currentItemChanged)

        aDatabase = QSqlDatabase.addDatabase("QSQLITE", "PipeStd_TEXT")
        aDatabase.setDatabaseName("catalogues/PipeStd.db")
        aDatabase.open()

        self.typeModel = QSqlQueryModel()
        self.typeModel.setQuery("SELECT DISTINCT Type, Icon FROM SKEY", aDatabase)

        for i in range(self.typeModel.rowCount()):
            aRecord = self.typeModel.record(i)
            aType = aRecord.value("Type")
            aIcon = ":/PipeCad/Resources/" + str(aRecord.value("Icon"))

            aTypeItem = QTreeWidgetItem(self.treeWidget)
            aTypeItem.setText(0, aType)
            aTypeItem.setIcon(0, QIcon(aIcon))

            self.skeyModel = QSqlQueryModel()
            self.skeyModel.setQuery("SELECT Skey, Detail FROM SKEY WHERE Type='" + aType + "'", aDatabase)

            for j in range(self.skeyModel.rowCount()):
                aRecord = self.skeyModel.record(j)
                aSkey = aRecord.value("Skey")
                aDetail = aRecord.value("Detail")

                aSkeyItem = QTreeWidgetItem(aTypeItem)
                aSkeyItem.setText(0, aSkey)
                aSkeyItem.setText(1, aDetail)
            # for
        # for

        self.verticalLayout.addWidget(self.treeWidget)

        self.formLayout = QFormLayout(self)
        self.labelSkey = QLabel("Symbol Key")
        self.textSkey = QLineEdit()
        self.textSkey.textEdited.connect(self.skeyChanged)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelSkey)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textSkey)

        self.labelRtext = QLabel("Detail(ISO)")
        self.textRtext = QLineEdit()

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelRtext)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textRtext)

        self.labelStext = QLabel("Stext")
        self.textStext = QLineEdit()

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelStext)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textStext)

        self.labelTtext = QLabel("Ttext")
        self.textTtext = QLineEdit()

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelTtext)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textTtext)

        self.verticalLayout.addLayout(self.formLayout)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.retranslateUi()
    # setupUi

    def retranslateUi(self):
        aHeaderItem = self.treeWidget.headerItem()
        aHeaderItem.setText(0, "Type")
        aHeaderItem.setText(1, "Description")
    # retranslateUi

    def activateName(self):
        self.modifyItem = None
        
        aIndex = self.comboBox.currentIndex
        if aIndex == 0:
            # create
            self.textName.setText("")
        else:
            # modify
            try:
                aSdteItem = PipeCad.CurrentItem()
                if aSdteItem.Type != "SDTE":
                    raise TypeError(aSdteItem.Name + " is not SDTE!")
                # if

                self.modifyItem = aSdteItem

                self.textName.setText(aSdteItem.Name)
                self.textSkey.setText(aSdteItem.Skey)
                self.textRtext.setText(aSdteItem.Rtext)
                self.textStext.setText(aSdteItem.Stext)
                self.textTtext.setText(aSdteItem.Ttext)

                self.skeyChanged()

            except Exception as e:
                QMessageBox.critical(self, "", e)
                raise e
            # try
        # if

    # activateName

    def currentItemChanged(self, theCurrentItem):
        aSkey = theCurrentItem.text(0)
        aDetail = theCurrentItem.text(1)

        if len(aDetail) > 0:
            self.textSkey.setText(aSkey)
        # if
    # currentItemChanged

    def skeyChanged(self):
        aItems = self.treeWidget.findItems(self.textSkey.text, Qt.MatchRecursive | Qt.MatchStartsWith | Qt.MatchCaseSensitive)
        if len(aItems) > 0:
            self.treeWidget.blockSignals(True)
            self.treeWidget.setCurrentItem(aItems[0])
            self.treeWidget.blockSignals(False)
        # if
    # skeyChanged

    def modify(self):
        aName = self.textName.text
        aSkey = self.textSkey.text
        aRtex = self.textRtext.text
        aStex = self.textStext.text
        aTtex = self.textTtext.text

        if self.modifyItem is None:
            QMessageBox.warning(self, "", "Please select item to modify!")
            return
        # if

        try:
            PipeCad.StartTransaction("Modify Detail Text")
            self.modifyItem.Name = aName
            self.modifyItem.Skey = aSkey
            self.modifyItem.Rtext = aRtex
            self.modifyItem.Stext = aStex
            self.modifyItem.Ttext = aTtex
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # modify

    def create(self):
        aName = self.textName.text
        aSkey = self.textSkey.text
        aRtex = self.textRtext.text
        aStex = self.textStext.text
        aTtex = self.textTtext.text

        try:
            PipeCad.StartTransaction("Build Detail Text")
            PipeCad.CreateItem("SDTE", aName)
            aSdteItem = PipeCad.CurrentItem()
            aSdteItem.Skey = aSkey
            aSdteItem.Rtext = aRtex
            aSdteItem.Stext = aStex
            aSdteItem.Ttext = aTtex
            PipeCad.CommitTransaction()
        except Exception as e:
            QMessageBox.critical(self, "", e)
            raise e
        # try
    # create

    def accept(self):
        aIndex = self.comboBox.currentIndex
        if aIndex == 0:
            # create
            self.create()
        else:
            # modify
            self.modify()
        # if

        QDialog.accept(self)
    # accept

# Singleton Instance.
aSdteDlg = SdteDialog(PipeCad)

def Show():
    aSdteDlg.show()
# Show
