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
from PythonQt.QtSql import *

from pipecad import *

import pandas as pd 

import os

class AdminMain(QWidget):
    """docstring for AdminMain"""
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.teamDialog = TeamDialog(self)
        self.userDialog = UserDialog(self)
        self.mdbDialog = MdbDialog(self)
        self.dbDialog = DatabaseDialog(self)
               
        self.setupUi()

    # __init__

    def setupUi(self):
               
        self.verticalLayout = QVBoxLayout(self)

        aCurrentPath = os.path.dirname( os.path.abspath(__file__) )

        self.horizontalLayout = QHBoxLayout()

        self.labelElements = QLabel(QT_TRANSLATE_NOOP("Admin", "Elements"))
        self.horizontalLayout.addWidget(self.labelElements)

        self.comboElements = QComboBox()
        self.comboElements.addItem(QIcon(aCurrentPath + "/icons/admin/128x128_team_select.png"), QT_TRANSLATE_NOOP("Admin", "Teams"), "Team")
        self.comboElements.addItem(QIcon(aCurrentPath + "/icons/admin/128x128_user_select.png"), QT_TRANSLATE_NOOP("Admin", "Users"), "User")
        self.comboElements.addItem(QIcon(aCurrentPath + "/icons/admin/128x128_database_select.png"), QT_TRANSLATE_NOOP("Admin", "Databases"), "Database")
        self.comboElements.addItem(QIcon(aCurrentPath + "/icons/admin/128x128_mdb_select.png"), QT_TRANSLATE_NOOP("Admin", "MDBs"), "MDB")

        aSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comboElements.setSizePolicy(aSizePolicy)

        self.comboElements.currentIndexChanged.connect(self.elementChanged)

        self.horizontalLayout.addWidget(self.comboElements)

        self.buttonRefresh = QPushButton(QT_TRANSLATE_NOOP("Admin", "Refresh List"))
        self.horizontalLayout.addWidget(self.buttonRefresh)

        self.buttonRefresh.clicked.connect(self.refreshList)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.currentItemChanged.connect(self.currentItemChanged)
        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()

        self.buttonSort = QPushButton(QT_TRANSLATE_NOOP("Admin", "Sort"))
        self.horizontalLayout.addWidget(self.buttonSort)
        self.buttonSort.clicked.connect(self.sortList)

        self.comboSort = QComboBox()
        self.comboSort.addItem(QT_TRANSLATE_NOOP("Admin", "Name"))
        self.comboSort.addItem(QT_TRANSLATE_NOOP("Admin", "Description"))
        self.comboSort.setSizePolicy(aSizePolicy)
        self.horizontalLayout.addWidget(self.comboSort)

        self.labelFilter = QLabel(QT_TRANSLATE_NOOP("Admin", "Filter"))
        self.horizontalLayout.addWidget(self.labelFilter)

        self.lineFilter = QLineEdit("*")
        self.horizontalLayout.addWidget(self.lineFilter)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupOption = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Operations"))
        self.verticalLayout.addWidget(self.groupOption)        
        
        self.verticalLayout = QVBoxLayout(self.groupOption)

        self.horizontalLayout = QHBoxLayout()

        self.buttonCreate = QPushButton(QT_TRANSLATE_NOOP("Admin", "Create"))
        self.buttonCreate.clicked.connect(self.create)
        self.horizontalLayout.addWidget(self.buttonCreate)

        self.buttonCopy = QPushButton(QT_TRANSLATE_NOOP("Admin", "Copy"))
        self.buttonCopy.clicked.connect(self.copy)
        self.horizontalLayout.addWidget(self.buttonCopy)

        self.buttonModify = QPushButton(QT_TRANSLATE_NOOP("Admin", "Modify"))
        self.buttonModify.clicked.connect(self.modify)
        self.horizontalLayout.addWidget(self.buttonModify)

        self.buttonDelete = QPushButton(QT_TRANSLATE_NOOP("Admin", "Delete"))
        self.buttonDelete.clicked.connect(self.delete)
        self.horizontalLayout.addWidget(self.buttonDelete)
        
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.statItem = PipeCad.GetItem("/*S")
        self.tmwlItem = PipeCad.GetItem("/*T")
        self.uswlItem = PipeCad.GetItem("/*U")
        self.mdbwItem = PipeCad.GetItem("/*M")

    # setupUi
        
    def elementChanged(self, theIndex):
        aElement = self.comboElements.currentData

        if aElement.startswith("Team"):
            self.buildTeamList()
        elif aElement.startswith("User"):
            self.buildUserList()
        elif aElement.startswith("Database"):
            self.buildDbList()
        elif aElement.startswith("MDB"):
            self.buildMdbList()
        # if

        #self.tableWidget.resizeColumnsToContents()
    # elementChanged

    def currentItemChanged(self):
        aRow = self.tableWidget.currentRow()
        aItem = self.tableWidget.item(aRow, 0)
        if aItem is not None:
            PipeCad.SetCurrentItem(aItem.data(Qt.UserRole))
        # if
    # currentItemChanged

    def buildTeamList(self):
        aRow = 0
        aHeaderLabels = [QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Description")]

        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)

        if self.tmwlItem == None:
            return

        aTeamItems = self.tmwlItem.Member
        for aTeamItem in aTeamItems:
            aItem = QTableWidgetItem(QT_TRANSLATE_NOOP("Admin", "<TEAM> %s") % aTeamItem.Name[1:])
            aItem.setData(Qt.UserRole, aTeamItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aTeamItem.Description))
            aRow += 1

    # buildTeamList

    def buildUserList(self):
        aRow = 0
        aHeaderLabels = [QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Security"), QT_TRANSLATE_NOOP("Admin", "Description")]
        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)
        
        if self.uswlItem == None:
            return
        # if

        aUserItems = self.uswlItem.Member
        for aUserItem in aUserItems:
            aItem = QTableWidgetItem(QT_TRANSLATE_NOOP("Admin", "<USER> %s") % aUserItem.Name)
            aItem.setData(Qt.UserRole, aUserItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aUserItem.Security))
            self.tableWidget.setItem(aRow, 2, QTableWidgetItem(aUserItem.Description))
            aRow += 1

    # buildUserList

    def buildMdbList(self):
        aRow = 0
        aHeaderLabels = [QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Description")]
        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)
        
        if self.mdbwItem == None:
            return

        aMdbItems = self.mdbwItem.Member
        for aMdbItem in aMdbItems:
            aItem = QTableWidgetItem(QT_TRANSLATE_NOOP("Admin", "<MDB> %s") % aMdbItem.Name)
            aItem.setData(Qt.UserRole, aMdbItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aMdbItem.Description))
            aRow += 1

    # buildMdbList

    def buildDbList(self):
        aRow = 0
        aHeaderLabels = [QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Type"), QT_TRANSLATE_NOOP("Admin", "DB Number"), QT_TRANSLATE_NOOP("Admin", "Description")]
        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)
        
        if self.tmwlItem == None:
            return

        aDbItems = PipeCad.CollectItem("DB")
        for aDbItem in aDbItems:
            aItem = QTableWidgetItem(QT_TRANSLATE_NOOP("Admin", "<DB> %s") % aDbItem.Name[1:])
            aItem.setData(Qt.UserRole, aDbItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aDbItem.DbType))
            self.tableWidget.setItem(aRow, 2, QTableWidgetItem( ( '    ' + str(aDbItem.DbNumber))[-4:]))
            self.tableWidget.setItem(aRow, 3, QTableWidgetItem(aDbItem.Description))
            aRow += 1
        # for

    # buildDbList

    def refreshList(self):
        aElement = self.comboElements.currentText
        self.elementChanged(aElement)
    # refreshList

    def sortList(self):
        aIndex = self.comboSort.currentIndex
        self.tableWidget.sortItems(aIndex)
    # sortList

    def create(self):
        aElement = self.comboElements.currentData
        if aElement.startswith("Team"):
            self.teamDialog.create()
        elif aElement.startswith("User"):
            self.userDialog.create()
        elif aElement.startswith("Database"):
            self.dbDialog.create()
        elif aElement.startswith("MDB"):
            self.mdbDialog.create()
        # if
    # create

    def copy(self):
        print("copy")
    # copy

    def modify(self):
        aElement = self.comboElements.currentData
        if aElement.startswith("Team"):
            self.teamDialog.modify()
        elif aElement.startswith("User"):
            self.userDialog.modify()
        elif aElement.startswith("Database"):
            self.dbDialog.modify()
        elif aElement.startswith("MDB"):
            self.mdbDialog.modify()
        # if

    # modify

    def delete(self):
        aItem = PipeCad.CurrentItem()
        aElement = self.comboElements.currentData
        if aElement.startswith("Team"):
            aReply = QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Admin", "Okay to delete team %s") % aItem.Name[1:])
            if aReply == QMessageBox.Yes:
                PipeCad.DeleteItem("TEAM")
                self.buildTeamList()
            # if
        elif aElement.startswith("User"):
            aReply = QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Admin", "Okay to delete user %s") % aItem.Name)
            if aReply == QMessageBox.Yes:
                PipeCad.DeleteItem("USER")
                self.buildUserList()
            # if
        elif aElement.startswith("Database"):
            aReply = QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Admin", "Okay to delete database %s") % aItem.Name[1:])
            if aReply == QMessageBox.Yes:
                aItem.DeleteDatabase()
                PipeCad.DeleteItem("DB")
                self.buildDbList()
            # if
        elif aElement.startswith("MDB"):
            aReply = QMessageBox.question(self, "", QT_TRANSLATE_NOOP("Admin", "Okay to delete mdb %s") % aItem.Name)
            if aReply == QMessageBox.Yes:
                PipeCad.DeleteItem("MDB")
                self.buildMdbList()
            # if
        # if

        PipeCad.SaveWork()
    # delete
    
    def update(self):
        self.importProjectInfo.showImportExcel()

