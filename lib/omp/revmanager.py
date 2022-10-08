from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *
from datetime import * 

import os

class RevManagerDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.dictRevisions = {}
        self.setupUi()
        
    # __init__

    def setupUi(self):
        
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Revision Manager") )
              
        self.hBoxLayPipe = QHBoxLayout()
       
        self.btnCE = QPushButton(QT_TRANSLATE_NOOP("Admin", "CE") )
        self.btnCE.setMaximumSize( 40 , 40 )
        
        self.lblCE = QLabel("Select Pipe and press CE")
        
        self.hBoxLayPipe.addWidget(self.btnCE)
        self.hBoxLayPipe.addWidget(self.lblCE)
         
        self.groupRevisions = QGroupBox("Revisions")        
        self.hBoxLayRevisions = QHBoxLayout()
        self.groupRevisions.setLayout(self.hBoxLayRevisions)
        
        self.vBoxLayRevLeft = QVBoxLayout()
        self.vBoxLayRevRight = QVBoxLayout()
        
        self.hBoxLayRevisions.addLayout( self.vBoxLayRevLeft)
        self.hBoxLayRevisions.addLayout( self.vBoxLayRevRight)
        
        self.lstRevisions = QListWidget()
        self.lstRevisions.setMaximumSize( 40, 90 )
                
        self.btnAddRev = QPushButton(QT_TRANSLATE_NOOP("Admin", "+") )
        self.btnAddRev.setMaximumSize( 40 , 32 )
        
        self.vBoxLayRevLeft.addWidget( self.lstRevisions )       
        self.vBoxLayRevLeft.addWidget( self.btnAddRev )       
        
        self.gridRevDetails = QGridLayout()
        
        self.lblDesc = QLabel("Description")
        self.txtDesc = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )    
        
        self.lblAuthor = QLabel("Author")
        self.lblChecker = QLabel("Checker")
        self.lblApprouver = QLabel("Approuver")  
        
        self.txtAuthorName = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )
        self.txtCheckerName = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )
        self.txtApprouverName = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )
        
        self.txtAuthorDate = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )
        self.txtCheckerDate = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )
        self.txtApprouverDate = QLineEdit( QT_TRANSLATE_NOOP("Admin", "") )
        
        self.lblName = QLabel("Name")
        self.lblDate = QLabel("Date")
        
        self.gridRevDetails.addWidget( self.lblDesc, 0, 0 )
        self.gridRevDetails.addWidget( self.txtDesc, 0, 1, 1, 3 )    
        
        self.gridRevDetails.addWidget( self.lblDesc, 0, 0 )
        self.gridRevDetails.addWidget( self.txtDesc, 0, 1, 1, 3 )
        
        self.gridRevDetails.addWidget( self.lblAuthor, 1, 1 )
        self.gridRevDetails.addWidget( self.lblChecker, 1, 2 )
        self.gridRevDetails.addWidget( self.lblApprouver, 1, 3 )
        
        self.gridRevDetails.addWidget( self.lblName, 2, 0 )
        self.gridRevDetails.addWidget( self.txtAuthorName, 2, 1 )
        self.gridRevDetails.addWidget( self.txtCheckerName, 2, 2 )
        self.gridRevDetails.addWidget( self.txtApprouverName, 2, 3 )
        
        self.gridRevDetails.addWidget( self.lblDate, 3, 0 )
        self.gridRevDetails.addWidget( self.txtAuthorDate, 3, 1 )
        self.gridRevDetails.addWidget( self.txtCheckerDate, 3, 2 )
        self.gridRevDetails.addWidget( self.txtApprouverDate, 3, 3 )
        
        self.vBoxLayRevRight.addLayout(  self.gridRevDetails )

        self.btnApply = QPushButton( QT_TRANSLATE_NOOP("Admin", "Apply") )
            
        self.btnAddRev.clicked.connect( self.callCreateNewRevision )
        self.btnCE.clicked.connect( self.callCE )
        self.lstRevisions.currentItemChanged.connect( self.callSelectRevision )
        self.btnApply.clicked.connect( self.callApply )
        
        self.txtDesc.editingFinished.connect( self.callSaveData )
        self.txtAuthorName.editingFinished.connect( self.callSaveData )
        self.txtAuthorDate.editingFinished.connect( self.callSaveData )
        self.txtCheckerName.editingFinished.connect( self.callSaveData )
        self.txtCheckerDate.editingFinished.connect( self.callSaveData )
        self.txtApprouverName.editingFinished.connect( self.callSaveData )
        self.txtApprouverDate.editingFinished.connect( self.callSaveData )
        
        self.vBoxLayMain = QVBoxLayout(self)
        self.vBoxLayMain.addLayout(  self.hBoxLayPipe )
        self.vBoxLayMain.addWidget( self.groupRevisions )
        self.vBoxLayMain.addWidget( self.btnApply )
               
    def callSaveData(self):
        self.dictRevisions[ self.lstRevisions.currentItem().text() ] = self.lblCE.text[1:] + "-R" + self.lstRevisions.currentItem().text() + ";" + \
                                                                       self.txtDesc.text + ";" + \
                                                                       self.txtAuthorName.text + ";" + \
                                                                       self.txtAuthorDate.text + ";" + \
                                                                       self.txtCheckerName.text + ";" + \
                                                                       self.txtCheckerDate.text + ";" + \
                                                                       self.txtApprouverName.text + ";" + \
                                                                       self.txtApprouverDate.text
                                                                               
    def callCreateNewRevision(self):
        self.lstRevisions.clear()
        
        self.dictRevisions[ str( len( self.dictRevisions.keys() ) + 1 ) ] = self.lblCE.text[1:] + "-R" + str( len( self.dictRevisions.keys() ) + 1 ) + ";Fill Description;" + os.getlogin() + ";" + date.today().strftime("%d.%m.%Y") + ";;;;"
        
        for key in sorted(self.dictRevisions.keys()):
            cur_item = QListWidgetItem( key )
            self.lstRevisions.addItem( cur_item )
        
        self.lstRevisions.setCurrentItem( cur_item )
       
    def callSelectRevision(self, item):
        if item != None: 
            self.txtDesc.text = self.dictRevisions[ str( item.text() ) ].split(";")[1]
            self.txtAuthorName.text = self.dictRevisions[ str( item.text() ) ].split(";")[2]
            self.txtAuthorDate.text = self.dictRevisions[ str( item.text() ) ].split(";")[3]
            self.txtCheckerName.text = self.dictRevisions[ str( item.text() ) ].split(";")[4]
            self.txtCheckerDate.text = self.dictRevisions[ str( item.text() ) ].split(";")[5]
            self.txtApprouverName.text = self.dictRevisions[ str( item.text() ) ].split(";")[6]
            self.txtApprouverDate.text = self.dictRevisions[ str( item.text() ) ].split(";")[7]
		
    def callCE(self):
        self.lstRevisions.clear()
        self.txtDesc.text = ""
        self.txtAuthorName.text = ""
        self.txtCheckerName.text = ""
        self.txtApprouverName.text = ""
        self.txtAuthorDate.text = ""
        self.txtCheckerDate.text = ""
        self.txtApprouverDate.text = ""
        
        if  PipeCad.CurrentItem().Type != "PIPE":
            QMessageBox.critical(self, "", QT_TRANSLATE_NOOP("Admin", "Please select Pipe!"))
            return 
                    
        self.lblCE.text = "/" + PipeCad.CurrentItem().Name
        revisions = PipeCad.CollectItem("REVI", PipeCad.CurrentItem() )
                
        if len( revisions ) != 0:
            for i in range( len( revisions ) ):
                self.dictRevisions[ revisions[i].Number ] = revisions[i].Name + ";" + \
                                                            revisions[i].Description + ";" + \
                                                            revisions[i].Author + ";" + \
                                                            revisions[i].Datetime.date().toString('dd.MM.yyyy') + ";" + \
                                                            revisions[i].Checker + ";" + \
                                                            revisions[i].Chkdate.date().toString('dd.MM.yyyy') + ";" + \
                                                            revisions[i].Approver + ";" + \
                                                            revisions[i].Appdate.date().toString('dd.MM.yyyy')
                                                                    
                rev_element = QListWidgetItem( revisions[i].Number )
                self.lstRevisions.addItem( rev_element )       
                    
        self.lstRevisions.sortItems()
        
        
    def callApply(self):      
        for key in self.dictRevisions.keys():
            rev_element =  self.dictRevisions[ key ].split(";")[0]      
            try: 
                PipeCad.SetCurrentItem( self.lblCE.text )
                current_pipe = PipeCad.CurrentItem()
                PipeCad.StartTransaction("Create Revision")
                PipeCad.CreateItem( "REVI", rev_element )
                PipeCad.CommitTransaction()
               
            except NameError as e:
                pass
            
            PipeCad.SetCurrentItem( "/" + rev_element )
            PipeCad.CurrentItem().Number = key
            PipeCad.CurrentItem().Description = self.dictRevisions[ key ].split(";")[1]
            PipeCad.CurrentItem().Author = self.dictRevisions[ key ].split(";")[2]
            if self.dictRevisions[ key ].split(";")[3] != "":
                PipeCad.CurrentItem().Datetime = QDateTime( QDate( int( self.dictRevisions[ key ].split(";")[3].split(".")[2]) , int( self.dictRevisions[ key ].split(";")[3].split(".")[1] ), int( self.dictRevisions[ key ].split(";")[3].split(".")[0])), QTime( 0, 0 )  )
                
            PipeCad.CurrentItem().Checker = self.dictRevisions[ key ].split(";")[4]
            
            if self.dictRevisions[ key ].split(";")[5] != "":
                PipeCad.CurrentItem().Chkdate = QDateTime( QDate( int( self.dictRevisions[ key ].split(";")[5].split(".")[2]) , int( self.dictRevisions[ key ].split(";")[5].split(".")[1] ), int( self.dictRevisions[ key ].split(";")[5].split(".")[0])), QTime( 0, 0 )  )
                
            PipeCad.CurrentItem().Approver = self.dictRevisions[ key ].split(";")[6]
            
            if self.dictRevisions[ key ].split(";")[7] != "":
                PipeCad.CurrentItem().Appdate = QDateTime( QDate( int( self.dictRevisions[ key ].split(";")[7].split(".")[2]) , int( self.dictRevisions[ key ].split(";")[7].split(".")[1] ), int( self.dictRevisions[ key ].split(";")[7].split(".")[0])), QTime( 0, 0 )  )
            
        PipeCad.SaveWork() 
            

       
# Singleton Instance.
aRevManagerDialog = RevManagerDialog(PipeCad)

def showRevManager():
    aRevManagerDialog.show()
# Show

















