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
import omp
import omp.newproject

import os
import subprocess
from functools import partial
import sys


class LoginDialog(QDialog):
   
    def __init__(self, parent = None):    
        QDialog.__init__(self, parent)
        
        self.selectedProject = None
        self.projectDict = dict()
        self.projectIndex = 0
        project_users = []
              
          
        self.setupUi()
    # __init__

    def setupUi( self ):     
        self.resize(350, 300)
        self.setMaximumWidth(350)
        self.setMaximumHeight(300)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Login", "PipeCAD Login"))

        aCurrentPath = os.path.dirname(os.path.abspath(__file__))
        
        self.hBoxLayoutProjects = QHBoxLayout()
        self.hBoxLayoutProjects.setSpacing(2)
        
        self.groupButtonsProject = QButtonGroup()
        
        self.btnProjectPrevious = QPushButton( "", self)           
        self.btnProjectPrevious.setMinimumSize( 32 , 32 )
        self.btnProjectPrevious.setMaximumSize( 32 , 32 )
        #<a href="https://www.flaticon.com/free-icons/previous" title="previous icons">Previous icons created by Pixel perfect - Flaticon</a>
        self.btnProjectPrevious.setIcon( QIcon(aCurrentPath + '/icons/common/32x32_arrow_left.png') )
        self.btnProjectPrevious.setIconSize( QSize( 32 , 32 ) )
        self.btnProjectPrevious.setStyleSheet("border:none;")
        self.hBoxLayoutProjects.addWidget(self.btnProjectPrevious)
       
        aProject = PipeCad.Projects[self.projectIndex]
        self.btnProject = QPushButton( "", self)           
        self.btnProject.setMinimumSize( 312 , 104 )
        self.btnProject.setMaximumSize( 312 , 104 )
        #Icon downloaded from <a href="https://www.flaticon.com/free-icons/factory" title="factory icons">Factory icons created by vectorsmarket15 - Flaticon</a>
        self.btnProject.setIcon( QIcon(aCurrentPath + '/icons/login/128x128_select_project.png') )
        self.btnProject.setIconSize( QSize(96,96) )
        self.btnProject.setStyleSheet("QPushButton { text-align: left; }")
        self.btnProject.setText(QT_TRANSLATE_NOOP("Login", "Project: %s \nCode: %s \nNumber: %s \nDescription: \n%s") % (aProject.Name, aProject.Code, aProject.Number, aProject.Description))
        self.btnProject.setObjectName( aProject.Code )
        self.btnProject.setAutoDefault(False)

        self.hBoxLayoutProjects.addWidget(self.btnProject)  
        
        self.btnProjectNext = QPushButton( "", self)           
        self.btnProjectNext.setMinimumSize( 32 , 32 )
        self.btnProjectNext.setMaximumSize( 32 , 32 )
        #<a href="https://www.flaticon.com/free-icons/previous" title="previous icons">Previous icons created by Pixel perfect - Flaticon</a>
        self.btnProjectNext.setIcon( QIcon(aCurrentPath + '/icons/common/32x32_arrow_right.png') )
        self.btnProjectNext.setIconSize( QSize( 32 , 32 ) )
        self.btnProjectNext.setStyleSheet("border:none;")
        self.hBoxLayoutProjects.addWidget(self.btnProjectNext)

        self.buttonCreate = QPushButton(QT_TRANSLATE_NOOP("Login", "Create New Project"))        
        self.labelUsername = QLabel(QT_TRANSLATE_NOOP("Login", "Username"))
        self.comboBoxUser = QComboBox()
        self.comboBoxUser.setEditable(True)
        
        self.labelPassword = QLabel(QT_TRANSLATE_NOOP("Login", "Password"))
        self.lineEditPassword = QLineEdit( self )
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        
        PipeCad.SetIndicator( self.lineEditPassword )
            
        self.buttonChange = QPushButton(QT_TRANSLATE_NOOP("Login", "Change"))
        self.buttonChange.setMinimumSize( 120 , 26 )
        self.buttonChange.setMaximumSize( 120 , 26 )
        
        self.labelMdb = QLabel(QT_TRANSLATE_NOOP("Login", "MDB"))
        self.comboBoxMdb = QComboBox()
        self.comboBoxMdb.setEditable(True)
        
        self.checkBox = QCheckBox(QT_TRANSLATE_NOOP("Login", "Read Only"))
        
        self.verticalSpacer = QSpacerItem( 20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding )
        
        self.btnDesign = QPushButton( "", self )
        self.btnParagon = QPushButton( "", self )
        self.btnAdmin = QPushButton( "", self )
        
        self.btnDesign.setObjectName( "Design" )
        self.btnParagon.setObjectName( "Paragon" )
        self.btnAdmin.setObjectName( "Admin" )
                
        #<a href="https://www.flaticon.com/free-icons/worker" title="worker icons">Worker icons created by Freepik - Flaticon</a>
        self.btnDesign.setIcon( QIcon(aCurrentPath + '/icons/login/128x128_select_design.png') )
        
        #Icon downloaded from <a href="https://www.flaticon.com/free-icons/algorithm" title="algorithm icons">Algorithm icons created by Eucalyp - Flaticon</a>
        self.btnParagon.setIcon( QIcon(aCurrentPath + '/icons/login/128x128_select_paragon.png') )
        
        #Icon downloaded from <a href="https://www.flaticon.com/free-icons/data-processing" title="data processing icons">Data processing icons created by Eucalyp - Flaticon</a>
        self.btnAdmin.setIcon( QIcon(aCurrentPath + '/icons/login/128x128_select_admin.png') )
        
        self.btnDesign.setIconSize( QSize(96,96) )
        self.btnParagon.setIconSize( QSize(96,96) )
        self.btnAdmin.setIconSize( QSize(96,96) )
        
        self.btnDesign.setToolTip(QT_TRANSLATE_NOOP("Login", 'Module <b>Design</b>'))
        self.btnParagon.setToolTip(QT_TRANSLATE_NOOP("Login", 'Module <b>Paragon</b>'))
        self.btnAdmin.setToolTip(QT_TRANSLATE_NOOP("Login", 'Module <b>Admin</b>'))
                
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
       
        self.btnProjectPrevious.clicked.connect( self.setProjectPrevious )
        self.btnProjectNext.clicked.connect( self.setProjectNext )
        self.comboBoxUser.currentIndexChanged.connect( self.selectUser )
        self.buttonChange.clicked.connect( self.changePassword )
        self.groupButtonsModule.buttonClicked.connect( self.accept )
        self.buttonCreate.clicked.connect( self.createProject )
        #self.groupButtonsProject.buttonClicked.connect( self.selectProject )
        
        # Deactive widgets before selecting project 
        self.btnDesign.setEnabled(False)
        self.btnParagon.setEnabled(False)
        self.btnAdmin.setEnabled(False)
        self.btnProjectPrevious.setEnabled(False)
        
        self.selectProject()
            
    # setupUi
    
    def setProjectNext( self ):
        
        self.projectIndex = self.projectIndex + 1
      
        self.selectProject()
        
    def setProjectPrevious( self ):
        
        self.projectIndex = self.projectIndex - 1
                
        self.selectProject()                    
        
    def selectProject( self ):
        
        if len( PipeCad.Projects ) == 0 or len( PipeCad.Projects ) == 1:
            self.btnProjectPrevious.setEnabled(False)
            self.btnProjectNext.setEnabled(False)
            
        else:
            if self.projectIndex == 0:
                self.btnProjectPrevious.setEnabled(False)
                self.btnProjectNext.setEnabled(True)
            elif self.projectIndex > 0  and self.projectIndex < ( len( PipeCad.Projects ) - 1 ):
                self.btnProjectPrevious.setEnabled(True)
                self.btnProjectNext.setEnabled(True) 
            elif self.projectIndex == ( len( PipeCad.Projects ) - 1 ):   
                self.btnProjectPrevious.setEnabled(True)
                self.btnProjectNext.setEnabled(False) 

        aProject = PipeCad.Projects[self.projectIndex]
        self.btnProject.setText(QT_TRANSLATE_NOOP("Login", "Project: %s \nCode: %s \nNumber: %s \nDescription: \n%s") % (aProject.Name, aProject.Code, aProject.Number, aProject.Description))
        
        self.comboBoxUser.setEnabled(True)
        self.lineEditPassword.setEnabled(True)
        self.buttonChange.setEnabled(True)
        self.checkBox.setEnabled(True)
        
        self.comboBoxUser.clear()
        self.comboBoxMdb.clear()

        self.selectedProject = PipeCad.Projects[self.projectIndex]
        
        if self.selectedProject is None:
            return
        # if

        self.setWindowTitle(QT_TRANSLATE_NOOP("Login", "PipeCAD Login - Project %s") % self.selectedProject.Code)

        for aUser in self.selectedProject.UserList:
            self.comboBoxUser.addItem(aUser.Name)
        # for
        
        if len( self.selectedProject.MdbList ) == 0:
            self.comboBoxMdb.setEnabled(False)
            self.btnDesign.setEnabled(False)
            self.btnParagon.setEnabled(False)
        else:
            self.comboBoxMdb.setEnabled(True)
            self.btnDesign.setEnabled(True)
            self.btnParagon.setEnabled(True)
            
            for aMdb in self.selectedProject.MdbList:
                self.comboBoxMdb.addItem(aMdb.Name)
            # for
        # if
    # selectProject

    def selectUser(self):
        if self.comboBoxUser.currentText == "SYSTEM":
            self.btnParagon.setEnabled(True)
            self.btnAdmin.setEnabled(True)
        else:
            self.btnParagon.setEnabled(False)
            self.btnAdmin.setEnabled(False)
        # if
    # selectUser
        
    def accept( self, theButton ):

        if self.selectedProject is None:
            return
        # if

        aSession = self.selectedProject.CreateSession( self.comboBoxMdb.currentText, self.comboBoxUser.currentText, self.lineEditPassword.text, str(theButton.objectName)  )
        if aSession is None:
            return
        # if

        QDialog.accept(self)

        PipeCad.Login()
    # accept
 
    def createProject(self):
        #subprocess.Popen("ProjectCreation.bat")
        #self.reject()   
        omp.newproject.show()
    # createProject

    def changePassword(self):

        if self.selectedProject is None:
            return
        # if

        aUser = self.comboBoxUser.currentText

        aPasswordDlg = PasswordDialog(self.selectedProject, aUser, self)
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
        self.setWindowTitle(QT_TRANSLATE_NOOP("Login", "Change Password"))

        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        self.labelCurrent = QLabel(QT_TRANSLATE_NOOP("Login", "Current Password"))
        self.textCurrent = QLineEdit()
        self.textCurrent.setEchoMode(QLineEdit.Password)
        PipeCad.SetIndicator(self.textCurrent)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelCurrent)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textCurrent)

        self.labelNew = QLabel(QT_TRANSLATE_NOOP("Login", "New Password"))
        self.textNew = QLineEdit("")
        self.textNew.setEchoMode(QLineEdit.Password)
        PipeCad.SetIndicator(self.textNew)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelNew)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textNew)

        self.labelConfirm = QLabel(QT_TRANSLATE_NOOP("Login", "Confirm Password"))
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
            QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Login", "The passwords you typed do not match!"))
            return
        # if

        if self.project.ChangePassword(self.user, aCurrent, aNew):
            QMessageBox.information(self, "", QT_TRANSLATE_NOOP("Login", "Password Changed!"))
        else:
            return
        # if

        QDialog.accept(self)
    # accept
# PasswordDialog
