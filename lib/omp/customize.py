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
        self.resize(500, 400)
       
        self.vBoxLayMain = QVBoxLayout()
        
        self.treeRibbonMenu = QTreeView()
        self.treeRibbonMenu.setMaximumSize( 150 , 300 )  
        self.treeRibbonMenu.setRootIsDecorated(True)

        self.groupModules = QGroupBox("Modules")        
        self.hBoxLayModules = QHBoxLayout()
        self.groupModules.setLayout(self.hBoxLayModules)
        
        self.rbtnDesign = QRadioButton("Design")
        self.rbtnDesign.setChecked(True)
        self.hBoxLayModules.addWidget(self.rbtnDesign)
        
        self.rbtnParagon = QRadioButton("Paragon")
        self.hBoxLayModules.addWidget(self.rbtnParagon)
        
        self.rbtnAdmin = QRadioButton("Admin")
        self.hBoxLayModules.addWidget(self.rbtnAdmin)
        
        self.rbtnDesign.toggled.connect( lambda: self.callModuleSwitch(self.rbtnDesign) )
        self.rbtnParagon.toggled.connect( lambda: self.callModuleSwitch(self.rbtnParagon) )
        self.rbtnAdmin.toggled.connect( lambda: self.callModuleSwitch(self.rbtnAdmin) )
        
        self.groupRibbonMenu = QGroupBox("Ribbon Menu")
        self.vBoxLayRibbonMenu = QVBoxLayout()
        self.groupRibbonMenu.setLayout(self.vBoxLayRibbonMenu)
       
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
        
        self.hBoxLayGroups = QHBoxLayout()
        self.hBoxLayGroups.addWidget(self.groupRibbonMenu) 
        self.hBoxLayGroups.addWidget(self.groupActions) 
        
        self.hBoxLayButttons = QHBoxLayout()
        self.btnApply =  QPushButton("Apply")
        self.btnCancel = QPushButton("Cancel")
        self.hBoxLayButttons.addWidget(self.btnApply)
        self.hBoxLayButttons.addWidget(self.btnCancel)
        
        self.vBoxLayMain.addWidget(self.groupModules)
        self.vBoxLayMain.addLayout(self.hBoxLayGroups)
        self.vBoxLayMain.addLayout(self.hBoxLayButttons)
        self.setLayout(self.vBoxLayMain)
    
    def callModuleSwitch(self, button):
        if button.text == "Design":  
            if button.isChecked() == True:
                self.callReadMenuXml(button)
        elif button.text == "Paragon": 
            if button.isChecked() == True:
                self.callReadMenuXml(button)
        elif button.text == "Admin": 
            if button.isChecked() == True:
                self.callReadMenuXml(button)
 
    def callReadMenuXml(self, button):
        print( "PipeCAD." + button.text + ".uic")
        print( "PipeCAD." + button.text + ".xml")

# Singleton Instance.
aCustomizeDialog = CustomizeDialog(PipeCad)

<<<<<<< Updated upstream
def showCustomize():
=======
def showCustomizeDialog():
>>>>>>> Stashed changes
    aCustomizeDialog.show()