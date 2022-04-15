# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :: Welcome to PipeCad!                                      ::
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
# PipeCad - Piping Design Software.
# Copyright (C) 2021 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 21:16 2021-09-16


from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PipeCAD import *

import os
import subprocess
from functools import partial
import sys

class LoginDialog(QDialog):
   
    def __init__(self, parent = None):
    
        QDialog.__init__(self, parent)
        
        self.selected_project_code = ""
        #self.selected_project_button = QPushButton()
          
        self.setupUi()

    def setupUi( self ):
        
        self.widget = QWidget() 
        
        self.resize(350, 300)
        self.setWindowTitle(self.tr("PipeCad Login"))
        
        self.hBoxLayoutProjects = QHBoxLayout()
        self.hBoxLayoutProjects.setSpacing(2)
        #self.hBoxLayoutProjects.setContentsMargins(11, 11, 11, 11)
        
        self.groupButtonsProject = QButtonGroup()
        
        # self.btnProjectLeft = QPushButton( "", self)           
        # self.btnProjectLeft.setMinimumSize( 30 , 40 )
        # self.btnProjectLeft.setMaximumSize( 30 , 40 )
        # #<a href="https://www.flaticon.com/free-icons/previous" title="previous icons">Previous icons created by Pixel perfect - Flaticon</a>
        # self.btnProjectLeft.setIcon( QIcon('plugins/PipeCad/icons/login/128x128_arrow_left.png') )
        # self.btnProjectLeft.setIconSize( QSize( 30 , 40 ) )
        # self.btnProjectLeft.setAutoDefault(False)
        # self.hBoxLayoutProjects.addWidget(self.btnProjectLeft)
             
        for aProject in (PipeCad.Projects):
            self.btnProject = QPushButton( "", self)           
            self.btnProject.setMinimumSize( 256 , 104 )
            self.btnProject.setMaximumSize( 256 , 104 )
            #Icon downloaded from <a href="https://www.flaticon.com/free-icons/factory" title="factory icons">Factory icons created by vectorsmarket15 - Flaticon</a>
            self.btnProject.setIcon( QIcon('plugins/PipeCad/icons/login/128x128_select_project.png') )
            self.btnProject.setIconSize( QSize(96,96) )
            self.btnProject.setStyleSheet("QPushButton { text-align: left; }")
            self.btnProject.setText("   Project: " + aProject.Name + " \n   Code: " + aProject.Code + " \n   Number: " + aProject.Number + "\n   Description: " + aProject.Description )
            self.btnProject.setObjectName( aProject.Code )
            self.groupButtonsProject.addButton( self.btnProject )
            self.btnProject.setAutoDefault(False)
            self.btnProject.clicked.connect( self.select_project )
            self.hBoxLayoutProjects.addWidget( self.btnProject )
        
        # self.btnProjectRight = QPushButton( "", self)           
        # self.btnProjectRight.setMinimumSize( 30 , 40 )
        # self.btnProjectRight.setMaximumSize( 30 , 40 )
        # #<a href="https://www.flaticon.com/free-icons/previous" title="previous icons">Previous icons created by Pixel perfect - Flaticon</a>
        # self.btnProjectRight.setIcon( QIcon('plugins/PipeCad/icons/login/128x128_arrow_right.png') )
        # self.btnProjectRight.setIconSize( QSize( 30 , 40 ) )
        # self.btnProjectRight.setAutoDefault(False)
        # self.hBoxLayoutProjects.addWidget(self.btnProjectRight)

        self.buttonCreate = QPushButton(self.tr("Create New Project"))        
        self.labelUsername = QLabel(self.tr("Username"))
        self.labelUsername.setFont( QFont('Times', 12) )
        self.comboBoxUser = QComboBox()
        self.comboBoxUser.setEditable(True)
        
        self.labelPassword = QLabel(self.tr("Password"))
        self.labelPassword.setFont( QFont('Times', 12) )
        self.lineEditPassword = QLineEdit( self )
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        
        PipeCad.SetIndicator(self.lineEditPassword)
            
        self.buttonChange = QPushButton(self.tr("Change"))
        
        self.labelMdb = QLabel(self.tr("MDB"))
        self.labelMdb.setFont( QFont('Times', 12) )
        self.comboBoxMdb = QComboBox()
        self.comboBoxMdb.setEditable(True)
        
        self.checkBox = QCheckBox(self.tr("Read Only"))
        
        self.verticalSpacer = QSpacerItem( 20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding )
        
        self.btnDesign = QPushButton( "", self )
        self.btnParagon = QPushButton( "", self )
        self.btnAdmin = QPushButton( "", self )
        
        self.btnDesign.setObjectName( "Design" )
        self.btnParagon.setObjectName( "Paragon" )
        self.btnAdmin.setObjectName( "Admin" )
                
        #<a href="https://www.flaticon.com/free-icons/worker" title="worker icons">Worker icons created by Freepik - Flaticon</a>
        self.btnDesign.setIcon( QIcon('plugins/PipeCad/icons/login/128x128_select_design.png') )
        
        #Icon downloaded from <a href="https://www.flaticon.com/free-icons/algorithm" title="algorithm icons">Algorithm icons created by Eucalyp - Flaticon</a>
        self.btnParagon.setIcon( QIcon('plugins/PipeCad/icons/login/128x128_select_paragon.png') )
        
        #Icon downloaded from <a href="https://www.flaticon.com/free-icons/data-processing" title="data processing icons">Data processing icons created by Eucalyp - Flaticon</a>
        self.btnAdmin.setIcon( QIcon('plugins/PipeCad/icons/login/128x128_select_admin.png') )
        
        self.btnDesign.setIconSize( QSize(96,96) )
        self.btnParagon.setIconSize( QSize(96,96) )
        self.btnAdmin.setIconSize( QSize(96,96) )
        
        self.btnDesign.setToolTip('Module <b>Design</b>')
        self.btnParagon.setToolTip('Module <b>Paragon</b>')
        self.btnAdmin.setToolTip('Module <b>Admin</b>')
                
        #Setup Widgets Layout
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.labelUsername, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBoxUser, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.labelPassword, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEditPassword, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.buttonChange, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.labelMdb, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBoxMdb, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.checkBox, 2, 2, 1, 1)
               
        self.horBoxLayoutModules = QHBoxLayout()
        self.horBoxLayoutModules.addWidget( self.btnDesign )
        self.horBoxLayoutModules.addWidget( self.btnParagon )
        self.horBoxLayoutModules.addWidget( self.btnAdmin )
        
        self.groupButtonsModule = QButtonGroup()
        self.groupButtonsModule.addButton( self.btnDesign )
        self.groupButtonsModule.addButton( self.btnParagon )
        self.groupButtonsModule.addButton( self.btnAdmin )
        
        self.verticalLayout = QVBoxLayout( self )
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)  
        self.verticalLayout.addLayout(self.hBoxLayoutProjects)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.verticalLayout.addLayout(self.horBoxLayoutModules)
        self.verticalLayout.addWidget(self.buttonCreate)
        
        self.labelSoftwareVersion = QLabel( "v. " + PipeCad.GetVersion() )
        self.labelSoftwareVersion.setAlignment(Qt.AlignRight)
        self.verticalLayout.addWidget(self.labelSoftwareVersion)
       
        self.comboBoxUser.currentIndexChanged.connect( self.select_user )
        self.buttonChange.clicked.connect( self.changePassword )
        self.groupButtonsModule.buttonClicked.connect( self.accept )
        self.buttonCreate.clicked.connect( self.createProject )
        self.groupButtonsProject.buttonClicked.connect( self.select_project )
        
        # Deactive widgets before selecting project 
        self.comboBoxUser.setEnabled(False)
        self.lineEditPassword.setEnabled(False)
        self.buttonChange.setEnabled(False)
        self.comboBoxMdb.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.btnDesign.setEnabled(False)
        self.btnParagon.setEnabled(False)
        self.btnAdmin.setEnabled(False)
        
        
    def select_project( self, id ):
        self.comboBoxUser.setEnabled(True)
        self.lineEditPassword.setEnabled(True)
        self.buttonChange.setEnabled(True)
        self.checkBox.setEnabled(True)
        
        self.comboBoxUser.clear()
        self.comboBoxMdb.clear()
        for Project in PipeCad.Projects:
            if Project.Code == id.objectName:
                self.selected_project_code = Project.Code
                self.setWindowTitle(self.tr("PipeCad Login - Project " + Project.Code))                
                for aUser in Project.UserList:
                    self.comboBoxUser.addItem(aUser.Name)
                
                if len(Project.MdbList) == 0:
                    self.comboBoxMdb.setEnabled(False)
                    self.btnDesign.setEnabled(False)
                    self.btnParagon.setEnabled(False)
                else:
                    self.comboBoxMdb.setEnabled(True)
                    self.btnDesign.setEnabled(True)
                    self.btnParagon.setEnabled(True)
                    
                    for aMdb in Project.MdbList:
                        self.comboBoxMdb.addItem(aMdb.Name)
                        
    def select_user( self, index ):       
        if self.comboBoxUser.currentText == "SYSTEM":
            self.btnParagon.setEnabled(True)
            self.btnAdmin.setEnabled(True)
        else:
            self.btnParagon.setEnabled(False)
            self.btnAdmin.setEnabled(False)
        
    def accept( self, id ):
        print(self.selected_project_code)
        for Project in PipeCad.Projects:
            if Project.Code == self.selected_project_code:
                #CreateSession(aMdb, aUser, aPassword, aModule)
                aSession = Project.CreateSession( self.comboBoxMdb.currentText, self.comboBoxUser.currentText, self.lineEditPassword.text, str(id.objectName) )
                if aSession is None:
                    return
                
                QDialog.accept( self )
                PipeCad.Login()
 
    def createProject(self):
        subprocess.Popen("ProjectCreation.bat")
        self.reject()
    # createProject

    def changePassword(self):
        aUser = self.comboBoxUser.currentText
        for Project in PipeCad.Projects:
            if Project.Code == self.selected_project_code:
                aPasswordDlg = PasswordDialog( Project, aUser, self )
                aPasswordDlg.exec()  

    # changePassword
    
class PasswordDialog(QDialog):
   
    def __init__(self, theProject, theUser, parent = None):
        QDialog.__init__(self, parent)

        self.project = theProject
        self.user = theUser
        
        self.setupUi()

    # __init__

    def setupUi(self):
        #self.resize(330, 200)
        self.setWindowTitle(self.tr("Change Password"))

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