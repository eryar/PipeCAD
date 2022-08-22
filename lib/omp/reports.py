from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

import numpy as np

class dlgReports(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.ColumnsHeaders = []
        self.setupUi()
    # __init__

    def setupUi(self):
        
        self.resize(500, 400)
        self.setWindowTitle(self.tr("PipeCAD - Report"))
        
        self.vBoxLayout = QVBoxLayout(self)        
        self.grid = QGridLayout()
        
        self.lblType = QLabel("Element Type")
        self.lstType = QComboBox()
        self.lstType.addItem("")
        self.lstType.addItem("PIPE")
        self.lstType.addItem("BRANCH")
        self.lstType.addItem("SITE")
        self.lstType.addItem("ZONE")
        
        self.hBoxLayoutCondition = QHBoxLayout(self)   
        self.lblCondition = QLabel("Condition")
        self.lstConditionAttributes = QComboBox()
        self.lstConditionAttributes.addItem("NAME")
        self.lstConditionAttributes.addItem("PURPOSE")
        self.lstConditionAttributes.addItem("FUNCTION")
        self.hBoxLayoutCondition.addWidget(self.lstConditionAttributes)
        
        self.lstConditionRule = QComboBox()
        self.lstConditionRule.addItem("Equal")
        self.lstConditionRule.addItem("Not Equal")
        self.lstConditionRule.addItem("Matchwild")
        self.lstConditionRule.addItem("Greater")
        self.lstConditionRule.addItem("Less")
        self.lstConditionRule.addItem("Greater Equal")
        self.lstConditionRule.addItem("Less Equal")
        self.hBoxLayoutCondition.addWidget(self.lstConditionRule)
        
        self.txtConditionValue = QLineEdit("")
        self.hBoxLayoutCondition.addWidget(self.txtConditionValue)

        self.lblColumns = QLabel("Columns")
        self.hBoxLayoutColumns = QHBoxLayout(self)  
        self.lstAttributes = QComboBox()
        self.lstAttributes.addItem("Name")
        self.lstAttributes.addItem("Temperature")
        self.lstAttributes.addItem("Purpose")
        self.lstAttributes.addItem("Pressure")
        self.lstAttributes.addItem("Bore")
        self.lstAttributes.addItem("Pspec")
        
        self.btnAddColumn = QPushButton(QT_TRANSLATE_NOOP("Admin", "+"))
        self.btnAddColumn.resize(10, 10)
        
        self.hBoxLayoutColumns.addWidget(self.lstAttributes)
        self.hBoxLayoutColumns.addWidget(self.btnAddColumn)
        
        self.lblHierarchy = QLabel("Hierarchy")
        self.hBoxLayoutHierarchy = QHBoxLayout(self)  
        self.txtHierarchy = QLineEdit("/*")
        self.btnHierarchy = QPushButton(QT_TRANSLATE_NOOP("Admin", "CE"))
        self.btnHierarchy.resize(10, 10)
        
        self.hBoxLayoutHierarchy.addWidget(self.txtHierarchy)
        self.hBoxLayoutHierarchy.addWidget(self.btnHierarchy)        
               
        self.btnRunReport = QPushButton(QT_TRANSLATE_NOOP("Admin", "Run Report"))

        self.tablePreview = QTableWidget()
        self.tablePreview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablePreview.setAlternatingRowColors(True)
        self.tablePreview.setGridStyle(Qt.SolidLine)
        self.tablePreview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablePreview.horizontalHeader().setStretchLastSection(False)
        self.tablePreview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.tablePreview.verticalHeader().setMinimumSectionSize(16)
        #self.tablePreview.verticalHeader().setDefaultSectionSize(18)
        
        #self.lblType.activated.connect(self.callCheckType)
        #self.txtCondition.clicked.connect(self.callCheckCondition)
        #self.txtHierarchy.clicked.connect(self.callCheckType)
        
        self.btnAddColumn.clicked.connect(self.callAddColumn)
        self.btnHierarchy.clicked.connect(self.callCE)
        self.btnRunReport.clicked.connect(self.callRunReport)
        
        self.grid.addWidget( self.lblType, 0, 0 )
        self.grid.addWidget( self.lstType, 0, 1 )        
        self.grid.addWidget( self.lblCondition, 1, 0 )
        self.grid.addLayout( self.hBoxLayoutCondition, 1, 1 )        
        self.grid.addWidget( self.lblColumns, 2, 0 )
        self.grid.addLayout( self.hBoxLayoutColumns, 2, 1 )        
        self.grid.addWidget( self.lblHierarchy, 3, 0 )
        self.grid.addLayout( self.hBoxLayoutHierarchy, 3, 1 )        
 
        self.vBoxLayout.addLayout(self.grid)   
        self.vBoxLayout.addWidget(self.btnRunReport)  
        self.vBoxLayout.addWidget(self.tablePreview)  


    # setupUi
    
    def callAddColumn(self):      
        #df = pd.DataFrame((some_Data),('z','T'))
        #self.data.setRowCount(len(df))
        for k in self.ColumnsHeaders:
            #if self.lstAttributes.currentText not k:
        
        self.ColumnsHeaders.append(self.lstAttributes.currentText)
        self.tablePreview.setColumnCount(len(self.ColumnsHeaders))
        self.tablePreview.setHorizontalHeaderLabels(self.ColumnsHeaders)
    
    def callCE(self):
        print(PipeCad.CurrentItem().Name)
        self.txtHierarchy.text = "/" + PipeCad.CurrentItem().Name
    
    def callRunReport(self):
        self.tablePreview.clear()
        self.tablePreview.setRowCount(0)
        self.tablePreview.setColumnCount(len(self.ColumnsHeaders))
        self.tablePreview.setHorizontalHeaderLabels(self.ColumnsHeaders)
        print(self.ColumnsHeaders)
        aCollection = PipeCad.CollectItem(self.lstType.currentText, PipeCad.GetItem(self.txtHierarchy.text) )      
        for i in range( len(aCollection) ):
            aRow = self.tablePreview.rowCount
            self.tablePreview.insertRow(aRow)
            for j in range( len(self.ColumnsHeaders) ):           
                self.tablePreview.setItem(aRow, j, QTableWidgetItem( getattr(aCollection[i] , self.ColumnsHeaders[j] ) ) )

# Singleton Instance.
adlgReports = dlgReports(PipeCad)

def RunReport():
    adlgReports.show()
# Show
