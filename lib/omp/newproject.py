from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

import os
import subprocess
from functools import partial
import sys

class NewProjectDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.ColumnsHeaders = []
        self.setupUi()
    # __init__

    def setupUi(self):
        
        self.resize(500, 400)
        self.setWindowTitle(self.tr("PipeCAD - Create New Project"))
        
        self.vBoxLayMain = QVBoxLayout(self)        
        
        self.groupProjectDetails = QGroupBox("Project Details")        
        self.gridProjectDetails = QGridLayout()
        self.groupProjectDetails.setLayout(self.gridProjectDetails)
        
        # Folders Code
        # 000, iso, dflts, tmpls, reports
        # Advanced Settings in stack 
        # project Variable 
        # check Additional Scripts
        # check Import Project Definition
        # check ActiveDirectory Autorisation
        
        self.hBoxLayProjectPath = QHBoxLayout()
        self.lblProjectPath = QLabel("Path")
        
        self.txtProjectPath = QLineEdit( os.getenv('PROJECTS_DIR') )       
        self.btnProjectPath = QPushButton( "...", self)           
        self.btnProjectPath.setMinimumSize( 32 , 24 )
        self.btnProjectPath.setMaximumSize( 32 , 24 )
        
        self.hBoxLayProjectPath.addWidget(self.txtProjectPath) 
        self.hBoxLayProjectPath.addWidget(self.btnProjectPath) 
        
        self.lblProjectNumber = QLabel("Number")
        self.txtProjectNumber = QLineEdit("")       
        
        self.lblProjectCode = QLabel("Code")
        self.txtProjectCode = QLineEdit("")

        self.lblProjectName = QLabel("Name")
        self.txtProjectName = QLineEdit("") 

        self.lblProjectDescription = QLabel("Description")
        self.txtProjectDescription = QLineEdit("")
 
        self.btnProjectLogo = QPushButton( "", self)           
        self.btnProjectLogo.setMinimumSize( 128 , 128 )
        self.btnProjectLogo.setMaximumSize( 128 , 128 )
        ##Icon downloaded from <a href="https://www.flaticon.com/free-icons/factory" title="factory icons">Factory icons created by vectorsmarket15 - Flaticon</a>
        aCurrentPath = os.path.dirname(os.path.abspath(__file__)).replace("\lib\omp","\lib\pipecad")

        self.btnProjectLogo.setIcon( QIcon( aCurrentPath + '/icons/login/128x128_select_project.png' ) )
        self.btnProjectLogo.setIconSize( QSize( 128, 128 ) )
       
        self.gridProjectDetails.addWidget( self.lblProjectPath, 0, 0 )
        self.gridProjectDetails.addLayout( self.hBoxLayProjectPath, 0, 1, 1, 3 )
        
        self.gridProjectDetails.addWidget( self.lblProjectNumber, 1, 0 )
        self.gridProjectDetails.addWidget( self.txtProjectNumber, 1, 1 )
              
        self.gridProjectDetails.addWidget( self.lblProjectCode, 2, 0 )
        self.gridProjectDetails.addWidget( self.txtProjectCode, 2, 1 ) 
                    
        self.gridProjectDetails.addWidget( self.lblProjectName, 3, 0 )
        self.gridProjectDetails.addWidget( self.txtProjectName, 3, 1 )
                    
        self.gridProjectDetails.addWidget( self.lblProjectDescription, 4, 0 )
        self.gridProjectDetails.addWidget( self.txtProjectDescription, 4, 1 )
                
        self.gridProjectDetails.addWidget( self.btnProjectLogo, 1, 3, 4, 1 )
        
        self.btnRunNewProject = QPushButton( QT_TRANSLATE_NOOP( "Admin", "Create" ))

        self.tablePreview = QTableWidget()
        self.tablePreview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablePreview.setAlternatingRowColors(True)
        self.tablePreview.setGridStyle(Qt.SolidLine)
        self.tablePreview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablePreview.horizontalHeader().setStretchLastSection(True)
        self.tablePreview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tablePreview.setColumnCount(2)
        self.tablePreview.setHorizontalHeaderLabels([ "Name", "Value" ])   
        self.tablePreview.horizontalHeader().setMinimumSectionSize(100)
               
        self.btnRunNewProject.clicked.connect(self.callRunNewProject)
            
        self.vBoxLayMain.addWidget(self.groupProjectDetails)  
        self.vBoxLayMain.addWidget(self.tablePreview)  
        self.vBoxLayMain.addWidget(self.btnRunNewProject)  
    # setupUi
    
        
    def callRunNewProject(self):
        os.mkdir("C:/PipeCAD/Projects/Tester")

        aDatabase = QSqlDatabase.addDatabase("QSQLITE", "TST_DB")
        aDatabase.setDatabaseName("Projects/Tester/tstsys")
        aDatabase.open()
        aDatabase.exec_("CREATE TABLE db (refno TEXT PRIMARY KEY REFERENCES item (refno) ON DELETE CASCADE ON UPDATE CASCADE, number INTEGER, area INTEGER, type TEXT, description TEXT, access TEXT, claim TEXT);")
        aDatabase.exec_("CREATE TABLE dbl (refno TEXT PRIMARY KEY REFERENCES item (refno) ON DELETE CASCADE ON UPDATE CASCADE, owner TEXT, dbref TEXT);")
        aDatabase.exec_("CREATE TABLE dbli (refno TEXT PRIMARY KEY REFERENCES item (refno) ON DELETE CASCADE ON UPDATE CASCADE, description TEXT);")
        aDatabase.exec_("CREATE TABLE info (dbnum INTEGER PRIMARY KEY, bucket INTEGER, nextid INTEGER DEFAULT (0), type TEXT, version TEXT);")
        aDatabase.exec_("CREATE TABLE team (refno TEXT PRIMARY KEY REFERENCES item (refno) ON DELETE CASCADE ON UPDATE CASCADE, description TEXT, access_status INTEGER DEFAULT (0));")
        aDatabase.exec_("CREATE TABLE tmli (refno TEXT PRIMARY KEY REFERENCES item (refno) ON DELETE CASCADE ON UPDATE CASCADE, description TEXT);")
        aDatabase.exec_("CREATE TABLE user (refno TEXT PRIMARY KEY REFERENCES item (refno) ON DELETE CASCADE ON UPDATE CASCADE, password TEXT, security TEXT, description TEXT);")
        
        # Types dictionary 


# Singleton Instance.
aNewProjectDialog = NewProjectDialog(PipeCad)

def showNewProject():
    aNewProjectDialog.show()
# Show
