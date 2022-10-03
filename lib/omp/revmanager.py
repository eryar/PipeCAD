from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

# import numpy as np

class RevManagerDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.dictRevisions = {}
        self.setupUi()
    # __init__

    def setupUi(self):
        
        self.setWindowTitle(self.tr("PipeCAD - Revision Manager"))
              
        self.hBoxLayPipe = QHBoxLayout()
       
        self.btnCE = QPushButton(QT_TRANSLATE_NOOP("Admin", "CE"))
        self.btnCE.setMaximumSize( 40 , 40 )
        
        self.lblCE = QLabel("Select Pipe and press CE")
        
        self.hBoxLayPipe.addWidget(self.btnCE)
        self.hBoxLayPipe.addWidget(self.lblCE)
         
        self.groupRevisions = QGroupBox("Revisions")        
        self.hBoxLayRevisions = QHBoxLayout()
        self.groupRevisions.setLayout(self.hBoxLayRevisions)
        
        self.vBoxLayRevLeft = QVBoxLayout()
        self.vBoxLayRevRight = QVBoxLayout()
        
        self.hBoxLayRevisions.addLayout(self.vBoxLayRevLeft)
        self.hBoxLayRevisions.addLayout(self.vBoxLayRevRight)
        
        self.lstRevisions = QListWidget()
        self.lstRevisions.setMaximumSize( 70, 90 )
        
        self.hBoxLayRevLeftButtons = QHBoxLayout()
        
        self.btnAddRev = QPushButton(QT_TRANSLATE_NOOP("Admin", "+"))
        self.btnAddRev.setMaximumSize( 32 , 32 )
        
        self.btnDelRev = QPushButton(QT_TRANSLATE_NOOP("Admin", "-"))
        self.btnDelRev.setMaximumSize( 32 , 32 )
        
        self.vBoxLayRevLeft.addWidget(self.lstRevisions)       
        self.vBoxLayRevLeft.addLayout(self.hBoxLayRevLeftButtons)       
        self.hBoxLayRevLeftButtons.addWidget(self.btnAddRev)       
        self.hBoxLayRevLeftButtons.addWidget(self.btnDelRev)       
        
        self.gridRevDetails = QGridLayout()
        
        self.lblDesc = QLabel("Description")
        self.txtDesc = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))    
        
        self.lblAuthor = QLabel("Author")
        self.lblChecker = QLabel("Checker")
        self.lblApprouver = QLabel("Approuver")  
        
        self.txtAuthorName = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))
        self.txtCheckerName = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))
        self.txtApprouverName = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))
        
        self.txtAuthorDate = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))
        self.txtCheckerDate = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))
        self.txtAprouverDate = QLineEdit(QT_TRANSLATE_NOOP("Admin", ""))
        
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
        self.gridRevDetails.addWidget( self.txtAprouverDate, 3, 3 )
        
        self.vBoxLayRevRight.addLayout(self.gridRevDetails)

        self.btnApply = QPushButton(QT_TRANSLATE_NOOP("Admin", "Apply"))
        
        self.btnAddRev.clicked.connect( self.callCreateNewRevision )
        self.btnDelRev.clicked.connect( self.callDeleteRevision )
        self.btnCE.clicked.connect( self.callCE )
        self.lstRevisions.currentRowChanged.connect(self.callSelectRevision)
        self.btnApply.clicked.connect( self.callApply )
        
        self.vBoxLayMain = QVBoxLayout(self)
        self.vBoxLayMain.addLayout( self.hBoxLayPipe )
        self.vBoxLayMain.addWidget( self.groupRevisions )
        self.vBoxLayMain.addWidget( self.btnApply )
    
    def callCreateNewRevision(self):
        
        new_revision = 0
        if self.lstRevisions.count != 0:
            next_revision = int( self.lstRevisions.takeItem( self.lstRevisions.count - 1 ).text() ) + 1
            self.lstRevisions.addItem( QListWidgetItem( next_revision ) )
        new_item = QListWidgetItem()
        new_item.setText(new_revision)
        #    for revision in self.lstRevisions:
        #        print( revision )
        #self.lstRevisions.addItem("0")
        #self.lstRevisions.sortItems()
        
    def callDeleteRevision(self):
        pass

    def callSelectRevision(self, i):
        print ( self.lstRevisions.currentItem() )
		
        #for count in range(self.lstRevisions.count()):
        #    print ( self.lstRevisions.itemText(count) )
        #    print ( "Current index",i,"selection changed ",self.lstRevisions.currentText() )

           
    def callCE(self):
        self.lstRevisions.clear()
        if  PipeCad.CurrentItem().Type == "PIPE":
            print("PIPE")
        elif PipeCad.CurrentItem().Type == "BRAN":
            print("BRAN")
        elif PipeCad.CurrentItem().Type == "REVI":
            print("REVI")
        else:
            print("sdsd")
        
        self.lblCE.text = "/" + PipeCad.CurrentItem().Name
        revisions = PipeCad.CollectItem("REVI", PipeCad.CurrentItem())
        
        self.txtDesc.text = ""
        self.txtAuthorName.text = ""
        self.txtCheckerName.text = ""
        self.txtApprouverName.text = ""
        self.txtAuthorDate.text = ""
        self.txtCheckerDate.text = ""
        self.txtAprouverDate.text = ""
        
        for i in range( len( revisions ) ):
            self.lstRevisions.addItem( revisions[i].Number )
        
        #self.txtDesc.text = ""
        #self.txtAuthorName.text = ""
        #self.txtCheckerName.text = ""
        #self.txtApprouverName.text = ""
        #self.txtAuthorDate.text = ""
        #self.txtCheckerDate.text = ""
        #self.txtAprouverDate.text = ""
        
        
        #self.tableRevisions.clear()
        #self.tableRevisions.setRowCount(0)
        #
        #    aRow = self.tableRevisions.rowCount
        #    self.tableRevisions.insertRow( aRow )
        #    self.tableRevisions.setItem( aRow, 0, QTableWidgetItem(  ) )
        #    self.tableRevisions.setItem( aRow, 1, QTableWidgetItem( revisions[i].Description ) )
        #    self.tableRevisions.setItem( aRow, 2, QTableWidgetItem( revisions[i].Author ) )
        #    self.tableRevisions.setItem( aRow, 3, QTableWidgetItem( revisions[i].Datetime.date().toString('dd.MM.yyyy') ) )
        #    self.tableRevisions.setItem( aRow, 4, QTableWidgetItem( revisions[i].Checker ) )
        #    self.tableRevisions.setItem( aRow, 5, QTableWidgetItem( revisions[i].Chkdate.date().toString('dd.MM.yyyy') ) )
        #    self.tableRevisions.setItem( aRow, 6, QTableWidgetItem( revisions[i].Approver ) )
        #    self.tableRevisions.setItem( aRow, 7, QTableWidgetItem( revisions[i].Appdate.date().toString('dd.MM.yyyy') ) )
        #
        #self.callTableRepresentation()                     
    
    def callApply(self):      
        self.callTableRepresentation()  
        
       
# Singleton Instance.
aRevManagerDialog = RevManagerDialog(PipeCad)

def showRevManager():
    aRevManagerDialog.show()
# Show
