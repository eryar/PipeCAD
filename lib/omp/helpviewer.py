from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from pipecad import *

class HelpDialog(QDialog):
    """docstring for HelpViewer"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    
    def setupUi(self):
        # self.setWindowTitle(QT_TRANSLATE_NOOP("Admin", " PipeCAD Help "))
        # self.resize(1000, 600)
        # 
        # style = self.style()
        # 
        # 
        # self.btnHome = QToolButton()
        # self.btnHome.setText("Home") 
        # 
        # self.btnBackward = QToolButton()
        # self.btnBackward.setText("Backward")
        #         
        # self.btnForward = QToolButton()
        # self.btnForward.setText("Forward")   
        # 
        # self.btnPrint = QToolButton()
        # self.btnPrint.setText("Print")  
        # 
        # self.lstLanguages = QComboBox()
        # self.lstLanguages.setFocusPolicy(Qt.NoFocus)
        # 
        # help_path = os.getenv('PIPECAD_HELP', default = None)
        # for lang_folder in os.listdir( help_path ):
        #     lang_full_path = os.path.join( help_path, lang_folder )
        #     if os.path.isdir( lang_full_path ) and lang_folder != 'images':
        #         self.lstLanguages.addItem( lang_folder )
        #    
        # 
        # 
        # #self.btnHome.setCheckable(True)
        # #self.btnHome.setAutoExclusive(True)
        # 
        # 
        # self.toolBar = QToolBar(self)
        # self.toolBar.addWidget(self.btnHome)
        # self.toolBar.addWidget(self.btnBackward)
        # self.toolBar.addWidget(self.btnForward)
        # self.toolBar.addWidget(self.btnPrint)
        # self.toolBar.addWidget(self.lstLanguages)
        # 
        # 
        # #channel = QWebChannel()
        # ##channel.registerObject("content", document)
        # #markdown_url = QUrl.fromUserInput( help_path + "en/index.md" )
        # #self.view = QWebEngineView()
        # #self.view.page().setWebChannel(channel)
        # #url = QUrl.fromLocalFile(fmarkdown_url)
        # #self.view.load(url)
        # #self.view.resize(640, 480)
        # #self.view.show()
        # 
        # 
        # self.vLayout = QVBoxLayout(self)
        # self.vLayout.addWidget(self.toolBar)
        # #self.vLayout.addWidget(self.view)
        # self.vLayout.addStretch()
        # self.setLayout(self.vLayout)
        
        navigation = self.addToolBar('Navigation')
        style = self.style()
        self.back = navigation.addAction('Back')
        self.back.setIcon(style.standardIcon(style.SP_ArrowBack))
        self.forward = navigation.addAction('Forward')
        self.forward.setIcon(style.standardIcon(style.SP_ArrowForward))
        self.reload = navigation.addAction('Reload')
        self.reload.setIcon(style.standardIcon(style.SP_BrowserReload))
        self.stop = navigation.addAction('Stop')
        self.stop.setIcon(style.standardIcon(style.SP_BrowserStop))
        self.urlbar = qtw.QLineEdit()
        navigation.addWidget(self.urlbar)
        self.go = navigation.addAction('Go')
        self.go.setIcon(style.standardIcon(style.SP_DialogOkButton))

        # single browser view
        #webview = qtwe.QWebEngineView()
        #self.setCentralWidget(webview)
        #webview.load(qtc.QUrl('http://www.alandmoore.com'))
        #self.go.triggered.connect(lambda: webview.load(
        #    qtc.QUrl(self.urlbar.text())))
        #self.back.triggered.connect(webview.back)
        #self.forward.triggered.connect(webview.forward)
        #self.reload.triggered.connect(webview.reload)
        #self.stop.triggered.connect(webview.stop)

        # browser tabs
        self.tabs = qtw.QTabWidget(
            tabsClosable=True, movable=True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.new = qtw.QPushButton('New')
        self.tabs.setCornerWidget(self.new)
        self.setCentralWidget(self.tabs)

        self.back.triggered.connect(self.on_back)
        self.forward.triggered.connect(self.on_forward)
        self.reload.triggered.connect(self.on_reload)
        self.stop.triggered.connect(self.on_stop)
        self.go.triggered.connect(self.on_go)
        self.urlbar.returnPressed.connect(self.on_go)
        self.new.clicked.connect(self.add_tab)

        # Profile sharing
        self.profile = qtwe.QWebEngineProfile()

        # History
        history_dock = qtw.QDockWidget('History')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, history_dock)
        self.history_list = qtw.QListWidget()
        history_dock.setWidget(self.history_list)
        self.tabs.currentChanged.connect(self.update_history)
        self.history_list.itemDoubleClicked.connect(self.navigate_history)

        # Altering Settings
        settings = qtwe.QWebEngineSettings.defaultSettings()
        settings.setFontFamily(
            qtwe.QWebEngineSettings.SansSerifFont, 'Impact')
        settings.setAttribute(
            qtwe.QWebEngineSettings.PluginsEnabled, True)


        # Text search feature
        find_dock = qtw.QDockWidget('Search')
        self.addDockWidget(qtc.Qt.BottomDockWidgetArea, find_dock)
        self.find_text = qtw.QLineEdit()
        find_dock.setWidget(self.find_text)
        self.find_text.textChanged.connect(self.text_search)
        # init javascript
        with open('finder.js', 'r') as fh:
            self.finder_js = fh.read()
        # using QWebEngineScript
        self.finder_script = qtwe.QWebEngineScript()
        self.finder_script.setSourceCode(self.finder_js)
        # Ensure that our created functions exist within the main JS environment
        self.finder_script.setWorldId(qtwe.QWebEngineScript.MainWorld)

        self.add_tab()

    def on_back(self):
        self.tabs.currentWidget().back()

    def on_forward(self):
        self.tabs.currentWidget().forward()

    def on_reload(self):
        self.tabs.currentWidget().reload()

    def on_stop(self):
        self.tabs.currentWidget().stop()

    def on_go(self):
        self.tabs.currentWidget().load(
            qtc.QUrl(self.urlbar.text()))
            
    def showHelpViewer(self):
        self.show()

# Singleton Instance.
adlgHelp = HelpDialog(PipeCad)

def showReport():
    adlgHelp.show()
# Show
