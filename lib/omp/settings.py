from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

class SettingsDialog(QDialog):
    """"Settings Window"""
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    
    def setupUi(self):
        self.setWindowTitle("PipeCad Setting")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pageCombo = QComboBox()
        self.pageCombo.addItem("Page 1")
        self.pageCombo.addItem("Page 2")
        self.pageCombo.currentIndexChanged.connect(self.switchPage)
        
        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        
        # Create the first page
        self.pageOne = QWidget()
        self.pageOneLayout = QFormLayout()
        self.pageOneLayout.addRow("Name:", QLineEdit())
        self.pageOneLayout.addRow("Address:", QLineEdit())
        self.pageOne.setLayout(self.pageOneLayout)
        self.stackedLayout.addWidget(self.pageOne)
        
        # Create the second page
        self.pageTwo = QWidget()
        self.pageTwoLayout = QFormLayout()
        self.pageTwoLayout.addRow("Job:", QLineEdit())
        self.pageTwoLayout.addRow("Department:", QLineEdit())
        self.pageTwo.setLayout(self.pageTwoLayout)
        self.stackedLayout.addWidget(self.pageTwo)
        
        # Add the combo box and the stacked layout to the top-level layout
        layout.addWidget(self.pageCombo)
        layout.addLayout(self.stackedLayout)
        layout.addStretch()
        self.setLayout(layout)
    
        #Connect to db 
        #Read menu group, submenus, menu description, group description, menu value type, menu value 
    
    def switchPage(self):
        print(self.pageCombo.currentIndex())

# Singleton Instance.
aSettings = SettingsDialog(PipeCad)

def showSettings():
    aSettings.show()