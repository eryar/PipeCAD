from PythonQt.QtCore import *
from PythonQt.QtGui import *

import re
import os
import urllib.request
import signal
import argparse
import json
import sys
import ssl

from pipecad import *

class dlgUpdateFromGithub(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
   
    def setupUi(self):
        self.resize(500, 50)
        self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", "Update PipeCAD components"))
        
        self.vBoxLayout = QVBoxLayout(self)        
        self.grid = QGridLayout()
        
        self.lblLibrary = QLabel(QT_TRANSLATE_NOOP("Admin", "Library"))
        self.txtLibrary = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/lib")
        self.txtLibrary.setEnabled(True)

        self.lblUic = QLabel(QT_TRANSLATE_NOOP("Admin", "Menu"))
        self.txtUic = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/uic")
        self.txtUic.setEnabled(True)
        
        self.lblSettings = QLabel(QT_TRANSLATE_NOOP("Admin", "Settings"))
        self.txtSettings = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/settings")
        self.txtSettings.setEnabled(True)
        
        self.lblDoc = QLabel(QT_TRANSLATE_NOOP("Admin", "Documentation"))
        self.txtDoc = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/docs")
        self.txtDoc.setEnabled(True)
        
        self.lblTranslation = QLabel(QT_TRANSLATE_NOOP("Admin", "Translation"))
        self.txtTranslation = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/translations")
        self.txtTranslation.setEnabled(True)       
        
        self.lblTemplate = QLabel(QT_TRANSLATE_NOOP("Admin", "Templates"))
        self.txtTemplate = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/templates")
        self.txtTemplate.setEnabled(True)
  
        self.lblCatalogue = QLabel(QT_TRANSLATE_NOOP("Admin", "Catalogues"))
        self.txtCatalogue = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/catalogues")
        self.txtCatalogue.setEnabled(True)
  
        self.lblSettings = QLabel(QT_TRANSLATE_NOOP("Admin", "Settings"))
        self.txtSettings = QLineEdit("https://github.com/eryar/PipeCAD/tree/main/settings")
        self.txtSettings.setEnabled(True)

        self.btnUpdateLibrary = QPushButton(QT_TRANSLATE_NOOP("Admin", "Update"))
        self.btnUpdateLibrary.clicked.connect(self.RunUpdateLibrary)
        
        self.grid.addWidget( self.lblLibrary, 0, 0 )
        self.grid.addWidget( self.txtLibrary, 0, 1 )        
        self.grid.addWidget( self.lblUic, 1, 0 )
        self.grid.addWidget( self.txtUic, 1, 1 )        
        self.grid.addWidget( self.lblDoc, 2, 0 )
        self.grid.addWidget( self.txtDoc, 2, 1 )        
        self.grid.addWidget( self.lblTranslation, 3, 0 )
        self.grid.addWidget( self.txtTranslation, 3, 1 )        
        self.grid.addWidget( self.lblTemplate, 4, 0 )
        self.grid.addWidget( self.txtTemplate, 4, 1 )       
        self.grid.addWidget( self.lblCatalogue, 5, 0 )
        self.grid.addWidget( self.txtCatalogue, 5, 1 )       
        self.grid.addWidget( self.lblSettings, 6, 0 )
        self.grid.addWidget( self.txtSettings, 6, 1 )

        self.vBoxLayout.addLayout(self.grid)   
        self.vBoxLayout.addWidget(self.btnUpdateLibrary)   
            
    def RunUpdateLibrary(self):
        total_files_lib = self.download("https://github.com/eryar/PipeCAD/tree/main/lib", "c:\PipeCAD\\test\\lib")
        total_files_help = self.download("https://github.com/eryar/PipeCAD/tree/main/docs", "c:\PipeCAD\\test\\docs")
        total_files_catalogues = self.download("https://github.com/eryar/PipeCAD/tree/main/catalogues", "c:\PipeCAD\\test\\catalogues")
        total_files_uic = self.download("https://github.com/eryar/PipeCAD/tree/main/uic", "c:\PipeCAD\\test\\uic")
        total_files_library = self.download("https://github.com/eryar/PipeCAD/tree/main/lib", "c:\PipeCAD\\test\\lib")
        total_files_templates = self.download("https://github.com/eryar/PipeCAD/tree/main/templates", "c:\PipeCAD\\test\\templates")
        total_files_translations = self.download("https://github.com/eryar/PipeCAD/tree/main/translations", "c:\PipeCAD\\test\\translations")
        total_files_settings = self.download("https://github.com/eryar/PipeCAD/tree/main/settings", "c:\PipeCAD\\test\\settings")

    def create_url(self, url):
        """
        From the given url, produce a URL that is compatible with Github's REST API. Can handle blob or tree paths.
        """
        repo_only_url = re.compile(r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$")
        re_branch = re.compile("/(tree|blob)/(.+?)/")

        # Check if the given url is a url to a GitHub repo. If it is, tell the
        # user to use 'git clone' to download it
        if re.match(repo_only_url,url):
            sys.exit()

        # extract the branch name from the given url (e.g master)
        branch = re_branch.search(url)
        download_dirs = url[branch.end():]
        api_url = (url[:branch.start()].replace("github.com", "api.github.com/repos", 1) +
                  "/contents/" + download_dirs + "?ref=" + branch.group(2))
        return api_url, download_dirs


    def download(self, repo_url, output_dir):
        """ Downloads the files and directories in repo_url. If flatten is specified, the contents of any and all
         sub-directories will be pulled upwards into the root folder. """

        # generate the url which returns the JSON data
        api_url, download_dirs = self.create_url(repo_url)
        
        # To handle file names.
        if len(download_dirs.split(".")) == 0:
            dir_out = os.path.join(output_dir, download_dirs)
        else:
            dir_out = os.path.join(output_dir, "/".join(download_dirs.split("/")[:-1]))
 
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            response = urllib.request.urlretrieve(api_url)
            
        except KeyboardInterrupt:
            # when CTRL+C is pressed during the execution of this script,
            # bring the cursor to the beginning, erase the current line, and dont make a new line
            sys.exit()

            # make a directory with the name which is taken from
            # the actual repo

        os.makedirs(dir_out, exist_ok=True)
        
        # total files count
        total_files = 0

        with open(response[0], "r") as f:
            data = json.load(f)
            
            # getting the total number of files so that we
            # can use it for the output information later
            total_files += len(data)

            # If the data is a file, download it as one.
            if isinstance(data, dict) and data["type"] == "file":
                try:
                    # download the file
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(data["download_url"], os.path.join(dir_out, data["name"]))
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    return total_files
                except KeyboardInterrupt:
                    # when CTRL+C is pressed during the execution of this script,
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    sys.exit()

            for file in data:
                file_url = file["download_url"]
                file_name = file["name"]
                file_path = file["path"]

                path = file_path
                dirname = os.path.dirname(path)
                
                if dirname != '':
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                else:
                    pass
                    
                if file_url is not None:
                    try:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                        urllib.request.install_opener(opener)
                        # download the file
                        urllib.request.urlretrieve(file_url, path)

                    except KeyboardInterrupt:
                        # when CTRL+C is pressed during the execution of this script,
                        # bring the cursor to the beginning, erase the current line, and dont make a new line
                        sys.exit()
                else:
                    self.download(file["html_url"], download_dirs)
                    
        return total_files
        

# UpdateFromGithub

# Singleton Instance.
aUpdateFromGithubDlg = dlgUpdateFromGithub(PipeCad)

def show():
    aUpdateFromGithubDlg.show()