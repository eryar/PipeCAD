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
# Date: 21:16 2021-09-16


from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

import os
import subprocess

class LoginDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.setupUi()

    # __init__

    def setupUi(self):
        self.resize(330, 200)
        self.setWindowTitle(QT_TRANSLATE_NOOP("PipeCAD", "PipeCAD Login" ) )

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(6)

        self.labelProject = QLabel( QT_TRANSLATE_NOOP( "PipeCAD", "Project" ) )
        self.comboBoxProject = QComboBox()
        self.buttonCreate = QPushButton( QT_TRANSLATE_NOOP( "PipeCAD", "Create" ) )

        for aProject in (PipeCad.Projects):
            self.comboBoxProject.addItem(aProject.Number)
        # for

        self.comboBoxProject.currentIndexChanged.connect(self.projectChanged)
        self.buttonCreate.clicked.connect(self.createProject)

        self.gridLayout.addWidget(self.labelProject, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBoxProject, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.buttonCreate, 0, 2, 1, 1)

        self.labelUsername = QLabel( QT_TRANSLATE_NOOP( "PipeCAD", "Username" ) )
        self.comboBoxUser = QComboBox()
        self.comboBoxUser.setEditable(True)

        self.gridLayout.addWidget(self.labelUsername, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBoxUser, 1, 1, 1, 1)

        self.labelPassword = QLabel( QT_TRANSLATE_NOOP( "PipeCAD", "Password" ) )
        self.lineEditPassword = QLineEdit(self)
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.textChanged.connect(self.passwordChanged)

        PipeCad.SetIndicator(self.lineEditPassword)

        self.gridLayout.addWidget(self.labelPassword, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEditPassword, 2, 1, 1, 1)

        self.buttonChange = QPushButton( QT_TRANSLATE_NOOP( "PipeCAD", "Change" ) )
        self.buttonChange.clicked.connect(self.changePassword)
        self.gridLayout.addWidget(self.buttonChange, 2, 2, 1, 1)

        self.labelMdb = QLabel( QT_TRANSLATE_NOOP( "PipeCAD", "MDB" ) )
        self.comboBoxMdb = QComboBox()
        self.comboBoxMdb.setEditable(True)

        self.gridLayout.addWidget(self.labelMdb, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBoxMdb, 3, 1, 1, 1)

        self.labelModule = QLabel( QT_TRANSLATE_NOOP( "PipeCAD", "Module" ) )
        self.comboBoxModule = QComboBox()
        self.comboBoxModule.addItem("Admin")
        self.comboBoxModule.addItem("Paragon")
        self.comboBoxModule.addItem("Design")
        self.checkBox = QCheckBox( QT_TRANSLATE_NOOP( "PipeCAD", "Read Only" ) )

        self.gridLayout.addWidget(self.labelModule, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBoxModule, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.checkBox, 4, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

        if len(PipeCad.Projects) > 0:
            self.projectChanged(0)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("LoginDlg", u"PipeCAD Login", None))
        self.labelPassword.setText(QCoreApplication.translate("LoginDlg", u"Password", None))
        self.comboBoxModule.setItemText(0, QCoreApplication.translate("LoginDlg", u"Admin", None))
        self.comboBoxModule.setItemText(1, QCoreApplication.translate("LoginDlg", u"Paragon", None))
        self.comboBoxModule.setItemText(2, QCoreApplication.translate("LoginDlg", u"Design", None))

        self.labelModule.setText(QCoreApplication.translate("LoginDlg", u"Module", None))
        self.labelUsername.setText(QCoreApplication.translate("LoginDlg", u"Username", None))
        self.checkBox.setText(QCoreApplication.translate("LoginDlg", u"Read Only", None))
        self.buttonChange.setText(QCoreApplication.translate("LoginDlg", u"Change", None))
        self.labelProject.setText(QCoreApplication.translate("LoginDlg", u"Project", None))
        self.labelMdb.setText(QCoreApplication.translate("LoginDlg", u"MDB", None))
    # retranslateUi

    def createProject(self):
        subprocess.Popen("ProjectCreation.bat")
        self.reject()
    # createProject

    def projectChanged(self, theIndex):
        self.comboBoxUser.clear()
        self.comboBoxMdb.clear()

        aProject = PipeCad.Projects[theIndex]
        for aUser in aProject.UserList:
            self.comboBoxUser.addItem(aUser.Name)

        for aMdb in aProject.MdbList:
            self.comboBoxMdb.addItem(aMdb.Name)
    # projectChanged

    def passwordChanged(self):
        if len(self.lineEditPassword.text) > 0:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    # passwordChanged

    def changePassword(self):
        aIndex = self.comboBoxProject.currentIndex
        aUser = self.comboBoxUser.currentText
        aProject = PipeCad.Projects[aIndex]

        aPasswordDlg = PasswordDialog(aProject, aUser, self)
        aPasswordDlg.exec()
    # changePassword

    def reject(self):
        sys.exit()
    # reject
    
    def accept(self):
        aIndex = self.comboBoxProject.currentIndex
        aUser = self.comboBoxUser.currentText
        aMdb = self.comboBoxMdb.currentText
        aModule = self.comboBoxModule.currentText
        aPassword = self.lineEditPassword.text

        aProject = PipeCad.Projects[aIndex]

        aSession = aProject.CreateSession(aMdb, aUser, aPassword, aModule)
        if aSession is None:
            return

        QDialog.accept(self)
        
        PipeCad.Login()
    # accept


class PasswordDialog(QDialog):
    def __init__(self, theProject, theUser, parent = None):
        QDialog.__init__(self, parent)

        self.project = theProject
        self.user = theUser
        
        self.setupUi()

    # __init__

    def setupUi(self):
        #self.resize(330, 200)
        self.setWindowTitle(QT_TRANSLATE_NOOP("PipeCAD", "Change Password" ) )

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        self.labelCurrent = QLabel("Current Password")
        self.textCurrent = QLineEdit()
        self.textCurrent.setEchoMode(QLineEdit.Password)
        PipeCad.SetIndicator(self.textCurrent)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelCurrent)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textCurrent)

        self.labelNew = QLabel("New Password")
        self.textNew = QLineEdit("")
        self.textNew.setEchoMode(QLineEdit.Password)
        PipeCad.SetIndicator(self.textNew)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNew)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textNew)

        self.labelConfirm = QLabel("Confirm Password")
        self.textConfirm = QLineEdit()
        self.textConfirm.setEchoMode(QLineEdit.Password)
        PipeCad.SetIndicator(self.textConfirm)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelConfirm)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textConfirm)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)
    # setupUi

    def accept(self):
        aCurrent = self.textCurrent.text
        aNew = self.textNew.text
        aConfirm = self.textConfirm.text

        if aNew != aConfirm or (len(aNew) + len(aConfirm)) < 1:
            QMessageBox.critical(self, "", "The passwords you typed do not match!")
            return
        # if

        if self.project.ChangePassword(self.user, aCurrent, aNew):
            QMessageBox.information(self, "", "Password Changed!")
        else:
            return
        # if

        QDialog.accept(self)
    # accept
# PasswordDialog
