from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

import numpy as np

class RevManagerDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.ColumnsHeaders = []
        self.setupUi()
    # __init__

    def setupUi(self):
        
        self.resize(400, 40)
        self.setWindowTitle(self.tr("PipeCAD - Revision Manager"))
              
        self.hBoxLayPipe = QHBoxLayout()
       
        self.btnCE = QPushButton(QT_TRANSLATE_NOOP("Admin", "CE"))
        self.btnCE.setMaximumSize( 40 , 40 )
        
        self.lblCE = QLabel("Select Pipe and press CE")
        
        self.hBoxLayPipe.addWidget(self.btnCE)
        self.hBoxLayPipe.addWidget(self.lblCE)
         
        self.btnApply = QPushButton(QT_TRANSLATE_NOOP("Admin", "Apply"))
        self.btnApply.setMaximumSize( 60 , 40 )
        
        self.btnCancel = QPushButton(QT_TRANSLATE_NOOP("Admin", "Cancel"))
        self.btnCancel.setMaximumSize( 60 , 40 )
            
        self.hBoxLayButtons = QHBoxLayout()
        self.hBoxLayButtons.addWidget(self.btnApply)
        self.hBoxLayButtons.addWidget(self.btnCancel)
        
        self.tableRevisions = QTableWidget()
        self.tableRevisions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableRevisions.setAlternatingRowColors(True)
        self.tableRevisions.setGridStyle(Qt.SolidLine)
        self.tableRevisions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableRevisions.horizontalHeader().setStretchLastSection(False)
        self.tableRevisions.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableRevisions.verticalHeader().setMinimumSectionSize(16)
        self.tableRevisions.verticalHeader().setDefaultSectionSize(18)
        self.tableRevisions.setHorizontalHeaderLabels(["Name"])         
        self.tableRevisions.setColumnCount(1)
           
        self.btnCE.clicked.connect(self.callCE)
        #self.btnApply.clicked.connect(self.callApply)
        
        self.vBoxLayMain = QVBoxLayout(self)
        self.vBoxLayMain.addLayout( self.hBoxLayPipe )
        self.vBoxLayMain.addWidget( self.tableRevisions )
        self.vBoxLayMain.addLayout( self.hBoxLayButtons )
        

    #def callAddColumn(self):      
    #    #df = pd.DataFrame((some_Data),('z','T'))
    #    #self.data.setRowCount(len(df))
    #    for k in self.ColumnsHeaders:
    #        #if self.lstAttributes.currentText not k:
    #        print(" ")
    #    self.ColumnsHeaders.append(self.lstAttributes.currentText)
    #    self.tableRevisions.setColumnCount(len(self.ColumnsHeaders))
    #    self.tableRevisions.setHorizontalHeaderLabels(self.ColumnsHeaders)
    
    def callCE(self):
        self.lblCE.text = "/" + PipeCad.CurrentItem().Name
        revisions = PipeCad.CollectItem("REVI", PipeCad.CurrentItem())
        self.tableRevisions.clear()
        self.tableRevisions.setRowCount(0)
        for i in range( len(revisions) ):
            print(revisions[i])
            aRow = self.tableRevisions.rowCount
            self.tableRevisions.insertRow(aRow)
            #for j in range( len(self.ColumnsHeaders) ):           
            self.tableRevisions.setItem(aRow, 1, QTableWidgetItem() )
            
                        
    #ef callRemoveColumn(self):      
    #   
    #   
    #   for k in self.ColumnsHeaders:
    #       if self.lstAttributes.currentText == k:
    #           self.ColumnsHeaders.remove(self.lstAttributes.currentText)
    #          
    #   self.tablePreview.setColumnCount(len(self.ColumnsHeaders))
    #   self.tablePreview.setHorizontalHeaderLabels(self.ColumnsHeaders)  


        
    
    def callApply(self):
        self.tableRevisions.clear()
        self.tableRevisions.setRowCount(0)
        self.tableRevisions.setColumnCount(len(self.ColumnsHeaders))
        self.tableRevisions.setHorizontalHeaderLabels(self.ColumnsHeaders)
        print(self.ColumnsHeaders)
        aCollection = PipeCad.CollectItem(self.lstType.currentText, PipeCad.GetItem(self.txtHierarchy.text) )      
        for i in range( len(aCollection) ):
            aRow = self.tableRevisions.rowCount
            self.tableRevisions.insertRow(aRow)
            for j in range( len(self.ColumnsHeaders) ):           
                self.tableRevisions.setItem(aRow, j, QTableWidgetItem( getattr(aCollection[i] , self.ColumnsHeaders[j] ) ) )

# Singleton Instance.
aRevManagerDialog = RevManagerDialog(PipeCad)

def showRevManager():
    aRevManagerDialog.show()
# Show
