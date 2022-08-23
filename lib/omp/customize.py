from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

class CustomizeDialog(QDialog):
    """"CustomizeDialog Window"""
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    
    def setupUi(self):
        self.setWindowTitle("PipeCAD - Customize Ribbon Menu")

        self.vBoxLayMain = QVBoxLayout()
        
        self.hBoxLayGroups = QHBoxLayout()
        
        
        self.treeRibbonMenu = QTreeView()
        self.treeRibbonMenu.setRootIsDecorated(True)

        
        self.groupRibbonMenu = QGroupBox("Ribbon Menu")
        self.vBoxRibbonMenu = QVBoxLayout()
        self.groupRibbonMenu.setLayout(self.vBoxRibbonMenu)
        
        
        
        
        self.groupActions = QGroupBox("Actions")
        self.tableActions = QTableWidget()
        self.tableActions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableActions.setAlternatingRowColors(True)
        self.tableActions.setGridStyle(Qt.SolidLine)
        self.tableActions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableActions.horizontalHeader().setStretchLastSection(True)
        self.tableActions.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableActions.verticalHeader().setMinimumSectionSize(16)
        self.tableActions.verticalHeader().setDefaultSectionSize(18)
        
        self.vBoxTableAction = QVBoxLayout()
        self.vBoxTableAction.addWidget(self.tableActions)
        self.groupActions.setLayout(self.vBoxTableAction)
        
        self.hBoxLayGroups.addWidget(self.groupRibbonMenu) 
        self.hBoxLayGroups.addWidget(self.groupActions) 
        
        self.hBoxLayButttons = QHBoxLayout()
        self.btnApply =  QPushButton("Apply")
        self.btnCancel = QPushButton("Cancel")
        self.hBoxLayButttons.addWidget(self.btnApply)
        self.hBoxLayButttons.addWidget(self.btnCancel)
        
        self.vBoxLayMain.addLayout(self.hBoxLayGroups)
        self.vBoxLayMain.addLayout(self.hBoxLayButttons)
        self.setLayout(self.vBoxLayMain)


# Singleton Instance.
aCustomizeDialog = CustomizeDialog(PipeCad)

def showCustomizeDialog():
    aCustomizeDialog.show()