from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

class dlgSample(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(500, 30)
        self.setWindowTitle(self.tr("PipeCAD - Sample Utility"))

        self.verticalLayout = QVBoxLayout(self)
        self.lblText = QLabel("Sample Form Text")
        self.verticalLayout.addWidget(self.lblText)
    # setupUi

# Singleton Instance.
aSample = dlgSample(PipeCad)

def ShowSample():
    aSample.show()
# Show