from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

import os
import imp
import importlib 
import inspect

class LibrariesDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.PythonLibraries = os.getenv('PYTHONPATH').split(";")
        self.PythonFiles = []
        self.iconsLibraryPath = os.path.dirname(os.path.abspath(__file__)).replace( "\lib\omp","\lib\pipecad" ) + "/icons"
        
        self.setupUi()
    # __init__

    def setupUi(self):
        
        self.setWindowTitle( QT_TRANSLATE_NOOP( "Admin", "PipeCAD - Reload Python Libraries" ) )
        
        self.txtSearch = QLineEdit("")
        
        self.btnFilterClear = QPushButton("")
        self.btnFilterClear.setToolTip( QT_TRANSLATE_NOOP( "Common", "Clear Filter" ) )
        self.btnFilterClear.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/common/100x100_filter_clear.png' ) ) )
        self.btnFilterClear.setIconSize( QSize( 16, 16 ) )
        self.btnFilterClear.setMinimumSize( 24, 24 )  
        self.btnFilterClear.setMaximumSize( 24, 24 )  
        
        self.lstLibrariesFiles = QListWidget()
        self.lstLibrariesFiles.setSelectionMode(1)
        self.lstLibrariesFiles.setMinimumSize( 350, 300 )  
        self.lstLibrariesFiles.setMaximumSize( 350, 300 )  
        
        
        self.btnReload = QPushButton( QT_TRANSLATE_NOOP( "Admin", "Reload" ) )
        self.btnReload.setMinimumSize( 350, 24 )  
        self.btnReload.setMaximumSize( 350, 24 )  
        
        self.hBoxLayFilter = QHBoxLayout()
        self.hBoxLayFilter.addWidget(self.txtSearch)
        self.hBoxLayFilter.addWidget(self.btnFilterClear)
        
        self.vBoxLayMain = QVBoxLayout(self)
        self.vBoxLayMain.addLayout(self.hBoxLayFilter)
        self.vBoxLayMain.addWidget(self.lstLibrariesFiles)
        self.vBoxLayMain.addWidget(self.btnReload)
        
        self.callCollect()
         
        # Callbacks
        self.txtSearch.textChanged.connect(self.callSearch)
        self.btnFilterClear.clicked.connect(self.callFilterClear)
        self.btnReload.clicked.connect(self.callReload)
        
    def callReload(self):
        for item in self.lstLibrariesFiles.selectedItems():
            imp.reload( importlib.import_module ( item.text() ) )
            # TODO: add method for path of module print("<module '" + item.text + "'from '" + inspect.getfile(item.text()) "'>" )
            print( QT_TRANSLATE_NOOP( "Common", "<module '" ) + item.text() + QT_TRANSLATE_NOOP( "Common", "' is reloaded>" ) )

    def callSearch(self):
        self.lstLibrariesFiles.clear()
        for macro in self.PythonFiles:
            if self.txtSearch.text.upper() in macro.upper():
                self.lstLibrariesFiles.addItem(macro)

    def callCollect(self):
        for sLib in self.PythonLibraries:
            if "site-packages" in sLib or "" == sLib:
                continue 
            
            full_file_paths = self.get_filepaths(sLib)
            for macro in full_file_paths:
                module = macro.partition(sLib)[2].partition(".py")[0].replace("\\",".").partition(".")[2]
                self.PythonFiles.append(module)
                self.lstLibrariesFiles.addItem( module )
        self.lstLibrariesFiles.sortItems()
    
    def callFilterClear(self):
        self.lstLibrariesFiles.clear()
        self.txtSearch.clear()

        for macro in self.PythonFiles:
            if self.txtSearch.text.upper() in macro.upper():
                self.lstLibrariesFiles.addItem(macro)
            
    def get_filepaths(self, directory):
        """
        This function will generate the file names in a directory 
        tree by walking the tree either top-down or bottom-up. For each 
        directory in the tree rooted at directory top (including top itself), 
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                if ".py" in filename and "__.py" not in filename:
                    # Join the two strings in order to form the full filepath.
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)  # Add it to the list.

        return file_paths  # Self-explanatory.
        # Types dictionary 

# Singleton Instance.
aLibraryReload = LibrariesDialog(PipeCad)
          
def show():
    aLibraryReload.show()
# Show

def reload():  
    PythonLibraries = os.getenv('PYTHONPATH').split(";")
    for sLib in PythonLibraries:
        if "site-packages" in sLib or "" == sLib:
            continue 
       
        full_file_paths = aLibraryReload.get_filepaths(sLib)
        for macro in full_file_paths:
            module = macro.partition(sLib)[2].partition(".py")[0].replace("\\",".").partition(".")[2]
            imp.reload( importlib.import_module ( module ) )
            print( QT_TRANSLATE_NOOP( "Common", "<module '" ) + module + QT_TRANSLATE_NOOP( "Common", "' is reloaded>" ) )
   