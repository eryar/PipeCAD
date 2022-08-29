from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

import pandas as pd

class ReportDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.ColumnsHeaders = []
        self.setupUi()
    # __init__

    def setupUi(self):
        
        self.resize(500, 400)
        self.setWindowTitle(self.tr("PipeCAD - Report"))
        
        self.vBoxLayMain = QVBoxLayout(self)        
        self.grid = QGridLayout()
        
        self.lblType = QLabel("Element Type")
        self.lstType = QComboBox()
        self.lstType.addItem("")
        self.lstType.addItem("ATTA")
        self.lstType.addItem("BEND")
        self.lstType.addItem("BOX")
        self.lstType.addItem("BRAN")
        self.lstType.addItem("CAP")
        self.lstType.addItem("CLOS")
        self.lstType.addItem("CONE")
        self.lstType.addItem("COUP")
        self.lstType.addItem("CROS")
        self.lstType.addItem("CTOR")
        self.lstType.addItem("CYLI")
        self.lstType.addItem("DISH")
        self.lstType.addItem("ELBO")
        self.lstType.addItem("EQUI")
        self.lstType.addItem("EXTR")
        self.lstType.addItem("FILT")
        self.lstType.addItem("FLAN")
        self.lstType.addItem("FRMW")
        self.lstType.addItem("FTUB")
        self.lstType.addItem("GASK")
        self.lstType.addItem("INST")
        self.lstType.addItem("LADD")
        self.lstType.addItem("LOOP")
        self.lstType.addItem("LSTR")
        self.lstType.addItem("NBOX")
        self.lstType.addItem("NCON")
        self.lstType.addItem("NCYL")
        self.lstType.addItem("NDIS")
        self.lstType.addItem("NOZZ")
        self.lstType.addItem("NPYR")
        self.lstType.addItem("NRTO")
        self.lstType.addItem("NSNO")
        self.lstType.addItem("NXTR")
        self.lstType.addItem("OLET")
        self.lstType.addItem("PANE")
        self.lstType.addItem("PAVE")
        self.lstType.addItem("PCOM")
        self.lstType.addItem("PIPE")
        self.lstType.addItem("PLOO")
        self.lstType.addItem("PYRA")
        self.lstType.addItem("REDU")
        self.lstType.addItem("RTOR")
        self.lstType.addItem("SBFR")
        self.lstType.addItem("SCTN")
        self.lstType.addItem("SITE")
        self.lstType.addItem("SNOU")
        self.lstType.addItem("STRU")
        self.lstType.addItem("SUBE")
        self.lstType.addItem("SUBS")
        self.lstType.addItem("TEE")
        self.lstType.addItem("TRAP")
        self.lstType.addItem("UNIO")
        self.lstType.addItem("VALV")
        self.lstType.addItem("VERT")
        self.lstType.addItem("VFWA")
        self.lstType.addItem("VTWA")
        self.lstType.addItem("WELD")
        self.lstType.addItem("ZONE")
                
        # self.hBoxLayoutCondition = QHBoxLayout(self)   
        # self.lblCondition = QLabel("Condition")
        # self.lstConditionAttributes = QComboBox()
        # self.lstConditionAttributes.addItem("Name")
        # self.lstConditionAttributes.addItem("Description")
        # self.lstConditionAttributes.addItem("Purpose")
        # self.lstConditionAttributes.addItem("Function")
        # self.lstConditionAttributes.addItem("Owner")
        # self.lstConditionAttributes.addItem("Lock")
        # self.lstConditionAttributes.addItem("RefNo")
        # self.hBoxLayoutCondition.addWidget(self.lstConditionAttributes)
        # 
        # self.lstConditionRule = QComboBox()
        # self.lstConditionRule.addItem("Equal")
        # self.lstConditionRule.addItem("Not Equal")
        # self.lstConditionRule.addItem("Matchwild")
        # self.lstConditionRule.addItem("Greater")
        # self.lstConditionRule.addItem("Less")
        # self.lstConditionRule.addItem("Greater Equal")
        # self.lstConditionRule.addItem("Less Equal")
        # self.hBoxLayoutCondition.addWidget(self.lstConditionRule)
        # 
        # self.txtConditionValue = QLineEdit("")
        # self.hBoxLayoutCondition.addWidget(self.txtConditionValue)

        self.lblColumns = QLabel("Columns")
        self.hBoxLayoutColumns = QHBoxLayout(self)  
        self.lstAttributes = QComboBox()
        self.lstAttributes.addItem("Name")
        self.lstAttributes.addItem("Description")
        self.lstAttributes.addItem("Purpose")
        self.lstAttributes.addItem("Function")
        self.lstAttributes.addItem("Owner")
        self.lstAttributes.addItem("Lock")
        self.lstAttributes.addItem("RefNo")
        
        self.btnAddColumn = QPushButton(QT_TRANSLATE_NOOP("Admin", "+"))
        self.btnAddColumn.setMaximumSize( 40 , 40 )    
        
        self.btnRemoveColumn = QPushButton(QT_TRANSLATE_NOOP("Admin", "-"))
        self.btnRemoveColumn.setMaximumSize( 40 , 40 )
        
        self.hBoxLayoutColumns.addWidget(self.lstAttributes)
        self.hBoxLayoutColumns.addWidget(self.btnAddColumn)
        self.hBoxLayoutColumns.addWidget(self.btnRemoveColumn)
        
        self.lblHierarchy = QLabel("Hierarchy")
        self.hBoxLayoutHierarchy = QHBoxLayout(self)  
        self.txtHierarchy = QLineEdit("/*")
        self.btnHierarchy = QPushButton(QT_TRANSLATE_NOOP("Admin", "CE"))
        self.btnHierarchy.setMaximumSize( 40 , 40 )
        
        self.hBoxLayoutHierarchy.addWidget(self.txtHierarchy)
        self.hBoxLayoutHierarchy.addWidget(self.btnHierarchy)        
     
        self.btnRunReport = QPushButton(QT_TRANSLATE_NOOP("Admin", "Run Report"))
        self.btnSaveToExcel = QPushButton(QT_TRANSLATE_NOOP("Admin", "Save to Excel file"))

        self.hBoxLayButtons = QHBoxLayout(self)           
        self.hBoxLayButtons.addWidget(self.btnRunReport)
        self.hBoxLayButtons.addWidget(self.btnSaveToExcel)
        
        self.tablePreview = QTableWidget()
        self.tablePreview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablePreview.setAlternatingRowColors(True)
        self.tablePreview.setGridStyle(Qt.SolidLine)
        self.tablePreview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablePreview.horizontalHeader().setStretchLastSection(False)
        self.tablePreview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        #self.lblType.activated.connect(self.callCheckType)
        #self.txtCondition.clicked.connect(self.callCheckCondition)
        #self.txtHierarchy.clicked.connect(self.callCheckType)
        
        self.btnAddColumn.clicked.connect(self.callAddColumn)
        self.btnRemoveColumn.clicked.connect(self.callRemoveColumn)
        self.btnHierarchy.clicked.connect(self.callCE)
        self.btnRunReport.clicked.connect(self.callRunReport)
        self.btnSaveToExcel.clicked.connect(self.callSaveToExcel)
        
        self.grid.addWidget( self.lblType, 0, 0 )
        self.grid.addWidget( self.lstType, 0, 1 )        
        #self.grid.addWidget( self.lblCondition, 1, 0 )
        #self.grid.addLayout( self.hBoxLayoutCondition, 1, 1 )        
        self.grid.addWidget( self.lblColumns, 1, 0 )
        self.grid.addLayout( self.hBoxLayoutColumns, 1, 1 )        
        self.grid.addWidget( self.lblHierarchy, 2, 0 )
        self.grid.addLayout( self.hBoxLayoutHierarchy, 2, 1 )        
 
        self.vBoxLayMain.addLayout(self.grid)   
        self.vBoxLayMain.addLayout(self.hBoxLayButtons)  
        self.vBoxLayMain.addWidget(self.tablePreview)  
    # setupUi
    
    def callAddColumn(self):      
        if_column_exists = False
        for k in self.ColumnsHeaders:
            if self.lstAttributes.currentText == k:
                if_column_exists = True
       
        if if_column_exists == False: 
            self.ColumnsHeaders.append(self.lstAttributes.currentText)
        
        self.tablePreview.setColumnCount(len(self.ColumnsHeaders))
        self.tablePreview.setHorizontalHeaderLabels(self.ColumnsHeaders)    
            
    def callRemoveColumn(self):      
        self.tablePreview.clear()
        self.tablePreview.setRowCount(0)
        for k in self.ColumnsHeaders:
            if self.lstAttributes.currentText == k:
                self.ColumnsHeaders.remove(self.lstAttributes.currentText)
               
        self.tablePreview.setColumnCount(len(self.ColumnsHeaders))
        self.tablePreview.setHorizontalHeaderLabels(self.ColumnsHeaders)  
    
    def callCE(self):
        if not PipeCad.CurrentItem().Name:
            self.txtHierarchy.text = "/*"
        else:
            self.txtHierarchy.text = "/" + PipeCad.CurrentItem().Name
    
    def callSaveToExcel(self):
        df = pd.DataFrame()
        savePath = QFileDialog.getSaveFileName( None, "Save Report to Excel file", "Report.xlsx", "Excel files (*.xlsx)")        
        
        rows = self.tablePreview.rowCount
        columns = self.tablePreview.columnCount      

        for i in range(rows):            
            for j in range(columns):                
                df.loc[i, j] = str(self.tablePreview.item(i, j).text())
                
        df.to_excel((savePath), header = self.ColumnsHeaders, index = 0)
        
    def callRunReport(self):
        self.tablePreview.clear()
        self.tablePreview.setRowCount(0)
        self.tablePreview.setColumnCount(len(self.ColumnsHeaders))
        self.tablePreview.setHorizontalHeaderLabels(self.ColumnsHeaders)
        aCollection = PipeCad.CollectItem(self.lstType.currentText, PipeCad.GetItem(self.txtHierarchy.text) )      
        for i in range( len(aCollection) ):
            aRow = self.tablePreview.rowCount
            self.tablePreview.insertRow(aRow)
            for j in range( len(self.ColumnsHeaders) ):           
                self.tablePreview.setItem(aRow, j, QTableWidgetItem( getattr(aCollection[i] , self.ColumnsHeaders[j] ) ) )

# Singleton Instance.
aReportDialog = ReportDialog(PipeCad)

def showReport():
    aReportDialog.show()
# Show