class ImportProjectDialog(QDialog):
    """docstring for ImportProjectDialog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
        
    def setupUi(self):
        
        self.aProgressBar = QProgressBar()
        self.aProgressBar.hide()
        
        self.aStatusBar = PipeCad.statusBar()
        self.aStatusBar.addPermanentWidget( self.aProgressBar )
        
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Import Project"))
        self.resize(450, 150)
        
        self.aCurrentPath = os.path.dirname( os.path.abspath(__file__) )
        
        self.txtPathToFile = QLineEdit("")
        
        self.btnExplorer = QPushButton( "", self) 
        self.btnExplorer.setMinimumSize( 32 , 32 )
        self.btnExplorer.setMaximumSize( 32 , 32 )
        self.btnExplorer.setIcon( QIcon(':/PipeCad/Resources/CATA.png') )
        self.btnExplorer.setIconSize( QSize( 32, 32 ) )
       
        self.icon_users = QLabel()
        self.icon_teams = QLabel()
        self.icon_dbs = QLabel()
        self.icon_mdbs = QLabel()     
        
        self.icon_users_counter = QLabel()
        self.icon_teams_counter = QLabel()
        self.icon_dbs_counter = QLabel()
        self.icon_mdbs_counter = QLabel()  
            
        self.icon_users.setStyleSheet("border: 0.5px solid grey;")
        self.icon_teams.setStyleSheet("border: 0.5px solid grey;")
        self.icon_dbs.setStyleSheet("border: 0.5px solid grey;")
        self.icon_mdbs.setStyleSheet("border: 0.5px solid grey;")
                
        self.icon_users.setAlignment(Qt.AlignCenter)
        self.icon_teams.setAlignment(Qt.AlignCenter)
        self.icon_dbs.setAlignment(Qt.AlignCenter)
        self.icon_mdbs.setAlignment(Qt.AlignCenter)    
        
        self.icon_users_counter.setAlignment(Qt.AlignCenter)
        self.icon_teams_counter.setAlignment(Qt.AlignCenter)
        self.icon_dbs_counter.setAlignment(Qt.AlignCenter)
        self.icon_mdbs_counter.setAlignment(Qt.AlignCenter)
        
        self.icon_teams.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_team_select.png' ).scaled( QSize( 128, 128 ) ) )
        self.icon_users.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_user_select.png'  ).scaled( QSize( 128, 128 ) ) )
        self.icon_dbs.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_database_select.png' ).scaled( QSize( 128, 128 ) ) )
        self.icon_mdbs.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_mdb_select.png' ).scaled( QSize( 128, 128 ) ) )
        
        self.hLayPath = QHBoxLayout()
        self.hLayPath.addWidget(self.txtPathToFile)
        self.hLayPath.addWidget(self.btnExplorer)
        
        self.hLayIcons = QHBoxLayout()
        self.hLayIcons.setAlignment(Qt.AlignVCenter) 
        self.hLayIcons.addWidget(self.icon_teams)  
        self.hLayIcons.addWidget(self.icon_users) 
        self.hLayIcons.addWidget(self.icon_dbs)  
        self.hLayIcons.addWidget(self.icon_mdbs)  
        self.hLayIcons.setContentsMargins(0, 0, 0, 0) 
        
        self.hLayCounters = QHBoxLayout()
        self.hLayCounters.addWidget(self.icon_teams_counter)  
        self.hLayCounters.addWidget(self.icon_users_counter) 
        self.hLayCounters.addWidget(self.icon_dbs_counter)  
        self.hLayCounters.addWidget(self.icon_mdbs_counter)  
        self.hLayCounters.setContentsMargins(0, 0, 0, 0)
        
        self.icon_users_counter.hide()
        self.icon_teams_counter.hide()
        self.icon_dbs_counter.hide()
        self.icon_mdbs_counter.hide()
                  
        self.vLayMain = QVBoxLayout(self)
        self.vLayMain.addLayout(self.hLayPath)
        self.vLayMain.addLayout(self.hLayIcons)
        self.vLayMain.addLayout(self.hLayCounters)
        
        self.btnExplorer.clicked.connect(self.run_import)
                
    def run_import(self):

        #self.collect_reserved_db_numbers()

        aProjectsDir = QCoreApplication.applicationDirPath() + "/templates"
        excel_path = QFileDialog.getOpenFileName( self, 'Import Project Definition', aProjectsDir, "Excel file (*.xlsx)" )
        if len(excel_path) < 1:
            return
        # if
        
        self.txtPathToFile.setText( excel_path.replace("/","\\") ) 
                      
        df_users = pd.read_excel( excel_path, 'Users' ).rename ( columns=lambda x: x.replace(' ', '_') )
        df_teams = pd.read_excel( excel_path, 'Teams' ).rename ( columns=lambda x: x.replace(' ', '_') )
        df_dbs = pd.read_excel( excel_path, 'Databases' ).rename ( columns=lambda x: x.replace(' ', '_') )
        df_mdbs = pd.read_excel( excel_path, 'MDBs' ).rename ( columns=lambda x: x.replace(' ', '_') )
        
        df_users_max = len(df_users)
        df_teams_max = len(df_teams)
        df_dbs_max = len(df_dbs)
        df_mdbs_max = len(df_mdbs)
                
        common_max = df_users_max + df_teams_max + df_dbs_max + df_mdbs_max
        current_progress = 0
        
        loaded_users = 0
        loaded_teams = 0
        loaded_dbs = 0
        loaded_mdbs = 0
        
        self.aProgressBar.show()
                
        # Importing Teams
        PipeCad.StartTransaction("Importing Teams")
        for i in range(len(df_teams)):   
            team_name = df_teams.iloc[i].Name
            team_description = df_teams.iloc[i].Description
                    
            try: 
                PipeCad.SetCurrentItem( '/*' + team_name )
               
            except NameError as e:
                PipeCad.CreateTeam( team_name, team_description )
            
            loaded_teams = loaded_teams + 1
            
            current_team = PipeCad.CurrentItem()
            current_team.Description = team_description    
            
            current_progress = i / common_max * 100
            self.aProgressBar.setValue( current_progress )         
        
        if loaded_teams == df_teams_max:
            self.icon_teams.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_team_done.png' ).scaled( QSize( 128, 128 ) ) )
        else: 
            self.icon_teams.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_team_fail.png' ).scaled( QSize( 128, 128 ) ) )
        
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
         
        # Importing Users 
        PipeCad.StartTransaction("Importing Users")        
        for i in range(len(df_users)):
            user_name = df_users.iloc[i].Name
            user_description = df_users.iloc[i].Description
            user_security = df_users.iloc[i].Security
            user_password = df_users.iloc[i].Password
            user_teams = sorted( set( df_users.iloc[i].Teams.split() ) )

            list_user_teams = []    
            
            for i in range ( len( user_teams ) ):
                user_team = PipeCad.SetCurrentItem( "/*" + user_teams[i] )
                user_team_ref = PipeCad.CurrentItem()               
                list_user_teams.append( user_team_ref )
            
            # Delete Teams of current user to avoid duplicating of Teams
            try:
                PipeCad.SetCurrentItem( '/' + user_name )
                current_user_teams = PipeCad.CurrentItem().Member[0].Member
                for current_user_team in current_user_teams:
                    PipeCad.SetCurrentItem( current_user_team )
                    PipeCad.DeleteItem("LTEA")
            except NameError as e:
                PipeCad.CreateUser( user_name, user_description, user_password, user_security, list_user_teams )
            
            try: 
                PipeCad.SetCurrentItem( '/' + user_name )
                current_user = PipeCad.CurrentItem()
                current_user.Password = user_password
                current_user.Description = user_description
                current_user.Security = user_security
                current_user.JoinTeam( list_user_teams )

            except NameError as e:
                PipeCad.CreateUser( user_name, user_description, user_password, user_security, list_user_teams )   
                           
            loaded_users = loaded_users + 1                  
            current_progress = ( i + df_teams_max ) / common_max * 100
            self.aProgressBar.setValue( current_progress ) 
        
        if loaded_users == df_users_max:
            self.icon_users.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_user_done.png' ).scaled( QSize( 128, 128 ) ) )
        else: 
            self.icon_users.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_user_fail.png' ).scaled( QSize( 128, 128 ) ) )

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()

        # Importing Databases   
        for i in range(len(df_dbs)):
            db_team = df_dbs.iloc[i].Owning_Team
            db_name = df_dbs.iloc[i].Name
            db_description = df_dbs.iloc[i].Description
            db_type = df_dbs.iloc[i].Type
            db_claim_mode = df_dbs.iloc[i].Claim_Mode
            db_number = df_dbs.iloc[i].Number
            db_main_element = df_dbs.iloc[i].Main_Element
            # db_area = db_dbs.iloc[i].Area
            
            if db_type == 'DESI' or db_type == 'CATA':            
                if db_number > 0 and db_number < 8000:
                    try: 
                        PipeCad.SetCurrentItem( '/*' + db_team + '/' + db_name )
                        current_db = PipeCad.CurrentItem()
                        current_db.Description = db_description
                        current_db.ClaimMode = db_claim_mode 
                        PipeCad.SaveWork()                        
                        
                    except NameError as e:
                        PipeCad.StartTransaction("Create Database")
                        PipeCad.CreateDb( db_team + '/' + db_name , db_type, db_number, db_description )  # TODO: Add check if required db number is availible for assigning
                        current_db = PipeCad.CurrentItem()
                        current_db.CreateDbElement( db_main_element )
                        current_db.ClaimMode = db_claim_mode  
                        PipeCad.CommitTransaction()
                        PipeCad.SaveWork()
                    
                    loaded_dbs = loaded_dbs + 1
                    
                else:
                    continue
            else:
                continue
                        
            current_progress = ( i + df_users_max + df_teams_max ) / common_max * 100
            self.aProgressBar.setValue( current_progress ) 
                    
        if loaded_dbs == df_dbs_max:
            self.icon_dbs.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_database_done.png' ).scaled( QSize( 128, 128 ) ) )
        else: 
            self.icon_dbs.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_database_fail.png' ).scaled( QSize( 128, 128 ) ) )
                
        # Importing MDBs
        PipeCad.StartTransaction("Importing MDBs")
        for i in range(len(df_mdbs)):
            mdb_name = df_mdbs.iloc[i].Name
            mdb_description = df_mdbs.iloc[i].Description
            mdb_dbs = df_mdbs.iloc[i].Databases.split()
                    
            try: 
                PipeCad.SetCurrentItem( '/' + mdb_name )
                mdb_dbs = PipeCad.CurrentItem().Member
                
                for i in range ( len( mdb_dbs ) ):
                    PipeCad.SetCurrentItem( mdb_dbs[i] )
                    PipeCad.DeleteItem("DBL")
               
            except NameError as e:
                PipeCad.CreateMdb( mdb_name, mdb_description )
            
            loaded_mdbs = loaded_mdbs + 1
            
            current_mdb = PipeCad.CurrentItem()
            current_mdb.Description = mdb_description    

            for i in range ( len( mdb_dbs )):
                PipeCad.CreateItem("DBL")
                mdb_dbl = PipeCad.CurrentItem()

                if isinstance(mdb_dbs[i], str):
                    mdb_db = PipeCad.SetCurrentItem( "/*" + mdb_dbs[i] )
                else:
                    mdb_db = PipeCad.SetCurrentItem( mdb_dbs[i] )

                mdb_db_ref = PipeCad.CurrentItem()
                                
                PipeCad.SetCurrentItem( mdb_dbl )
                mdb_dbl = PipeCad.CurrentItem()
                
                mdb_dbl.Dbref = mdb_db_ref

            current_progress = i / common_max * 100
            self.aProgressBar.setValue( current_progress )   
            
            current_progress = ( i + df_users_max + df_teams_max + df_dbs_max ) / common_max * 100
            self.aProgressBar.setValue( current_progress )

        if loaded_mdbs == df_mdbs_max:
            self.icon_mdbs.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_mdb_done.png' ).scaled( QSize( 128, 128 ) ) )
        else: 
            self.icon_mdbs.setPixmap( QPixmap( self.aCurrentPath + '/icons/admin/128x128_mdb_fail.png' ).scaled( QSize( 128, 128 ) ) )
        
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
        
        self.icon_users_counter.show()
        self.icon_teams_counter.show()
        self.icon_dbs_counter.show()
        self.icon_mdbs_counter.show()
        
        self.icon_teams_counter.setText( "Loaded " + str( loaded_teams ) + "/" + str( df_teams_max ) )        
        self.icon_users_counter.setText( "Loaded " + str( loaded_users ) + "/" + str( df_users_max ) )        
        self.icon_dbs_counter.setText( "Loaded " + str( loaded_dbs ) + "/" + str( df_dbs_max ) )        
        self.icon_mdbs_counter.setText( "Loaded " + str( loaded_mdbs ) + "/" + str( df_mdbs_max ) )
        
        self.aProgressBar.setValue( 100 )
        self.aProgressBar.hide()

        PipeCad.centralWidget().refreshList()

    
    # TODO: Add functional for collecting all used dbs numbers
    def collect_reserved_db_numbers(self):
        print("find all used dbs numbers")


# Singleton Instance.
aImportProjectDlg = ImportProjectDialog(PipeCad)

def ImportProject():
    aImportProjectDlg.show()
# ImportProject
        
class TeamDialog(QDialog):
    """docstring for TeamDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Admin", "Name"))
        self.textName = QLineEdit()
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Admin", "Description"))
        self.textDescription = QLineEdit()
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDescription)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Team Membership"))
        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.layoutTable = QVBoxLayout()
        self.labelProjectUsers = QLabel(QT_TRANSLATE_NOOP("Admin", "Project Users"))
        self.tableProjectUsers = QTableWidget()
        self.tableProjectUsers.setColumnCount(3)
        self.tableProjectUsers.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Security"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableProjectUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectUsers.setAlternatingRowColors(True)
        self.tableProjectUsers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectUsers.setGridStyle(Qt.SolidLine)
        self.tableProjectUsers.horizontalHeader().setStretchLastSection(True)
        self.tableProjectUsers.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectUsers.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelProjectUsers)
        self.layoutTable.addWidget(self.tableProjectUsers)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.layoutButton = QVBoxLayout()
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.buttonAddUser = QToolButton()
        self.buttonAddUser.setArrowType(Qt.RightArrow)
        self.buttonAddUser.clicked.connect(self.addUser)
        self.layoutButton.addWidget(self.buttonAddUser)

        self.buttonDelUser = QToolButton()
        self.buttonDelUser.setArrowType(Qt.LeftArrow)
        self.buttonDelUser.clicked.connect(self.delUser)
        self.layoutButton.addWidget(self.buttonDelUser)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.horizontalLayout.addLayout(self.layoutButton)
        
        self.layoutTable = QVBoxLayout()
        self.labelTeamUsers = QLabel(QT_TRANSLATE_NOOP("Admin", "Team Members"))
        self.tableTeamUsers = QTableWidget()
        self.tableTeamUsers.setColumnCount(3)
        self.tableTeamUsers.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Security"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableTeamUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableTeamUsers.setAlternatingRowColors(True)
        self.tableTeamUsers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableTeamUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableTeamUsers.setGridStyle(Qt.SolidLine)
        self.tableTeamUsers.horizontalHeader().setStretchLastSection(True)
        self.tableTeamUsers.verticalHeader().setMinimumSectionSize(16)
        self.tableTeamUsers.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelTeamUsers)
        self.layoutTable.addWidget(self.tableTeamUsers)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tmwlItem = PipeCad.GetItem("/*T")
        self.uswlItem = PipeCad.GetItem("/*U")
        self.teamItem = None

    # setupUi

    def init(self, theTeamItem = None):
        self.textName.setText("")
        self.textDescription.setText("")
        self.tableTeamUsers.setRowCount(0)
        self.tableProjectUsers.setRowCount(0)

        # Project Users.
        if self.uswlItem == None:
            return
        # if

        aTeamUserSet = set()
        
        if theTeamItem is not None:
            self.teamItem = theTeamItem
            self.textName.setText(theTeamItem.Name[1:])
            self.textDescription.setText(theTeamItem.Description)

            aTeamItems = PipeCad.CollectItem("LTEA", self.uswlItem)
            for aTeamItem in aTeamItems:
                if aTeamItem.Temf == theTeamItem:
                    aRow = self.tableTeamUsers.rowCount
                    self.tableTeamUsers.insertRow(aRow)

                    aUserItem = aTeamItem.Owner.Owner
                    aTeamUserSet.add(aUserItem)

                    aListItem = QTableWidgetItem(aUserItem.Name)
                    aListItem.setData(Qt.UserRole, aUserItem)

                    self.tableTeamUsers.setItem(aRow, 0, aListItem)
                    self.tableTeamUsers.setItem(aRow, 1, QTableWidgetItem(aUserItem.Security))
                    self.tableTeamUsers.setItem(aRow, 2, QTableWidgetItem(aUserItem.Description))
                # if
            # for
        # if

        aUserItems = self.uswlItem.Member
        for aUserItem in aUserItems:
            if aUserItem in aTeamUserSet:
                continue
            # if

            aRow = self.tableProjectUsers.rowCount
            self.tableProjectUsers.insertRow(aRow)

            aItem = QTableWidgetItem(aUserItem.Name)
            aItem.setData(Qt.UserRole, aUserItem)

            self.tableProjectUsers.setItem(aRow, 0, aItem)
            self.tableProjectUsers.setItem(aRow, 1, QTableWidgetItem(aUserItem.Security))
            self.tableProjectUsers.setItem(aRow, 2, QTableWidgetItem(aUserItem.Description))
        # for

        self.tableProjectUsers.resizeColumnsToContents()

        self.tableTeamUsers.resizeColumnsToContents()

    # init

    def create(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Create Team"))
        self.init()
        self.show()
    # createTeam

    def modify(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Modify Team"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modifyTeam

    def addUser(self):
        aRows = []
        for aItem in self.tableProjectUsers.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableProjectUsers.item(r, 0).clone()
            aSecurityItem = self.tableProjectUsers.item(r, 1).clone()
            aDescriptionItem = self.tableProjectUsers.item(r, 2).clone()

            aRow = self.tableTeamUsers.rowCount
            self.tableTeamUsers.insertRow(aRow)
            self.tableTeamUsers.setItem(aRow, 0, aNameItem)
            self.tableTeamUsers.setItem(aRow, 1, aSecurityItem)
            self.tableTeamUsers.setItem(aRow, 2, aDescriptionItem)

            self.tableProjectUsers.removeRow(r)

        self.tableTeamUsers.resizeColumnsToContents()
    # addUser

    def delUser(self):
        aRows = []
        for aItem in self.tableTeamUsers.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableTeamUsers.item(r, 0).clone()
            aSecurityItem = self.tableTeamUsers.item(r, 1).clone()
            aDescriptionItem = self.tableTeamUsers.item(r, 2).clone()

            aRow = self.tableProjectUsers.rowCount
            self.tableProjectUsers.insertRow(aRow)
            self.tableProjectUsers.setItem(aRow, 0, aNameItem)
            self.tableProjectUsers.setItem(aRow, 1, aSecurityItem)
            self.tableProjectUsers.setItem(aRow, 2, aDescriptionItem)

            self.tableTeamUsers.removeRow(r)

        self.tableTeamUsers.resizeColumnsToContents()
    # delUser

    def createTeam(self):
        aName = self.textName.text

        if len(aName) < 1:
            QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Admin", "Cannot create team - No team name specified!"))
            return
        # if

        PipeCad.StartTransaction("Create Team")

        try:
            PipeCad.CreateTeam(aName, self.textDescription.text)
        except NameError as e:
            # repr(e)
            QMessageBox.critical(self, "", str(e))
            raise
        # try

        aTeamItem = PipeCad.CurrentItem()

        # Add team to user team list.
        for r in range (self.tableTeamUsers.rowCount):
            aItem = self.tableTeamUsers.item(r, 0).data(Qt.UserRole)
            if aItem is not None:
                aTmliItems = aItem.Member
                if len(aTmliItems) > 0:
                    aTmliItem = aTmliItems[0]
                    aLteaItems = aTmliItem.Member
                    if len(aLteaItems) == 0:
                        PipeCad.SetCurrentItem(aTmliItem)
                    else:
                        PipeCad.SetCurrentItem(aLteaItems[-1])
                    # if

                    PipeCad.CreateItem("LTEA")
                    aLteaItem = PipeCad.CurrentItem()
                    aLteaItem.Temf = aTeamItem
                # if
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createTeam

    def modifyTeam(self):

        # Get Team Users.
        aUserSet = set()

        aUserTeams = PipeCad.CollectItem("LTEA", self.uswlItem)
        for aTeamItem in aUserTeams:
            if aTeamItem.Temf == self.teamItem:
                aUserItem = aTeamItem.Owner.Owner
                aUserSet.add(aUserItem)
            # if
        # for

        # Check Team Members.
        aMemberSet = set()

        for r in range (self.tableTeamUsers.rowCount):
            aUserItem = self.tableTeamUsers.item(r, 0).data(Qt.UserRole)
            if aUserItem is not None:
                aMemberSet.add(aUserItem)
            # if
        # for

        PipeCad.StartTransaction("Modify User")

        self.teamItem.Name = "*" + self.textName.text
        self.teamItem.Description = self.textDescription.text

        # Add new users to the team.
        aAddUsers = aMemberSet.difference(aUserSet)
        for aUserItem in aAddUsers:
            aTmliItems = aUserItem.Member
            if len(aTmliItems) > 0:
                aTmliItem = aTmliItems[0]
                aLteaItems = aTmliItem.Member
                if len(aLteaItems) == 0:
                    PipeCad.SetCurrentItem(aTmliItem)
                else:
                    PipeCad.SetCurrentItem(aLteaItems[-1])
                # if

                PipeCad.CreateItem("LTEA")
                aLteaItem = PipeCad.CurrentItem()
                aLteaItem.Temf = self.teamItem
            # if
        # for

        # Remove users from the team.
        aRemUsers = aUserSet.difference(aMemberSet)
        for aUserItem in aRemUsers:
            aLteaItems = PipeCad.CollectItem("LTEA", aUserItem)
            for aLteaItem in aLteaItems:
                if aLteaItem.Temf == self.teamItem:
                    PipeCad.SetCurrentItem(aLteaItem)
                    PipeCad.DeleteItem("LTEA")
                # if
            # for
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # modifyTeam

    def accept(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Admin", "Please input team name!"))
            return
        # if

        if self.tmwlItem is None:
            return

        if self.teamItem is None:
            self.createTeam()
        else:
            self.modifyTeam()
        # if

        self.parent().refreshList()

        QDialog.accept(self)
    # accept
# TeamDialog

class UserDialog(QDialog):
    """docstring for UserDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        self.gridLayout = QGridLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Admin", "Name"))
        self.textName = QLineEdit()

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Admin", "Description"))
        self.textDescription = QLineEdit()

        self.gridLayout.addWidget(self.labelName, 0, 0)
        self.gridLayout.addWidget(self.textName, 0, 1)
        self.gridLayout.addWidget(self.labelDescription, 0, 2)
        self.gridLayout.addWidget(self.textDescription, 0, 3)

        self.labelPassword = QLabel(QT_TRANSLATE_NOOP("Admin", "Password"))
        self.textPassword = QLineEdit()
        self.textPassword.setEchoMode(QLineEdit.Password)
        self.textPassword.setPlaceholderText(QT_TRANSLATE_NOOP("Admin", "Enter Password"))
        self.textPassword.textChanged.connect(self.confirmPassword)
        PipeCad.SetIndicator(self.textPassword)

        self.labelSecurity = QLabel(QT_TRANSLATE_NOOP("Admin", "Security"))
        self.comboSecurity = QComboBox()
        self.comboSecurity.addItem("General")
        self.comboSecurity.addItem("Free")

        self.labelConfirm = QLabel(QT_TRANSLATE_NOOP("Admin", "Confirm"))
        self.textConfirm = QLineEdit()
        self.textConfirm.setEchoMode(QLineEdit.Password)
        self.textConfirm.setPlaceholderText(QT_TRANSLATE_NOOP("Admin", "Confirm Password"))
        self.textConfirm.textChanged.connect(self.confirmPassword)
        PipeCad.SetIndicator(self.textConfirm)

        self.labelInfo = QLabel()

        self.gridLayout.addWidget(self.labelPassword, 1, 0)
        self.gridLayout.addWidget(self.textPassword, 1, 1)
        self.gridLayout.addWidget(self.labelConfirm, 1, 2)
        self.gridLayout.addWidget(self.textConfirm, 1, 3)

        self.gridLayout.addWidget(self.labelSecurity, 2, 0)
        self.gridLayout.addWidget(self.comboSecurity, 2, 1)
        self.gridLayout.addWidget(self.labelInfo, 2, 3)

        self.verticalLayout.addLayout(self.gridLayout)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Admin", "User Membership"))
        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.layoutTable = QVBoxLayout()
        self.labelProjectTeams = QLabel(QT_TRANSLATE_NOOP("Admin", "Project Teams"))
        self.tableProjectTeams = QTableWidget()
        self.tableProjectTeams.setColumnCount(2)
        self.tableProjectTeams.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableProjectTeams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectTeams.setAlternatingRowColors(True)
        self.tableProjectTeams.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectTeams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectTeams.setGridStyle(Qt.SolidLine)
        self.tableProjectTeams.horizontalHeader().setStretchLastSection(True)
        self.tableProjectTeams.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectTeams.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelProjectTeams)
        self.layoutTable.addWidget(self.tableProjectTeams)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.layoutButton = QVBoxLayout()
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.buttonAddTeam = QToolButton()
        self.buttonAddTeam.setArrowType(Qt.RightArrow)
        self.layoutButton.addWidget(self.buttonAddTeam)

        self.buttonDelTeam = QToolButton()
        self.buttonDelTeam.setArrowType(Qt.LeftArrow)
        self.layoutButton.addWidget(self.buttonDelTeam)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.buttonAddTeam.clicked.connect(self.addTeam)
        self.buttonDelTeam.clicked.connect(self.delTeam)

        self.horizontalLayout.addLayout(self.layoutButton)
        
        self.layoutTable = QVBoxLayout()
        self.labelUserTeams = QLabel(QT_TRANSLATE_NOOP("Admin", "Team Membership"))
        self.tableUserTeams = QTableWidget()
        self.tableUserTeams.setColumnCount(2)
        self.tableUserTeams.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableUserTeams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableUserTeams.setAlternatingRowColors(True)
        self.tableUserTeams.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableUserTeams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableUserTeams.setGridStyle(Qt.SolidLine)
        self.tableUserTeams.horizontalHeader().setStretchLastSection(True)
        self.tableUserTeams.verticalHeader().setMinimumSectionSize(16)
        self.tableUserTeams.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelUserTeams)
        self.layoutTable.addWidget(self.tableUserTeams)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.uswlItem = PipeCad.GetItem("/*U")
        self.tmwlItem = PipeCad.GetItem("/*T")
        self.userItem = None

    # setupUi

    def init(self, theUserItem = None):
        self.userItem = theUserItem
        self.tableUserTeams.setRowCount(0)

        if theUserItem is not None:
            if theUserItem.Type == "USER":
                self.textName.setText(theUserItem.Name)
                self.comboSecurity.setCurrentText(theUserItem.Security)
                self.textDescription.setText(theUserItem.Description)
                self.textPassword.setText(theUserItem.Password)
                self.textConfirm.setText(theUserItem.Password)
            # if
        else:
            self.textName.setText("")
            self.comboSecurity.setCurrentText("General")
            self.textDescription.setText("")
            self.textPassword.setText("")
            self.textConfirm.setText("")
        # if

        # Project Teams.
        if self.tmwlItem == None:
            return
        # if

        aTeamSet = set()

        if theUserItem is not None:
            aLteaItems = PipeCad.CollectItem("LTEA", theUserItem)
            self.tableUserTeams.setRowCount(len(aLteaItems))

            for r in range (self.tableUserTeams.rowCount):
                aTeamItem = aLteaItems[r].Temf
                if aTeamItem is None:
                    continue
                # if

                aTeamSet.add(aTeamItem)

                aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
                aItem.setData(Qt.UserRole, aTeamItem)

                self.tableUserTeams.setItem(r, 0, aItem)
                self.tableUserTeams.setItem(r, 1, QTableWidgetItem(aTeamItem.Description))
            # for

            self.tableUserTeams.resizeColumnsToContents()
        # if

        aTeamItems = self.tmwlItem.Member
        self.tableProjectTeams.setRowCount(0)

        for r in range(len(aTeamItems)):
            aTeamItem = aTeamItems[r]
            if not(aTeamItem in aTeamSet):
                aRow = self.tableProjectTeams.rowCount
                self.tableProjectTeams.insertRow(aRow)

                aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
                aItem.setData(Qt.UserRole, aTeamItem)

                self.tableProjectTeams.setItem(aRow, 0, aItem)
                self.tableProjectTeams.setItem(aRow, 1, QTableWidgetItem(aTeamItem.Description))
            # if
        # for

        self.tableProjectTeams.resizeColumnsToContents()
    # init

    def create(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Create User"))
        self.init()
        self.show()
    # createTeam

    def modify(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Modify User"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modifyTeam

    def confirmPassword(self):
        if len(self.textPassword.text) > 0 or len(self.textConfirm.text) > 0:
            if self.textPassword.text == self.textConfirm.text:
                self.labelInfo.setText(QT_TRANSLATE_NOOP("Admin", "<font color=Green>Matched</font>"))
            else:
                self.labelInfo.setText(QT_TRANSLATE_NOOP("Admin", "<font color=Red>Not match</font>"))
        else:
            self.labelInfo.setText("")
    # confirmPassword

    def addTeam(self):
        aRows = []
        for aItem in self.tableProjectTeams.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableProjectTeams.item(r, 0).clone()
            aDescriptionItem = self.tableProjectTeams.item(r, 1).clone()

            aRow = self.tableUserTeams.rowCount
            self.tableUserTeams.insertRow(aRow)
            self.tableUserTeams.setItem(aRow, 0, aNameItem)
            self.tableUserTeams.setItem(aRow, 1, aDescriptionItem)

            self.tableProjectTeams.removeRow(r)

        self.tableUserTeams.resizeColumnsToContents()
    # addTeam

    def delTeam(self):
        aRows = []
        for aItem in self.tableUserTeams.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableUserTeams.item(r, 0).clone()
            aDescriptionItem = self.tableUserTeams.item(r, 1).clone()

            aRow = self.tableProjectTeams.rowCount
            self.tableProjectTeams.insertRow(aRow)
            self.tableProjectTeams.setItem(aRow, 0, aNameItem)
            self.tableProjectTeams.setItem(aRow, 1, aDescriptionItem)

            self.tableUserTeams.removeRow(r)

        self.tableProjectTeams.resizeColumnsToContents()
    # delTeam

    def createUser(self):
        aName = self.textName.text
        aDescription = self.textDescription.text
        aPassword = self.textPassword.text
        aSecurity = self.comboSecurity.currentText
        aTeamList = list()

        for r in range (self.tableUserTeams.rowCount):
            aTeamItem = self.tableUserTeams.item(r, 0).data(Qt.UserRole)
            aTeamList.append(aTeamItem)
        # for

        PipeCad.CreateUser(aName, aDescription, aPassword, aSecurity, aTeamList)

        PipeCad.SaveWork()
    # createUser

    def modifyUser(self):
        # Get user team list.
        aTeamSet = set()
        aLteaItems = PipeCad.CollectItem("LTEA", self.userItem)
        for aLteaItem in aLteaItems:
            if aLteaItem.Temf is not None:
                aTeamSet.add(aLteaItem.Temf)
            # if
        # for

        # Get team member list.
        aMemberSet = set()

        for r in range (self.tableUserTeams.rowCount):
            aTeamItem = self.tableUserTeams.item(r, 0).data(Qt.UserRole)
            aMemberSet.add(aTeamItem)
        # for

        PipeCad.StartTransaction("Modify User")
        self.userItem.Name = self.textName.text
        self.userItem.Description = self.textDescription.text
        self.userItem.Security = self.comboSecurity.currentText
        if self.userItem.Password != self.textPassword.text:
            self.userItem.Password = self.textPassword.text
        # if

        # Set current item to add new team.
        aTmliItem = self.userItem.Member[0]
        if len(aTmliItem.Member) > 0:
            PipeCad.SetCurrentItem(aTmliItem.Member[-1])
        else:
            PipeCad.SetCurrentItem(aTmliItem)
        # if

        # Add new team to the user.
        aAddTeams = aMemberSet.difference(aTeamSet)
        for aTeamItem in aAddTeams:
            PipeCad.CreateItem("LTEA")
            aLteaItem = PipeCad.CurrentItem()
            aLteaItem.Temf = aTeamItem
        # for

        # Remove teams from the user.
        aRemTeams = aTeamSet.difference(aMemberSet)
        for aLteaItem in aLteaItems:
            if aLteaItem.Temf in aRemTeams:
                PipeCad.SetCurrentItem(aLteaItem)
                PipeCad.DeleteItem("LTEA")
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # modifyUser

    def accept(self):
        aName = self.textName.text
        aPassword = self.textPassword.text
        if len(aName) < 1 or len(aPassword) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Admin", "Please input user name and password!"))
            return
        # if

        if self.textPassword.text != self.textConfirm.text:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Admin", "The passwords do not match!"))
            return
        # if

        if self.uswlItem is None:
            return
        # if

        if self.userItem is None:
            self.createUser()
        else:
            self.modifyUser()
        # if

        self.parent().refreshList()

        QDialog.accept(self)

    # accept


class DatabaseDialog(QDialog):
    """docstring for DatabaseDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(420, 580)
        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()
        self.labelDatabase = QLabel(QT_TRANSLATE_NOOP("Admin", "Database"))
        self.horizontalLayout.addWidget(self.labelDatabase)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Project Teams"))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.tableProjectTeams = QTableWidget()
        self.tableProjectTeams.setColumnCount(2)
        self.tableProjectTeams.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableProjectTeams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectTeams.setAlternatingRowColors(True)
        self.tableProjectTeams.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectTeams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectTeams.setGridStyle(Qt.SolidLine)
        self.tableProjectTeams.horizontalHeader().setStretchLastSection(True)
        self.tableProjectTeams.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectTeams.verticalHeader().setDefaultSectionSize(18)
        self.tableProjectTeams.currentItemChanged.connect(self.teamChanged)
        self.horizontalLayout.addWidget(self.tableProjectTeams)
        self.verticalLayout.addWidget(self.groupBox)

        self.gridLayout = QGridLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Admin", "Name"))
        self.textName = QLineEdit()
        self.textName.textChanged.connect(self.teamChanged)
        self.gridLayout.addWidget(self.labelName, 0, 0)
        self.gridLayout.addWidget(self.textName, 0, 1)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Admin", "Description"))
        self.textDescription = QLineEdit()
        self.gridLayout.addWidget(self.labelDescription, 1, 0)
        self.gridLayout.addWidget(self.textDescription, 1, 1)

        self.labelType = QLabel(QT_TRANSLATE_NOOP("Admin", "Database Type"))
        self.comboType = QComboBox()
        self.comboType.addItems(["Design", "Catalogue"])
        self.comboType.currentTextChanged.connect(self.dbTypeChanged)
        self.gridLayout.addWidget(self.labelType, 2, 0)
        self.gridLayout.addWidget(self.comboType, 2, 1)

        self.labelCreate = QLabel(QT_TRANSLATE_NOOP("Admin", "Create SITE"))
        self.textCreate = QLineEdit()
        self.gridLayout.addWidget(self.labelCreate, 3, 0)
        self.gridLayout.addWidget(self.textCreate, 3, 1)

        # self.labelArea = QLabel("Area Number")
        # self.textArea = QLineEdit()
        # self.textArea.setPlaceholderText("Set by System")
        # self.buttonArea = QPushButton("System")
        # self.buttonArea.clicked.connect(self.setAreaNumber)
        # self.gridLayout.addWidget(self.labelArea, 4, 0)
        # self.gridLayout.addWidget(self.textArea, 4, 1)
        # self.gridLayout.addWidget(self.buttonArea, 4, 2)

        self.labelNumber = QLabel(QT_TRANSLATE_NOOP("Admin", "DB Number"))
        self.textNumber = QLineEdit()
        self.textNumber.setPlaceholderText(QT_TRANSLATE_NOOP("Admin", "Set by System"))
        self.buttonNumber = QPushButton(QT_TRANSLATE_NOOP("Admin", "System"))
        self.buttonNumber.clicked.connect(self.setDbNumber)
        self.gridLayout.addWidget(self.labelNumber, 5, 0)
        self.gridLayout.addWidget(self.textNumber, 5, 1)
        self.gridLayout.addWidget(self.buttonNumber, 5, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tmwlItem = PipeCad.GetItem("/*T")
        self.dbItem = None

    # setupUi

    def init(self, theDbItem = None):
        self.dbItem = theDbItem
        
        if theDbItem is not None:
            self.textName.setText(theDbItem.Name[theDbItem.Name.index("/")+1:])
            self.textDescription.setText(theDbItem.Description)
            #self.textArea.setText(str(theDbItem.Area))
            self.textNumber.setText(str(theDbItem.DbNumber))
            aIndex = self.comboType.findText(theDbItem.DbType, Qt.MatchStartsWith)
            self.comboType.setCurrentIndex(aIndex)

            self.textNumber.setEnabled(False)
            self.buttonNumber.setEnabled(False)
            self.comboType.setEnabled(False)
            self.textCreate.setEnabled(False)
        else:
            self.textName.setText("")
            self.textDescription.setText("")
            self.textNumber.setText("")

            self.textNumber.setEnabled(True)
            self.buttonNumber.setEnabled(True)
            self.comboType.setEnabled(True)
            self.textCreate.setEnabled(True)
        # if

        if self.tmwlItem is None:
            return
        # if

        aTeamItems = self.tmwlItem.Member
        self.tableProjectTeams.setRowCount(len(aTeamItems))

        for r in range (self.tableProjectTeams.rowCount):
            aTeamItem = aTeamItems[r]
            aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
            aItem.setData(Qt.UserRole, aTeamItem)

            self.tableProjectTeams.setItem(r, 0, aItem)
            self.tableProjectTeams.setItem(r, 1, QTableWidgetItem(aTeamItem.Description))

            if theDbItem is not None:
                if theDbItem.Name.startswith(aTeamItem.Name):
                    self.tableProjectTeams.setCurrentItem(aItem)
                # if
            # if
        # for

        self.tableProjectTeams.resizeColumnsToContents()

    # init

    def create(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Create Database"))
        self.init()
        self.show()
    # create

    def modify(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Modify Database"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modify

    def teamChanged(self):
        aRow = self.tableProjectTeams.currentRow()
        aItem = self.tableProjectTeams.item(aRow, 0)
        aName = self.textName.text
        if aItem is not None:
            self.labelDatabase.setText(QT_TRANSLATE_NOOP("Admin", "Database: <font color=Brown>%s/%s </font>") % (aItem.text()[6:], aName))
        # if
    # teamChanged

    def dbTypeChanged(self, theType):
        if theType == "Catalogue":
            self.labelCreate.setText(QT_TRANSLATE_NOOP("Admin", "Create CATA"))
        else:
            self.labelCreate.setText(QT_TRANSLATE_NOOP("Admin", "Create SITE"))
        # if
    # dbTypeChanged

    def setAreaNumber(self):
        QMessageBox.warning(self, "", "set area number")
    # setAreaNumber

    def setDbNumber(self):
        aNumber = self.tmwlItem.NextDbNumber
        self.textNumber.setText(str(aNumber))
    # setDatabaseNumber

    def createDb(self, theName):
        #aArea = 0
        aNumber = 0
        #if len(self.textArea.text) > 0:
        #    aArea = int(self.textArea.text)

        if len(self.textNumber.text) > 0:
            aNumber = int(self.textNumber.text)

            # Check the input database number range.
            if aNumber > 8000 or aNumber < 1:
                QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Admin", "Database Number range is [1~8000]!"))
                raise ValueError ("Database Number range is [1~8000]!")
            # if
        else:
            aNumber = self.tmwlItem.NextDbNumber()
        # if

        aDbType = self.comboType.currentText[0:4].upper()

        PipeCad.StartTransaction("Create Database")
        PipeCad.CreateDb(theName, aDbType, aNumber, self.textDescription.text)
        aDbItem = PipeCad.CurrentItem()
        aDbItem.CreateDbElement(self.textCreate.text)
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createDb

    def modifyDb(self):
        PipeCad.StartTransaction("Modify Database")
        self.dbItem.Name = self.textName.text
        self.dbItem.Description = self.textDescription.text
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()

        QDialog.accept(self)
    # modifyDb

    def accept(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Admin", "Please input database name!"))
            return
        # if

        aRow = self.tableProjectTeams.currentRow()
        aTeamItem = self.tableProjectTeams.item(aRow, 0).data(Qt.UserRole)
        if aTeamItem is None:
            return
        # if

        aDbliItem = aTeamItem.Member[0]
        if aDbliItem is None:
            return
        # if

        aDbItems = aDbliItem.Member
        if len(aDbItems) > 0:
            PipeCad.SetCurrentItem(aDbItems[-1])
        else:
            PipeCad.SetCurrentItem(aDbliItem)
        # if

        # Check the input database name.
        aDbName = aTeamItem.Name + "/" + aName
        if self.dbItem is not None:
            PipeCad.StartTransaction("Modify Database")
            self.dbItem.Name = aDbName
            self.dbItem.Description = self.textDescription.text
            PipeCad.CommitTransaction()
            PipeCad.SaveWork()

            self.parent().refreshList()

            QDialog.accept(self)

            return
        # if

        aDatabases = PipeCad.CollectItem("DB", self.tmwlItem)
        for aDatabase in aDatabases:
            if aDatabase.Name == aDbName:
                aMessage = "Database Name " + aDbName + " already exists!"
                QMessageBox.critical(self, "", aMessage)
                raise NameError (aMessage)
            # if
        # for

        self.createDb(aDbName)

        self.parent().refreshList()

        QDialog.accept(self)

    # accept


class MdbDialog(QDialog):
    """docstring for MdbDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(580, 600)
        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Admin", "Name"))
        self.textName = QLineEdit()
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Admin", "Description"))
        self.textDescription = QLineEdit()
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDescription)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupBoxProject = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Project Databases"))
        self.horizontalLayout = QHBoxLayout(self.groupBoxProject)

        self.tableProjectDatabases = QTableWidget()
        self.tableProjectDatabases.setColumnCount(4)
        self.tableProjectDatabases.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Type"), QT_TRANSLATE_NOOP("Admin", "DB Number"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableProjectDatabases.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectDatabases.setAlternatingRowColors(True)
        self.tableProjectDatabases.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectDatabases.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectDatabases.setGridStyle(Qt.SolidLine)
        self.tableProjectDatabases.horizontalHeader().setStretchLastSection(True)
        self.tableProjectDatabases.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectDatabases.verticalHeader().setDefaultSectionSize(18)

        self.horizontalLayout.addWidget(self.tableProjectDatabases)

        self.verticalLayout.addWidget(self.groupBoxProject)

        self.layoutButton = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layoutButton.addItem(self.horizontalSpacer)

        self.buttonAddDatabase = QToolButton()
        self.buttonAddDatabase.setArrowType(Qt.DownArrow)
        self.buttonAddDatabase.clicked.connect(self.addDatabase)
        self.layoutButton.addWidget(self.buttonAddDatabase)

        self.buttonDelDatabase = QToolButton()
        self.buttonDelDatabase.setArrowType(Qt.UpArrow)
        self.buttonDelDatabase.clicked.connect(self.delDatabase)
        self.layoutButton.addWidget(self.buttonDelDatabase)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layoutButton.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.layoutButton)
        
        self.groupBoxCurrent = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Current Databases"))
        self.horizontalLayout = QHBoxLayout(self.groupBoxCurrent)

        self.tableCurrentDatabases = QTableWidget()
        self.tableCurrentDatabases.setColumnCount(4)
        self.tableCurrentDatabases.setHorizontalHeaderLabels([QT_TRANSLATE_NOOP("Admin", "Name"), QT_TRANSLATE_NOOP("Admin", "Type"), QT_TRANSLATE_NOOP("Admin", "DB Number"), QT_TRANSLATE_NOOP("Admin", "Description")])
        self.tableCurrentDatabases.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableCurrentDatabases.setAlternatingRowColors(True)
        self.tableCurrentDatabases.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableCurrentDatabases.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableCurrentDatabases.setGridStyle(Qt.SolidLine)
        self.tableCurrentDatabases.horizontalHeader().setStretchLastSection(True)
        self.tableCurrentDatabases.verticalHeader().setMinimumSectionSize(16)
        self.tableCurrentDatabases.verticalHeader().setDefaultSectionSize(18)

        self.horizontalLayout.addWidget(self.tableCurrentDatabases)

        self.verticalLayout.addWidget(self.groupBoxCurrent)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tmwlItem = PipeCad.GetItem("/*T")
        self.mdbwItem = PipeCad.GetItem("/*M")
        self.mdbItem = None

    # setupUi

    def init(self, theMdbItem = None):
        aDbNumers = []
        self.mdbItem = theMdbItem
        self.tableCurrentDatabases.setRowCount(0)
        self.tableProjectDatabases.setRowCount(0)
        
        if theMdbItem is not None:
            self.textName.setText(theMdbItem.Name)
            self.textDescription.setText(theMdbItem.Description)

            # Current MDB databases.
            aDbItems = theMdbItem.Member
            self.tableCurrentDatabases.setRowCount(len(aDbItems))
            for r in range (self.tableCurrentDatabases.rowCount):
                aDbItem = aDbItems[r].Dbref
                aItem = QTableWidgetItem("<DB> " + aDbItem.Name[1:])
                aItem.setData(Qt.UserRole, aDbItem)

                self.tableCurrentDatabases.setItem(r, 0, aItem)
                self.tableCurrentDatabases.setItem(r, 1, QTableWidgetItem(aDbItem.DbType))
                self.tableCurrentDatabases.setItem(r, 2, QTableWidgetItem(str(aDbItem.DbNumber)))
                self.tableCurrentDatabases.setItem(r, 3, QTableWidgetItem(aDbItem.Description))

                aDbNumers.append(aDbItem.DbNumber)
            # for

            self.tableCurrentDatabases.resizeColumnsToContents()
        else:
            self.textName.setText("")
            self.textDescription.setText("")
        # if

        if self.tmwlItem is None:
            return
        # if

        aDbItems = []
        aDatabases = PipeCad.CollectItem("DB")
        for aDatabase in aDatabases:
            if aDbNumers.count(aDatabase.DbNumber) < 1:
                aDbItems.append(aDatabase)

        self.tableProjectDatabases.setRowCount(len(aDbItems))

        for r in range (self.tableProjectDatabases.rowCount):
            aDbItem = aDbItems[r]
            aItem = QTableWidgetItem("<DB> " + aDbItem.Name[1:])
            aItem.setData(Qt.UserRole, aDbItem)

            self.tableProjectDatabases.setItem(r, 0, aItem)
            self.tableProjectDatabases.setItem(r, 1, QTableWidgetItem(aDbItem.DbType))
            self.tableProjectDatabases.setItem(r, 2, QTableWidgetItem(str(aDbItem.DbNumber)))
            self.tableProjectDatabases.setItem(r, 3, QTableWidgetItem(aDbItem.Description))

        self.tableProjectDatabases.resizeColumnsToContents()
    # init

    def create(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Create Multiple Database"))
        self.init()
        self.show()
    # create

    def modify(self):
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Modify Multiple Database"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modify

    def addDatabase(self):
        aRows = []
        for aItem in self.tableProjectDatabases.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableProjectDatabases.item(r, 0).clone()
            aTypeItem = self.tableProjectDatabases.item(r, 1).clone()
            aNumbItem = self.tableProjectDatabases.item(r, 2).clone()
            aDescItem = self.tableProjectDatabases.item(r, 3).clone()

            aRow = self.tableCurrentDatabases.rowCount
            self.tableCurrentDatabases.insertRow(aRow)
            self.tableCurrentDatabases.setItem(aRow, 0, aNameItem)
            self.tableCurrentDatabases.setItem(aRow, 1, aTypeItem)
            self.tableCurrentDatabases.setItem(aRow, 2, aNumbItem)
            self.tableCurrentDatabases.setItem(aRow, 3, aDescItem)

            self.tableProjectDatabases.removeRow(r)

        self.tableCurrentDatabases.resizeColumnsToContents()
    # addDatabase

    def delDatabase(self):
        aRows = []
        for aItem in self.tableCurrentDatabases.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableCurrentDatabases.item(r, 0).clone()
            aTypeItem = self.tableCurrentDatabases.item(r, 1).clone()
            aNumbItem = self.tableCurrentDatabases.item(r, 2).clone()
            aDescItem = self.tableCurrentDatabases.item(r, 3).clone()

            aRow = self.tableProjectDatabases.rowCount
            self.tableProjectDatabases.insertRow(aRow)
            self.tableProjectDatabases.setItem(aRow, 0, aNameItem)
            self.tableProjectDatabases.setItem(aRow, 1, aTypeItem)
            self.tableProjectDatabases.setItem(aRow, 2, aNumbItem)
            self.tableProjectDatabases.setItem(aRow, 3, aDescItem)

            self.tableCurrentDatabases.removeRow(r)

        self.tableProjectDatabases.resizeColumnsToContents()
    # delDatabase

    def createMdb(self):
        aName = self.textName.text        

        PipeCad.StartTransaction("Create MDB")
        PipeCad.CreateMdb(aName, self.textDescription.text)
        
        for r in range (self.tableCurrentDatabases.rowCount):
            aDbItem = self.tableCurrentDatabases.item(r, 0).data(Qt.UserRole)

            PipeCad.CreateItem("DBL")
            aDblItem = PipeCad.CurrentItem()
            if aDbItem is not None:
                aDblItem.Dbref = aDbItem
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createMdb

    def modifyMdb(self):
        # Get databse set.
        aDatabaseSet = set()
        for aDblItem in self.mdbItem.Member:
            aDatabaseSet.add(aDblItem.Dbref)
        # for

        # Get current databse set.
        aCurrentSet = set()
        for r in range (self.tableCurrentDatabases.rowCount):
            aDbItem = self.tableCurrentDatabases.item(r, 0).data(Qt.UserRole)
            aCurrentSet.add(aDbItem)
        # for

        PipeCad.StartTransaction("Modify MDB")
        self.mdbItem.Name = self.textName.text
        self.mdbItem.Description = self.textDescription.text

        if len(self.mdbItem.Member) > 0:
            PipeCad.SetCurrentItem(self.mdbItem.Member[-1])
        else:
            PipeCad.SetCurrentItem(self.mdbItem)
        # if

        # Add new database to the MDB.
        aAddDbs = aCurrentSet.difference(aDatabaseSet)
        for aDbItem in aAddDbs:
            PipeCad.CreateItem("DBL")
            aDblItem = PipeCad.CurrentItem()
            if aDbItem is not None:
                aDblItem.Dbref = aDbItem
            # if
        # for

        # Remove database from the MDB.
        aRemDbs = aDatabaseSet.difference(aCurrentSet)
        for aDblItem in self.mdbItem.Member:
            if aDblItem.Dbref in aRemDbs:
                PipeCad.SetCurrentItem(aDblItem)
                PipeCad.DeleteItem("DBL")
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # modifyMdb

    def accept(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", QT_TRANSLATE_NOOP("Admin", "Please input MDB name!"))
            return
        # if

        if self.mdbwItem is None:
            return

        if self.mdbItem is None:
            self.createMdb()
        else:
            self.modifyMdb()
        # if

        self.parent().refreshList()

        QDialog.accept(self)

    # accept

def Show():
    aMain = AdminMain()
    aMain.elementChanged("Teams")
    PipeCad.setCentralWidget(aMain)
# Show

class ProjectDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.statItem = PipeCad.GetItem("/*S")
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setMinimumWidth(380)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Project Information"))

        aStatItem = self.statItem

        self.verticalLayout = QVBoxLayout(self)
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Project"))
        self.formLayout = QFormLayout(self.groupBox)

        self.labelProject = QLabel(QT_TRANSLATE_NOOP("Admin", "Project"))
        self.textProject = QLineEdit(aStatItem.ProjectNumber)
        self.textProject.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelProject)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textProject)

        self.labelCode = QLabel(QT_TRANSLATE_NOOP("Admin", "Code"))
        self.textCode = QLineEdit(PipeCad.CurrentProject.Code)
        self.textCode.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelCode)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textCode)

        self.labelNumber = QLabel(QT_TRANSLATE_NOOP("Admin", "Number"))
        self.textNumber = QLineEdit(aStatItem.ProjectNumber)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelNumber)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textNumber)

        self.labelName = QLabel(QT_TRANSLATE_NOOP("Admin", "Name"))
        self.textName = QLineEdit(aStatItem.ProjectName)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel(QT_TRANSLATE_NOOP("Admin", "Description"))
        self.textDescription = QLineEdit(aStatItem.ProjectDescription)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textDescription)

        self.labelMessage = QLabel(QT_TRANSLATE_NOOP("Admin", "Message"))
        self.textMessage = QLineEdit(aStatItem.ProjectMessage)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelMessage)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textMessage)

        self.verticalLayout.addWidget(self.groupBox)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    # setupUi

    def accept(self):
        if self.statItem is None:
            return
        # if

        PipeCad.StartTransaction("Modify Project Info")
        self.statItem.ProjectNumber = self.textNumber.text
        self.statItem.ProjectName = self.textName.text
        self.statItem.ProjectDescription = self.textDescription.text
        self.statItem.ProjectMessage = self.textMessage.text
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()

        QDialog.accept(self)
    # accept

# ProjectDialog

def ShowProject():
    aProjectDlg = ProjectDialog(PipeCad)
    aProjectDlg.exec()
# ShowProject

class UserProcessDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Expunge User Process"))

        self.verticalLayout = QVBoxLayout(self)
        self.groupBox = QGroupBox(QT_TRANSLATE_NOOP("Admin", "Project Users"))

        self.verticalLayoutBox = QHBoxLayout(self.groupBox)
        self.tableUser = QTableWidget()
        self.tableUser.setColumnCount(5)
        self.tableUser.setHorizontalHeaderLabels(["Date", "PC Name", "Host Name", "PipeCAD User", "Module"])
        self.tableUser.horizontalHeader().setDefaultSectionSize(80)
        self.tableUser.verticalHeader().setDefaultSectionSize(18)
        self.tableUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableUser.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableUser.horizontalHeader().setStretchLastSection(True)
        self.tableUser.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.verticalLayoutBox.addWidget(self.tableUser)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

    # setupUi

    def setSession(self):
        PipeCad.CurrentProject.updateSession()

        aSessionList = PipeCad.CurrentProject.Sessions

        self.tableUser.setRowCount(len(aSessionList))

        for i in range(self.tableUser.rowCount):
            aSession = aSessionList[i]

            aCurrent = aSession.Entered
            if aSession == PipeCad.CurrentSession:
                aCurrent = "*" + aSession.Entered
            # if

            aUserName = ""
            if aSession.User is not None:
                aUserName = aSession.User.Name
            # if

            aSessionItem = QTableWidgetItem(aCurrent)
            aSessionItem.setData(Qt.UserRole, aSession)

            self.tableUser.setItem(i, 0, aSessionItem)
            self.tableUser.setItem(i, 1, QTableWidgetItem(aSession.Login))
            self.tableUser.setItem(i, 2, QTableWidgetItem(aSession.Host))
            self.tableUser.setItem(i, 3, QTableWidgetItem(aUserName))
            self.tableUser.setItem(i, 4, QTableWidgetItem(aSession.Module))
        # for

    # setSession

    def accept(self):
        aRow = self.tableUser.currentRow()
        aSessionItem = self.tableUser.item(aRow, 0)
        if aSessionItem is None:
            return
        # if

        aSession = aSessionItem.data(Qt.UserRole)
        if aSession is None:
            return
        # if

        PipeCad.CurrentProject.expungeSession(aSession)

        self.setSession()
    # accept

# UserProcessDialog

# Singleton Instance.
aUserProcessDlg = UserProcessDialog(PipeCad)

def ExpungeUser():
    aUserProcessDlg.setSession()
    aUserProcessDlg.show()
# ExpungeUser

def ExpungeData():
    QMessageBox.warning(PipeCad, "", "Not implement yet!")
# ExpungeData
