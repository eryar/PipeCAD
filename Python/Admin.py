# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :: Welcome to PipeCAD!                                      ::
# ::  ____                        ____     ______  ____       ::
# :: /\  _`\   __                /\  _`\  /\  _  \/\  _`\     ::
# :: \ \ \L\ \/\_\  _____      __\ \ \/\_\\ \ \L\ \ \ \/\ \   ::
# ::  \ \ ,__/\/\ \/\ '__`\  /'__`\ \ \/_/_\ \  __ \ \ \ \ \  ::
# ::   \ \ \/  \ \ \ \ \L\ \/\  __/\ \ \L\ \\ \ \/\ \ \ \_\ \ ::
# ::    \ \_\   \ \_\ \ ,__/\ \____\\ \____/ \ \_\ \_\ \____/ ::
# ::     \/_/    \/_/\ \ \/  \/____/ \/___/   \/_/\/_/\/___/  ::
# ::                  \ \_\                                   ::
# ::                   \/_/                                   ::
# ::                                                          ::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# PipeCAD - Piping Design Software.
# Copyright (C) 2021 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 21:16 2021-09-16

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *

from PipeCAD import *

class AdminMain(QWidget):
    """docstring for AdminMain"""
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.teamDialog = TeamDialog(self)
        self.userDialog = UserDialog(self)
        self.mdbDialog = MdbDialog(self)
        self.dbDialog = DatabaseDialog(self)

        self.setupUi()

    # __init__

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        #self.groupBox = QGroupBox("Admin Elements")
        #self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()

        self.labelElements = QLabel("Elements")
        self.horizontalLayout.addWidget(self.labelElements)

        self.comboElements = QComboBox()
        self.comboElements.addItem("Teams")
        self.comboElements.addItem("Users")
        self.comboElements.addItem("Databases")
        self.comboElements.addItem("MDBs")

        aSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comboElements.setSizePolicy(aSizePolicy)

        self.comboElements.currentTextChanged.connect(self.elementChanged)

        self.horizontalLayout.addWidget(self.comboElements)

        self.buttonRefresh = QPushButton("Refresh List")
        self.horizontalLayout.addWidget(self.buttonRefresh)

        self.buttonRefresh.clicked.connect(self.refreshList)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        self.tableWidget.currentItemChanged.connect(self.currentItemChanged)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()

        self.buttonSort = QPushButton("Sort")
        self.horizontalLayout.addWidget(self.buttonSort)
        self.buttonSort.clicked.connect(self.sortList)

        self.comboSort = QComboBox()
        self.comboSort.addItem("Name")
        self.comboSort.addItem("Description")
        self.comboSort.setSizePolicy(aSizePolicy)
        self.horizontalLayout.addWidget(self.comboSort)

        self.labelFilter = QLabel("Filter")
        self.horizontalLayout.addWidget(self.labelFilter)

        self.lineFilter = QLineEdit("*")
        self.horizontalLayout.addWidget(self.lineFilter)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupOption = QGroupBox("Operations")
        self.verticalLayout.addWidget(self.groupOption)

        self.verticalLayout = QVBoxLayout(self.groupOption)

        self.horizontalLayout = QHBoxLayout()

        self.buttonCreate = QPushButton("Create")
        self.buttonCreate.clicked.connect(self.create)
        self.horizontalLayout.addWidget(self.buttonCreate)

        self.buttonCopy = QPushButton("Copy")
        self.buttonCopy.clicked.connect(self.copy)
        self.horizontalLayout.addWidget(self.buttonCopy)

        self.buttonModify = QPushButton("Modify")
        self.buttonModify.clicked.connect(self.modify)
        self.horizontalLayout.addWidget(self.buttonModify)

        self.buttonDelete = QPushButton("Delete")
        self.buttonDelete.clicked.connect(self.delete)
        self.horizontalLayout.addWidget(self.buttonDelete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.statItem = PipeCad.GetItem("/*S")
        self.tmwlItem = PipeCad.GetItem("/*T")
        self.uswlItem = PipeCad.GetItem("/*U")
        self.mdbwItem = PipeCad.GetItem("/*M")

    # setupUi
        
    def elementChanged(self, theElement):
        if theElement.startswith("Team"):
            self.buildTeamList()
        elif theElement.startswith("User"):
            self.buildUserList()
        elif theElement.startswith("MDB"):
            self.buildMdbList()
        elif theElement.startswith("Databases"):
            self.buildDbList()

        #self.tableWidget.resizeColumnsToContents()
    # elementChanged

    def currentItemChanged(self):
        aRow = self.tableWidget.currentRow()
        aItem = self.tableWidget.item(aRow, 0)
        if aItem is not None:
            PipeCad.SetCurrentItem(aItem.data(Qt.UserRole))
    # currentItemChanged

    def buildTeamList(self):
        aRow = 0
        aHeaderLabels = ["Name", "Description"]

        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)

        if self.tmwlItem == None:
            return

        aTeamItems = self.tmwlItem.Member
        for aTeamItem in aTeamItems:
            aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
            aItem.setData(Qt.UserRole, aTeamItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aTeamItem.Description))
            aRow += 1

    # buildTeamList

    def buildUserList(self):
        aRow = 0
        aHeaderLabels = ["Name", "Security", "Description"]
        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)
        
        if self.uswlItem == None:
            return

        aUserItems = self.uswlItem.Member
        for aUserItem in aUserItems:
            aItem = QTableWidgetItem("<USER> " + aUserItem.Name)
            aItem.setData(Qt.UserRole, aUserItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aUserItem.Security))
            self.tableWidget.setItem(aRow, 2, QTableWidgetItem(aUserItem.Description))
            aRow += 1

    # buildUserList

    def buildMdbList(self):
        aRow = 0
        aHeaderLabels = ["Name", "Description"]
        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)
        
        if self.mdbwItem == None:
            return

        aMdbItems = self.mdbwItem.Member
        for aMdbItem in aMdbItems:
            aItem = QTableWidgetItem("<MDB> " + aMdbItem.Name)
            aItem.setData(Qt.UserRole, aMdbItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aMdbItem.Description))
            aRow += 1

    # buildMdbList

    def buildDbList(self):
        aRow = 0
        aHeaderLabels = ["Name", "Type", "DB Number", "Description"]
        self.tableWidget.setRowCount(aRow)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(aHeaderLabels)

        self.comboSort.clear()
        self.comboSort.addItems(aHeaderLabels)
        
        if self.tmwlItem == None:
            return

        aDbItems = PipeCad.CollectItem("DB")
        for aDbItem in aDbItems:
            aItem = QTableWidgetItem("<DB> " + aDbItem.Name[1:])
            aItem.setData(Qt.UserRole, aDbItem)

            self.tableWidget.setRowCount(aRow + 1)
            self.tableWidget.setItem(aRow, 0, aItem)
            self.tableWidget.setItem(aRow, 1, QTableWidgetItem(aDbItem.DbType))
            self.tableWidget.setItem(aRow, 2, QTableWidgetItem(str(aDbItem.DbNumber)))
            self.tableWidget.setItem(aRow, 3, QTableWidgetItem(aDbItem.Description))
            aRow += 1

    # buildDbList

    def refreshList(self):
        aElement = self.comboElements.currentText
        self.elementChanged(aElement)
    # refreshList

    def sortList(self):
        aIndex = self.comboSort.currentIndex
        self.tableWidget.sortItems(aIndex)
    # sortList

    def create(self):
        aElement = self.comboElements.currentText
        if aElement.startswith("Team"):
            self.teamDialog.create()
        elif aElement.startswith("User"):
            self.userDialog.create()
        elif aElement.startswith("Database"):
            self.dbDialog.create()
        elif aElement.startswith("MDB"):
            self.mdbDialog.create()
        # if
    # create

    def copy(self):
        print("copy")
    # copy

    def modify(self):
        aElement = self.comboElements.currentText
        if aElement.startswith("Team"):
            self.teamDialog.modify()
        elif aElement.startswith("User"):
            self.userDialog.modify()
        elif aElement.startswith("Database"):
            self.dbDialog.modify()
        elif aElement.startswith("MDB"):
            self.mdbDialog.modify()
        # if

    # modify

    def delete(self):
        aItem = PipeCad.CurrentItem()
        aElement = self.comboElements.currentText
        if aElement.startswith("Team"):
            aReply = QMessageBox.question(self, "", "Okay to delete team " + aItem.Name[1:])
            if aReply == QMessageBox.Yes:
                PipeCad.DeleteItem("TEAM")
                self.buildTeamList()
            # if
        elif aElement.startswith("User"):
            aReply = QMessageBox.question(self, "", "Okay to delete user " + aItem.Name)
            if aReply == QMessageBox.Yes:
                PipeCad.DeleteItem("USER")
                self.buildUserList()
            # if
        elif aElement.startswith("Database"):
            aReply = QMessageBox.question(self, "", "Okay to delete database " + aItem.Name[1:])
            if aReply == QMessageBox.Yes:
                aItem.DeleteDatabase()
                PipeCad.DeleteItem("DB")
                self.buildDbList()
            # if
        elif aElement.startswith("MDB"):
            aReply = QMessageBox.question(self, "", "Okay to delete mdb " + aItem.Name)
            if aReply == QMessageBox.Yes:
                PipeCad.DeleteItem("MDB")
                self.buildMdbList()
            # if
        # if

        PipeCad.SaveWork()
    # delete


class TeamDialog(QDialog):
    """docstring for TeamDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel("Description")
        self.textDescription = QLineEdit()
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDescription)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupBox = QGroupBox("Team Membership")
        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.layoutTable = QVBoxLayout()
        self.labelProjectUsers = QLabel("Project Users")
        self.tableProjectUsers = QTableWidget()
        self.tableProjectUsers.setColumnCount(3)
        self.tableProjectUsers.setHorizontalHeaderLabels(["Name", "Security", "Description"])
        self.tableProjectUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectUsers.setAlternatingRowColors(True)
        self.tableProjectUsers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectUsers.setGridStyle(Qt.SolidLine)
        self.tableProjectUsers.horizontalHeader().setStretchLastSection(True)
        self.tableProjectUsers.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectUsers.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelProjectUsers)
        self.layoutTable.addWidget(self.tableProjectUsers)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.layoutButton = QVBoxLayout()
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.buttonAddUser = QToolButton()
        self.buttonAddUser.setArrowType(Qt.RightArrow)
        self.buttonAddUser.clicked.connect(self.addUser)
        self.layoutButton.addWidget(self.buttonAddUser)

        self.buttonDelUser = QToolButton()
        self.buttonDelUser.setArrowType(Qt.LeftArrow)
        self.buttonDelUser.clicked.connect(self.delUser)
        self.layoutButton.addWidget(self.buttonDelUser)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.horizontalLayout.addLayout(self.layoutButton)
        
        self.layoutTable = QVBoxLayout()
        self.labelTeamUsers = QLabel("Team Members")
        self.tableTeamUsers = QTableWidget()
        self.tableTeamUsers.setColumnCount(3)
        self.tableTeamUsers.setHorizontalHeaderLabels(["Name", "Security", "Description"])
        self.tableTeamUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableTeamUsers.setAlternatingRowColors(True)
        self.tableTeamUsers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableTeamUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableTeamUsers.setGridStyle(Qt.SolidLine)
        self.tableTeamUsers.horizontalHeader().setStretchLastSection(True)
        self.tableTeamUsers.verticalHeader().setMinimumSectionSize(16)
        self.tableTeamUsers.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelTeamUsers)
        self.layoutTable.addWidget(self.tableTeamUsers)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tmwlItem = PipeCad.GetItem("/*T")
        self.uswlItem = PipeCad.GetItem("/*U")
        self.teamItem = None

    # setupUi

    def init(self, theTeamItem = None):
        self.textName.setText("")
        self.textDescription.setText("")
        self.tableTeamUsers.setRowCount(0)
        self.tableProjectUsers.setRowCount(0)

        # Project Users.
        if self.uswlItem == None:
            return
        # if

        aTeamUserSet = set()
        
        if theTeamItem is not None:
            self.teamItem = theTeamItem
            self.textName.setText(theTeamItem.Name[1:])
            self.textDescription.setText(theTeamItem.Description)

            aTeamItems = PipeCad.CollectItem("LTEA", self.uswlItem)
            for aTeamItem in aTeamItems:
                if aTeamItem.Temf == theTeamItem:
                    aRow = self.tableTeamUsers.rowCount
                    self.tableTeamUsers.insertRow(aRow)

                    aUserItem = aTeamItem.Owner.Owner
                    aTeamUserSet.add(aUserItem)

                    aListItem = QTableWidgetItem(aUserItem.Name)
                    aListItem.setData(Qt.UserRole, aUserItem)

                    self.tableTeamUsers.setItem(aRow, 0, aListItem)
                    self.tableTeamUsers.setItem(aRow, 1, QTableWidgetItem(aUserItem.Security))
                    self.tableTeamUsers.setItem(aRow, 2, QTableWidgetItem(aUserItem.Description))
                # if
            # for
        # if

        aUserItems = self.uswlItem.Member
        for aUserItem in aUserItems:
            if aUserItem in aTeamUserSet:
                continue
            # if

            aRow = self.tableProjectUsers.rowCount
            self.tableProjectUsers.insertRow(aRow)

            aItem = QTableWidgetItem(aUserItem.Name)
            aItem.setData(Qt.UserRole, aUserItem)

            self.tableProjectUsers.setItem(aRow, 0, aItem)
            self.tableProjectUsers.setItem(aRow, 1, QTableWidgetItem(aUserItem.Security))
            self.tableProjectUsers.setItem(aRow, 2, QTableWidgetItem(aUserItem.Description))
        # for

        self.tableProjectUsers.resizeColumnsToContents()

        self.tableTeamUsers.resizeColumnsToContents()

    # init

    def create(self):
        self.setWindowTitle(self.tr("Create Team"))
        self.init()
        self.show()
    # createTeam

    def modify(self):
        self.setWindowTitle(self.tr("Modify Team"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modifyTeam

    def addUser(self):
        aRows = []
        for aItem in self.tableProjectUsers.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableProjectUsers.item(r, 0).clone()
            aSecurityItem = self.tableProjectUsers.item(r, 1).clone()
            aDescriptionItem = self.tableProjectUsers.item(r, 2).clone()

            aRow = self.tableTeamUsers.rowCount
            self.tableTeamUsers.insertRow(aRow)
            self.tableTeamUsers.setItem(aRow, 0, aNameItem)
            self.tableTeamUsers.setItem(aRow, 1, aSecurityItem)
            self.tableTeamUsers.setItem(aRow, 2, aDescriptionItem)

            self.tableProjectUsers.removeRow(r)

        self.tableTeamUsers.resizeColumnsToContents()
    # addUser

    def delUser(self):
        aRows = []
        for aItem in self.tableTeamUsers.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableTeamUsers.item(r, 0).clone()
            aSecurityItem = self.tableTeamUsers.item(r, 1).clone()
            aDescriptionItem = self.tableTeamUsers.item(r, 2).clone()

            aRow = self.tableProjectUsers.rowCount
            self.tableProjectUsers.insertRow(aRow)
            self.tableProjectUsers.setItem(aRow, 0, aNameItem)
            self.tableProjectUsers.setItem(aRow, 1, aSecurityItem)
            self.tableProjectUsers.setItem(aRow, 2, aDescriptionItem)

            self.tableTeamUsers.removeRow(r)

        self.tableTeamUsers.resizeColumnsToContents()
    # delUser

    def createTeam(self):
        aName = self.textName.text

        PipeCad.SetCurrentItem(self.tmwlItem)
        PipeCad.StartTransaction("Create Team")

        try:
            PipeCad.CreateItem("TEAM", "*" + aName)
        except NameError as e:
            # str(e)
            # repr(e)
            QMessageBox.critical(self, "", str(e))
            raise

        aTeamItem = PipeCad.CurrentItem()
        aTeamItem.Description = self.textDescription.text
        PipeCad.CreateItem("DBLI")

        # Add team to user team list.
        for r in range (self.tableTeamUsers.rowCount):
            aItem = self.tableTeamUsers.item(r, 0).data(Qt.UserRole)
            if aItem is not None:
                aTmliItems = aItem.Member
                if len(aTmliItems) > 0:
                    aTmliItem = aTmliItems[0]
                    aLteaItems = aTmliItem.Member
                    if len(aLteaItems) == 0:
                        PipeCad.SetCurrentItem(aTmliItem)
                    else:
                        PipeCad.SetCurrentItem(aLteaItems[-1])
                    # if

                    PipeCad.CreateItem("LTEA")
                    aLteaItem = PipeCad.CurrentItem()
                    aLteaItem.Temf = aTeamItem
                # if
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createTeam

    def modifyTeam(self):

        # Get Team Users.
        aUserSet = set()

        aUserTeams = PipeCad.CollectItem("LTEA", self.uswlItem)
        for aTeamItem in aUserTeams:
            if aTeamItem.Temf == self.teamItem:
                aUserItem = aTeamItem.Owner.Owner
                aUserSet.add(aUserItem)
            # if
        # for

        # Check Team Members.
        aMemberSet = set()

        for r in range (self.tableTeamUsers.rowCount):
            aUserItem = self.tableTeamUsers.item(r, 0).data(Qt.UserRole)
            if aUserItem is not None:
                aMemberSet.add(aUserItem)
            # if
        # for

        PipeCad.StartTransaction("Modify User")

        self.teamItem.Name = "*" + self.textName.text
        self.teamItem.Description = self.textDescription.text

        # Add new users to the team.
        aAddUsers = aMemberSet.difference(aUserSet)
        for aUserItem in aAddUsers:
            aTmliItems = aUserItem.Member
            if len(aTmliItems) > 0:
                aTmliItem = aTmliItems[0]
                aLteaItems = aTmliItem.Member
                if len(aLteaItems) == 0:
                    PipeCad.SetCurrentItem(aTmliItem)
                else:
                    PipeCad.SetCurrentItem(aLteaItems[-1])
                # if

                PipeCad.CreateItem("LTEA")
                aLteaItem = PipeCad.CurrentItem()
                aLteaItem.Temf = self.teamItem
            # if
        # for

        # Remove users from the team.
        aRemUsers = aUserSet.difference(aMemberSet)
        for aUserItem in aRemUsers:
            aLteaItems = PipeCad.CollectItem("LTEA", aUserItem)
            for aLteaItem in aLteaItems:
                if aLteaItem.Temf == self.teamItem:
                    PipeCad.SetCurrentItem(aLteaItem)
                    PipeCad.DeleteItem("LTEA")
                # if
            # for
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # modifyTeam

    def accept(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", self.tr("Please input team name!"))
            return
        # if

        if self.tmwlItem is None:
            return

        if self.teamItem is None:
            self.createTeam()
        else:
            self.modifyTeam()
        # if

        self.parent().refreshList()

        QDialog.accept(self)
    # accept
# TeamDialog

class UserDialog(QDialog):
    """docstring for UserDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        self.gridLayout = QGridLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()

        self.labelDescription = QLabel("Description")
        self.textDescription = QLineEdit()

        self.gridLayout.addWidget(self.labelName, 0, 0)
        self.gridLayout.addWidget(self.textName, 0, 1)
        self.gridLayout.addWidget(self.labelDescription, 0, 2)
        self.gridLayout.addWidget(self.textDescription, 0, 3)

        self.labelPassword = QLabel("Password")
        self.textPassword = QLineEdit()
        self.textPassword.setEchoMode(QLineEdit.Password)
        self.textPassword.setPlaceholderText("Enter Password")
        self.textPassword.textChanged.connect(self.confirmPassword)
        PipeCad.SetIndicator(self.textPassword)

        self.labelSecurity = QLabel("Security")
        self.comboSecurity = QComboBox()
        self.comboSecurity.addItem("General")
        self.comboSecurity.addItem("Free")

        self.labelConfirm = QLabel("Confirm")
        self.textConfirm = QLineEdit()
        self.textConfirm.setEchoMode(QLineEdit.Password)
        self.textConfirm.setPlaceholderText("Confirm Password")
        self.textConfirm.textChanged.connect(self.confirmPassword)
        PipeCad.SetIndicator(self.textConfirm)

        self.labelInfo = QLabel()

        self.gridLayout.addWidget(self.labelPassword, 1, 0)
        self.gridLayout.addWidget(self.textPassword, 1, 1)
        self.gridLayout.addWidget(self.labelConfirm, 1, 2)
        self.gridLayout.addWidget(self.textConfirm, 1, 3)

        self.gridLayout.addWidget(self.labelSecurity, 2, 0)
        self.gridLayout.addWidget(self.comboSecurity, 2, 1)
        self.gridLayout.addWidget(self.labelInfo, 2, 3)

        self.verticalLayout.addLayout(self.gridLayout)

        self.groupBox = QGroupBox("User Membership")
        self.horizontalLayout = QHBoxLayout(self.groupBox)

        self.layoutTable = QVBoxLayout()
        self.labelProjectTeams = QLabel("Project Teams")
        self.tableProjectTeams = QTableWidget()
        self.tableProjectTeams.setColumnCount(2)
        self.tableProjectTeams.setHorizontalHeaderLabels(["Name", "Description"])
        self.tableProjectTeams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectTeams.setAlternatingRowColors(True)
        self.tableProjectTeams.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectTeams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectTeams.setGridStyle(Qt.SolidLine)
        self.tableProjectTeams.horizontalHeader().setStretchLastSection(True)
        self.tableProjectTeams.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectTeams.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelProjectTeams)
        self.layoutTable.addWidget(self.tableProjectTeams)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.layoutButton = QVBoxLayout()
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.buttonAddTeam = QToolButton()
        self.buttonAddTeam.setArrowType(Qt.RightArrow)
        self.layoutButton.addWidget(self.buttonAddTeam)

        self.buttonDelTeam = QToolButton()
        self.buttonDelTeam.setArrowType(Qt.LeftArrow)
        self.layoutButton.addWidget(self.buttonDelTeam)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutButton.addItem(self.verticalSpacer)

        self.buttonAddTeam.clicked.connect(self.addTeam)
        self.buttonDelTeam.clicked.connect(self.delTeam)

        self.horizontalLayout.addLayout(self.layoutButton)
        
        self.layoutTable = QVBoxLayout()
        self.labelUserTeams = QLabel("Team Membership")
        self.tableUserTeams = QTableWidget()
        self.tableUserTeams.setColumnCount(2)
        self.tableUserTeams.setHorizontalHeaderLabels(["Name", "Description"])
        self.tableUserTeams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableUserTeams.setAlternatingRowColors(True)
        self.tableUserTeams.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableUserTeams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableUserTeams.setGridStyle(Qt.SolidLine)
        self.tableUserTeams.horizontalHeader().setStretchLastSection(True)
        self.tableUserTeams.verticalHeader().setMinimumSectionSize(16)
        self.tableUserTeams.verticalHeader().setDefaultSectionSize(18)

        self.layoutTable.addWidget(self.labelUserTeams)
        self.layoutTable.addWidget(self.tableUserTeams)

        self.horizontalLayout.addLayout(self.layoutTable)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.uswlItem = PipeCad.GetItem("/*U")
        self.tmwlItem = PipeCad.GetItem("/*T")
        self.userItem = None

    # setupUi

    def init(self, theUserItem = None):
        if theUserItem is not None:
            if theUserItem.Type == "USER":
                self.userItem = theUserItem
                self.textName.setText(theUserItem.Name)
                self.comboSecurity.setCurrentText(theUserItem.Security)
                self.textDescription.setText(theUserItem.Description)
                self.textPassword.setText(theUserItem.Password)
                self.textConfirm.setText(theUserItem.Password)
            # if
        # if

        # Project Teams.
        if self.tmwlItem == None:
            return
        # if

        aTeamSet = set()

        if theUserItem is not None:
            aLteaItems = PipeCad.CollectItem("LTEA", theUserItem)
            self.tableUserTeams.setRowCount(len(aLteaItems))

            for r in range (self.tableUserTeams.rowCount):
                aTeamItem = aLteaItems[r].Temf
                if aTeamItem is None:
                    continue
                # if

                aTeamSet.add(aTeamItem)

                aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
                aItem.setData(Qt.UserRole, aTeamItem)

                self.tableUserTeams.setItem(r, 0, aItem)
                self.tableUserTeams.setItem(r, 1, QTableWidgetItem(aTeamItem.Description))
            # for

            self.tableUserTeams.resizeColumnsToContents()
        # if

        aTeamItems = self.tmwlItem.Member
        self.tableProjectTeams.setRowCount(0)

        for r in range(len(aTeamItems)):
            aTeamItem = aTeamItems[r]
            if not(aTeamItem in aTeamSet):
                aRow = self.tableProjectTeams.rowCount
                self.tableProjectTeams.insertRow(aRow)

                aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
                aItem.setData(Qt.UserRole, aTeamItem)

                self.tableProjectTeams.setItem(aRow, 0, aItem)
                self.tableProjectTeams.setItem(aRow, 1, QTableWidgetItem(aTeamItem.Description))
            # if
        # for

        self.tableProjectTeams.resizeColumnsToContents()

    # init

    def create(self):
        self.setWindowTitle(self.tr("Create User"))
        self.init()
        self.show()
    # createTeam

    def modify(self):
        self.setWindowTitle(self.tr("Modify User"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modifyTeam

    def confirmPassword(self):
        if len(self.textPassword.text) > 0 or len(self.textConfirm.text) > 0:
            if self.textPassword.text == self.textConfirm.text:
                self.labelInfo.setText("<font color=Green>Matched</font>")
            else:
                self.labelInfo.setText("<font color=Red>Not match</font>")
        else:
            self.labelInfo.setText("")
    # confirmPassword

    def addTeam(self):
        aRows = []
        for aItem in self.tableProjectTeams.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableProjectTeams.item(r, 0).clone()
            aDescriptionItem = self.tableProjectTeams.item(r, 1).clone()

            aRow = self.tableUserTeams.rowCount
            self.tableUserTeams.insertRow(aRow)
            self.tableUserTeams.setItem(aRow, 0, aNameItem)
            self.tableUserTeams.setItem(aRow, 1, aDescriptionItem)

            self.tableProjectTeams.removeRow(r)

        self.tableUserTeams.resizeColumnsToContents()
    # addTeam

    def delTeam(self):
        aRows = []
        for aItem in self.tableUserTeams.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableUserTeams.item(r, 0).clone()
            aDescriptionItem = self.tableUserTeams.item(r, 1).clone()

            aRow = self.tableProjectTeams.rowCount
            self.tableProjectTeams.insertRow(aRow)
            self.tableProjectTeams.setItem(aRow, 0, aNameItem)
            self.tableProjectTeams.setItem(aRow, 1, aDescriptionItem)

            self.tableUserTeams.removeRow(r)

        self.tableProjectTeams.resizeColumnsToContents()
    # delTeam

    def createUser(self):
        aName = self.textName.text
        aPassword = self.textPassword.text

        PipeCad.SetCurrentItem(self.uswlItem)
        PipeCad.StartTransaction("Create User")

        try:
            PipeCad.CreateItem("USER", aName)
        except NameError as e:
            QMessageBox.critical(self, "", str(e))
            raise

        aUserItem = PipeCad.CurrentItem()
        aUserItem.Security = self.comboSecurity.currentText
        aUserItem.Password = self.textPassword.text
        aUserItem.Description = self.textDescription.text

        PipeCad.CreateItem("TMLI")
        aTmliItem = PipeCad.CurrentItem()

        for r in range (self.tableUserTeams.rowCount):
            aItem = self.tableUserTeams.item(r, 0).data(Qt.UserRole)

            PipeCad.CreateItem("LTEA")
            aLteaItem = PipeCad.CurrentItem()
            aLteaItem.Temf = aItem

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createUser

    def modifyUser(self):
        # Get user team list.
        aTeamSet = set()
        aLteaItems = PipeCad.CollectItem("LTEA", self.userItem)
        for aLteaItem in aLteaItems:
            if aLteaItem.Temf is not None:
                aTeamSet.add(aLteaItem.Temf)
            # if
        # for

        # Get team member list.
        aMemberSet = set()

        for r in range (self.tableUserTeams.rowCount):
            aTeamItem = self.tableUserTeams.item(r, 0).data(Qt.UserRole)
            aMemberSet.add(aTeamItem)
        # for

        PipeCad.StartTransaction("Modify User")
        self.userItem.Name = self.textName.text
        self.userItem.Description = self.textDescription.text
        self.userItem.Security = self.comboSecurity.currentText
        if self.userItem.Password != self.textPassword.text:
            self.userItem.Password = self.textPassword.text
        # if

        # Set current item to add new team.
        aTmliItem = self.userItem.Member[0]
        if len(aTmliItem.Member) > 0:
            PipeCad.SetCurrentItem(aTmliItem.Member[-1])
        else:
            PipeCad.SetCurrentItem(aTmliItem)
        # if

        # Add new team to the user.
        aAddTeams = aMemberSet.difference(aTeamSet)
        for aTeamItem in aAddTeams:
            PipeCad.CreateItem("LTEA")
            aLteaItem = PipeCad.CurrentItem()
            aLteaItem.Temf = aTeamItem
        # for

        # Remove teams from the user.
        aRemTeams = aTeamSet.difference(aMemberSet)
        for aLteaItem in aLteaItems:
            if aLteaItem.Temf in aRemTeams:
                PipeCad.SetCurrentItem(aLteaItem)
                PipeCad.DeleteItem("LTEA")
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # modifyUser

    def accept(self):
        aName = self.textName.text
        aPassword = self.textPassword.text
        if len(aName) < 1 or len(aPassword) < 1:
            QMessageBox.warning(self, "", self.tr("Please input user name and password!"))
            return
        # if

        if self.textPassword.text != self.textConfirm.text:
            QMessageBox.warning(self, "", self.tr("The passwords do not match!"))
            return
        # if

        if self.uswlItem is None:
            return

        if self.userItem is None:
            self.createUser()
        else:
            self.modifyUser()
        # if

        self.parent().refreshList()

        QDialog.accept(self)

    # accept


class DatabaseDialog(QDialog):
    """docstring for DatabaseDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(420, 580)
        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()
        self.labelDatabase = QLabel("Database")
        self.horizontalLayout.addWidget(self.labelDatabase)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox("Project Teams")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.tableProjectTeams = QTableWidget()
        self.tableProjectTeams.setColumnCount(2)
        self.tableProjectTeams.setHorizontalHeaderLabels(["Name", "Description"])
        self.tableProjectTeams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectTeams.setAlternatingRowColors(True)
        self.tableProjectTeams.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectTeams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectTeams.setGridStyle(Qt.SolidLine)
        self.tableProjectTeams.horizontalHeader().setStretchLastSection(True)
        self.tableProjectTeams.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectTeams.verticalHeader().setDefaultSectionSize(18)
        self.tableProjectTeams.currentItemChanged.connect(self.teamChanged)
        self.horizontalLayout.addWidget(self.tableProjectTeams)
        self.verticalLayout.addWidget(self.groupBox)

        self.gridLayout = QGridLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.textName.textChanged.connect(self.teamChanged)
        self.gridLayout.addWidget(self.labelName, 0, 0)
        self.gridLayout.addWidget(self.textName, 0, 1)

        self.labelDescription = QLabel("Description")
        self.textDescription = QLineEdit()
        self.gridLayout.addWidget(self.labelDescription, 1, 0)
        self.gridLayout.addWidget(self.textDescription, 1, 1)

        self.labelType = QLabel("Database Type")
        self.comboType = QComboBox()
        self.comboType.addItems(["Design", "Catalogue"])
        self.comboType.currentTextChanged.connect(self.dbTypeChanged)
        self.gridLayout.addWidget(self.labelType, 2, 0)
        self.gridLayout.addWidget(self.comboType, 2, 1)

        self.labelCreate = QLabel("Create SITE")
        self.textCreate = QLineEdit()
        self.gridLayout.addWidget(self.labelCreate, 3, 0)
        self.gridLayout.addWidget(self.textCreate, 3, 1)

        # self.labelArea = QLabel("Area Number")
        # self.textArea = QLineEdit()
        # self.textArea.setPlaceholderText("Set by System")
        # self.buttonArea = QPushButton("System")
        # self.buttonArea.clicked.connect(self.setAreaNumber)
        # self.gridLayout.addWidget(self.labelArea, 4, 0)
        # self.gridLayout.addWidget(self.textArea, 4, 1)
        # self.gridLayout.addWidget(self.buttonArea, 4, 2)

        self.labelNumber = QLabel("DB Number")
        self.textNumber = QLineEdit()
        self.textNumber.setPlaceholderText("Set by System")
        self.buttonNumber = QPushButton("System")
        self.buttonNumber.clicked.connect(self.setDbNumber)
        self.gridLayout.addWidget(self.labelNumber, 5, 0)
        self.gridLayout.addWidget(self.textNumber, 5, 1)
        self.gridLayout.addWidget(self.buttonNumber, 5, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tmwlItem = PipeCad.GetItem("/*T")
        self.dbItem = None

    # setupUi

    def init(self, theDbItem = None):
        if theDbItem is not None:
            self.dbItem = theDbItem
            self.textName.setText(theDbItem.Name[theDbItem.Name.index("/")+1:])
            self.textDescription.setText(theDbItem.Description)
            #self.textArea.setText(str(theDbItem.Area))
            self.textNumber.setText(str(theDbItem.DbNumber))
            aIndex = self.comboType.findText(theDbItem.DbType, Qt.MatchStartsWith)
            self.comboType.setCurrentIndex(aIndex)

            self.textNumber.setEnabled(False)
            self.buttonNumber.setEnabled(False)
            self.comboType.setEnabled(False)
            self.textCreate.setEnabled(False)
        else:
            self.textName.setText("")
            self.textDescription.setText("")
            self.textNumber.setText("")

            self.textNumber.setEnabled(True)
            self.buttonNumber.setEnabled(True)
            self.comboType.setEnabled(True)
            self.textCreate.setEnabled(True)
        # if

        if self.tmwlItem is None:
            return
        # if

        aTeamItems = self.tmwlItem.Member
        self.tableProjectTeams.setRowCount(len(aTeamItems))

        for r in range (self.tableProjectTeams.rowCount):
            aTeamItem = aTeamItems[r]
            aItem = QTableWidgetItem("<TEAM> " + aTeamItem.Name[1:])
            aItem.setData(Qt.UserRole, aTeamItem)

            self.tableProjectTeams.setItem(r, 0, aItem)
            self.tableProjectTeams.setItem(r, 1, QTableWidgetItem(aTeamItem.Description))
        # for

        self.tableProjectTeams.resizeColumnsToContents()

    # init

    def create(self):
        self.setWindowTitle(self.tr("Create Database"))
        self.init()
        self.show()
    # create

    def modify(self):
        self.setWindowTitle(self.tr("Modify Database"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modify

    def teamChanged(self):
        aRow = self.tableProjectTeams.currentRow()
        aItem = self.tableProjectTeams.item(aRow, 0)
        aName = self.textName.text
        if aItem is not None:
            self.labelDatabase.setText("Database: <font color=Brown>" + aItem.text()[6:] + "/" + aName + " </font>")
    # teamChanged

    def dbTypeChanged(self, theType):
        if theType == "Catalogue":
            self.labelCreate.setText("Create CATA")
        else:
            self.labelCreate.setText("Create SITE")
    # dbTypeChanged

    def setAreaNumber(self):
        QMessageBox.warning(self, "", "set area number")
    # setAreaNumber

    def setDbNumber(self):
        aNumber = self.tmwlItem.NextDbNumber
        self.textNumber.setText(str(aNumber))
    # setDatabaseNumber

    def createDb(self, theName):
        #aArea = 0
        aNumber = 0
        #if len(self.textArea.text) > 0:
        #    aArea = int(self.textArea.text)

        if len(self.textNumber.text) > 0:
            aNumber = int(self.textNumber.text)

            # Check the input database number range.
            if aNumber > 8000 or aNumber < 1:
                QMessageBox.critical(self, "", "Database Number range is [1~8000]!")
                raise ValueError ("Database Number range is [1~8000]!")

            # Check the input database number used.
            aDatabases = PipeCad.CollectItem("DB", self.tmwlItem)
            for aDatabase in aDatabases:
                if aDatabase.DbNumber == aNumber:
                    aMessage = "Database Number " + str(aNumber) + " is used!"
                    QMessageBox.critical(self, "", aMessage)
                    raise ValueError (aMessage)
                # if
            # for
        else:
            aNumber = self.tmwlItem.NextDbNumber()
        # if

        PipeCad.StartTransaction("Create Database")
        PipeCad.CreateItem("DB", theName)
        aDbItem = PipeCad.CurrentItem()
        aDbItem.Description = self.textDescription.text
        aDbItem.DbType = self.comboType.currentText[0:4].upper()
        #aDbItem.Area = aArea
        aDbItem.DbNumber = aNumber
        aDbItem.CreateDatabase(self.textCreate.text)
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createDb

    def modifyDb(self):
        PipeCad.StartTransaction("Modify Database")
        self.dbItem.Name = self.textName.text
        self.dbItem.Description = self.textDescription.text
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()

        QDialog.accept(self)
    # modifyDb

    def accept(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", "Please input database name!")
            return
        # if

        aRow = self.tableProjectTeams.currentRow()
        aTeamItem = self.tableProjectTeams.item(aRow, 0).data(Qt.UserRole)
        if aTeamItem is None:
            return
        # if

        aDbliItem = aTeamItem.Member[0]
        if aDbliItem is None:
            return
        # if

        aDbItems = aDbliItem.Member
        if len(aDbItems) > 0:
            PipeCad.SetCurrentItem(aDbItems[-1])
        else:
            PipeCad.SetCurrentItem(aDbliItem)

        # Check the input database name.
        aDbName = aTeamItem.Name + "/" + aName
        if self.dbItem is not None:
            PipeCad.StartTransaction("Modify Database")
            self.dbItem.Name = aDbName
            self.dbItem.Description = self.textDescription.text
            PipeCad.CommitTransaction()
            PipeCad.SaveWork()

            self.parent().refreshList()

            QDialog.accept(self)

            return
        # if

        aDatabases = PipeCad.CollectItem("DB", self.tmwlItem)
        for aDatabase in aDatabases:
            if aDatabase.Name == aDbName:
                aMessage = "Database Name " + aDbName + " already exists!"
                QMessageBox.critical(self, "", aMessage)
                raise NameError (aMessage)
            # if
        # for

        self.createDb(aDbName)

        self.parent().refreshList()

        QDialog.accept(self)

    # accept


class MdbDialog(QDialog):
    """docstring for MdbDailog"""
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(580, 600)
        self.verticalLayout = QVBoxLayout(self)

        self.formLayout = QFormLayout()

        self.labelName = QLabel("Name")
        self.textName = QLineEdit()
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel("Description")
        self.textDescription = QLineEdit()
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textDescription)

        self.verticalLayout.addLayout(self.formLayout)

        self.groupBoxProject = QGroupBox("Project Databases")
        self.horizontalLayout = QHBoxLayout(self.groupBoxProject)

        self.tableProjectDatabases = QTableWidget()
        self.tableProjectDatabases.setColumnCount(4)
        self.tableProjectDatabases.setHorizontalHeaderLabels(["Name", "Type", "DB Number", "Description"])
        self.tableProjectDatabases.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableProjectDatabases.setAlternatingRowColors(True)
        self.tableProjectDatabases.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableProjectDatabases.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableProjectDatabases.setGridStyle(Qt.SolidLine)
        self.tableProjectDatabases.horizontalHeader().setStretchLastSection(True)
        self.tableProjectDatabases.verticalHeader().setMinimumSectionSize(16)
        self.tableProjectDatabases.verticalHeader().setDefaultSectionSize(18)

        self.horizontalLayout.addWidget(self.tableProjectDatabases)

        self.verticalLayout.addWidget(self.groupBoxProject)

        self.layoutButton = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layoutButton.addItem(self.horizontalSpacer)

        self.buttonAddDatabase = QToolButton()
        self.buttonAddDatabase.setArrowType(Qt.DownArrow)
        self.buttonAddDatabase.clicked.connect(self.addDatabase)
        self.layoutButton.addWidget(self.buttonAddDatabase)

        self.buttonDelDatabase = QToolButton()
        self.buttonDelDatabase.setArrowType(Qt.UpArrow)
        self.buttonDelDatabase.clicked.connect(self.delDatabase)
        self.layoutButton.addWidget(self.buttonDelDatabase)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layoutButton.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.layoutButton)
        
        self.groupBoxCurrent = QGroupBox("Current Databases")
        self.horizontalLayout = QHBoxLayout(self.groupBoxCurrent)

        self.tableCurrentDatabases = QTableWidget()
        self.tableCurrentDatabases.setColumnCount(4)
        self.tableCurrentDatabases.setHorizontalHeaderLabels(["Name", "Type", "DB Number", "Description"])
        self.tableCurrentDatabases.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableCurrentDatabases.setAlternatingRowColors(True)
        self.tableCurrentDatabases.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableCurrentDatabases.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableCurrentDatabases.setGridStyle(Qt.SolidLine)
        self.tableCurrentDatabases.horizontalHeader().setStretchLastSection(True)
        self.tableCurrentDatabases.verticalHeader().setMinimumSectionSize(16)
        self.tableCurrentDatabases.verticalHeader().setDefaultSectionSize(18)

        self.horizontalLayout.addWidget(self.tableCurrentDatabases)

        self.verticalLayout.addWidget(self.groupBoxCurrent)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tmwlItem = PipeCad.GetItem("/*T")
        self.mdbwItem = PipeCad.GetItem("/*M")
        self.mdbItem = None

    # setupUi

    def init(self, theMdbItem = None):
        aDbNumers = []
        self.tableCurrentDatabases.setRowCount(0)
        self.tableProjectDatabases.setRowCount(0)
        
        if theMdbItem is not None:
            self.mdbItem = theMdbItem
            self.textName.setText(theMdbItem.Name)
            self.textDescription.setText(theMdbItem.Description)

            # Current MDB databases.
            aDbItems = theMdbItem.Member
            self.tableCurrentDatabases.setRowCount(len(aDbItems))
            for r in range (self.tableCurrentDatabases.rowCount):
                aDbItem = aDbItems[r].Dbref
                aItem = QTableWidgetItem("<DB> " + aDbItem.Name[1:])
                aItem.setData(Qt.UserRole, aDbItem)

                self.tableCurrentDatabases.setItem(r, 0, aItem)
                self.tableCurrentDatabases.setItem(r, 1, QTableWidgetItem(aDbItem.DbType))
                self.tableCurrentDatabases.setItem(r, 2, QTableWidgetItem(str(aDbItem.DbNumber)))
                self.tableCurrentDatabases.setItem(r, 3, QTableWidgetItem(aDbItem.Description))

                aDbNumers.append(aDbItem.DbNumber)
            # for

            self.tableCurrentDatabases.resizeColumnsToContents()
        # if

        if self.tmwlItem is None:
            return
        # if

        aDbItems = []
        aDatabases = PipeCad.CollectItem("DB")
        for aDatabase in aDatabases:
            if aDbNumers.count(aDatabase.DbNumber) < 1:
                aDbItems.append(aDatabase)

        self.tableProjectDatabases.setRowCount(len(aDbItems))

        for r in range (self.tableProjectDatabases.rowCount):
            aDbItem = aDbItems[r]
            aItem = QTableWidgetItem("<DB> " + aDbItem.Name[1:])
            aItem.setData(Qt.UserRole, aDbItem)

            self.tableProjectDatabases.setItem(r, 0, aItem)
            self.tableProjectDatabases.setItem(r, 1, QTableWidgetItem(aDbItem.DbType))
            self.tableProjectDatabases.setItem(r, 2, QTableWidgetItem(str(aDbItem.DbNumber)))
            self.tableProjectDatabases.setItem(r, 3, QTableWidgetItem(aDbItem.Description))

        self.tableProjectDatabases.resizeColumnsToContents()
    # init

    def create(self):
        self.setWindowTitle(self.tr("Create Multiple Database"))
        self.init()
        self.show()
    # create

    def modify(self):
        self.setWindowTitle(self.tr("Modify Multiple Database"))
        self.init(PipeCad.CurrentItem())
        self.show()
    # modify

    def addDatabase(self):
        aRows = []
        for aItem in self.tableProjectDatabases.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableProjectDatabases.item(r, 0).clone()
            aTypeItem = self.tableProjectDatabases.item(r, 1).clone()
            aNumbItem = self.tableProjectDatabases.item(r, 2).clone()
            aDescItem = self.tableProjectDatabases.item(r, 3).clone()

            aRow = self.tableCurrentDatabases.rowCount
            self.tableCurrentDatabases.insertRow(aRow)
            self.tableCurrentDatabases.setItem(aRow, 0, aNameItem)
            self.tableCurrentDatabases.setItem(aRow, 1, aTypeItem)
            self.tableCurrentDatabases.setItem(aRow, 2, aNumbItem)
            self.tableCurrentDatabases.setItem(aRow, 3, aDescItem)

            self.tableProjectDatabases.removeRow(r)

        self.tableCurrentDatabases.resizeColumnsToContents()
    # addDatabase

    def delDatabase(self):
        aRows = []
        for aItem in self.tableCurrentDatabases.selectedItems():
            aRows.append(aItem.row())

        aRows = list(set(aRows))
        if len(aRows) < 1:
            return

        aRows.sort(reverse=True)
        for r in aRows:
            aNameItem = self.tableCurrentDatabases.item(r, 0).clone()
            aTypeItem = self.tableCurrentDatabases.item(r, 1).clone()
            aNumbItem = self.tableCurrentDatabases.item(r, 2).clone()
            aDescItem = self.tableCurrentDatabases.item(r, 3).clone()

            aRow = self.tableProjectDatabases.rowCount
            self.tableProjectDatabases.insertRow(aRow)
            self.tableProjectDatabases.setItem(aRow, 0, aNameItem)
            self.tableProjectDatabases.setItem(aRow, 1, aTypeItem)
            self.tableProjectDatabases.setItem(aRow, 2, aNumbItem)
            self.tableProjectDatabases.setItem(aRow, 3, aDescItem)

            self.tableCurrentDatabases.removeRow(r)

        self.tableProjectDatabases.resizeColumnsToContents()
    # delDatabase

    def createMdb(self):
        aName = self.textName.text
        
        PipeCad.SetCurrentItem(self.mdbwItem)
        PipeCad.StartTransaction("Create MDB")
        PipeCad.CreateItem("MDB", aName)
        aMdbItem = PipeCad.CurrentItem()
        aMdbItem.Description = self.textDescription.text
        
        for r in range (self.tableCurrentDatabases.rowCount):
            aDbItem = self.tableCurrentDatabases.item(r, 0).data(Qt.UserRole)

            PipeCad.CreateItem("DBL")
            aDblItem = PipeCad.CurrentItem()
            if aDbItem is not None:
                aDblItem.Dbref = aDbItem
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # createMdb

    def modifyMdb(self):
        # Get databse set.
        aDatabaseSet = set()
        for aDblItem in self.mdbItem.Member:
            aDatabaseSet.add(aDblItem.Dbref)
        # for

        # Get current databse set.
        aCurrentSet = set()
        for r in range (self.tableCurrentDatabases.rowCount):
            aDbItem = self.tableCurrentDatabases.item(r, 0).data(Qt.UserRole)
            aCurrentSet.add(aDbItem)
        # for

        PipeCad.StartTransaction("Modify MDB")
        self.mdbItem.Name = self.textName.text
        self.mdbItem.Description = self.textDescription.text

        if len(self.mdbItem.Member) > 0:
            PipeCad.SetCurrentItem(self.mdbItem.Member[-1])
        else:
            PipeCad.SetCurrentItem(self.mdbItem)
        # if

        # Add new database to the MDB.
        aAddDbs = aCurrentSet.difference(aDatabaseSet)
        for aDbItem in aAddDbs:
            PipeCad.CreateItem("DBL")
            aDblItem = PipeCad.CurrentItem()
            if aDbItem is not None:
                aDblItem.Dbref = aDbItem
            # if
        # for

        # Remove database from the MDB.
        aRemDbs = aDatabaseSet.difference(aCurrentSet)
        for aDblItem in self.mdbItem.Member:
            if aDblItem.Dbref in aRemDbs:
                PipeCad.SetCurrentItem(aDblItem)
                PipeCad.DeleteItem("DBL")
            # if
        # for

        PipeCad.CommitTransaction()
        PipeCad.SaveWork()
    # modifyMdb

    def accept(self):
        aName = self.textName.text
        if len(aName) < 1:
            QMessageBox.warning(self, "", "Please input MDB name!")
            return
        # if

        if self.mdbwItem is None:
            return

        if self.mdbItem is None:
            self.createMdb()
        else:
            self.modifyMdb()
        # if

        self.parent().refreshList()

        QDialog.accept(self)

    # accept

def Show():
    aMain = AdminMain()
    aMain.elementChanged("Teams")
    PipeCad.setCentralWidget(aMain)
# Show

class ProjectDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.statItem = PipeCad.GetItem("/*S")
        
        self.setupUi()
    # __init__

    def setupUi(self):
        self.setMinimumWidth(380)
        self.setWindowTitle(self.tr("Project Information"))

        aStatItem = self.statItem

        self.verticalLayout = QVBoxLayout(self)
        self.groupBox = QGroupBox("Project")
        self.formLayout = QFormLayout(self.groupBox)

        self.labelProject = QLabel("Project")
        self.textProject = QLineEdit(aStatItem.ProjectNumber)
        self.textProject.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelProject)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textProject)

        self.labelCode = QLabel("Code")
        self.textCode = QLineEdit(PipeCad.CurrentProject.Code)
        self.textCode.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelCode)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textCode)

        self.labelNumber = QLabel("Number")
        self.textNumber = QLineEdit(aStatItem.ProjectNumber)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelNumber)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textNumber)

        self.labelName = QLabel("Name")
        self.textName = QLineEdit(aStatItem.ProjectName)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelName)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textName)

        self.labelDescription = QLabel("Description")
        self.textDescription = QLineEdit(aStatItem.ProjectDescription)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelDescription)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textDescription)

        self.labelMessage = QLabel("Message")
        self.textMessage = QLineEdit(aStatItem.ProjectMessage)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.labelMessage)
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.textMessage)

        self.verticalLayout.addWidget(self.groupBox)

        # Action buttons.
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    # setupUi

    def accept(self):
        if self.statItem is None:
            return
        # if

        PipeCad.StartTransaction("Modify Project Info")
        self.statItem.ProjectNumber = self.textNumber.text
        self.statItem.ProjectName = self.textName.text
        self.statItem.ProjectDescription = self.textDescription.text
        self.statItem.ProjectMessage = self.textMessage.text
        PipeCad.CommitTransaction()
        PipeCad.SaveWork()

        QDialog.accept(self)
    # accept

# ProjectDialog

def ShowProject():
    aProjectDlg = ProjectDialog(PipeCad)
    aProjectDlg.exec()
# ShowProject


class UserProcessDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi()
    # __init__

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle("Expunge User Process")

        self.verticalLayout = QVBoxLayout(self)
        self.groupBox = QGroupBox("Project Users")

        self.verticalLayoutBox = QHBoxLayout(self.groupBox)
        self.tableUser = QTableWidget()
        self.tableUser.setColumnCount(5)
        self.tableUser.setHorizontalHeaderLabels(["Date", "PC Name", "Host Name", "PipeCAD User", "Module"])
        self.tableUser.horizontalHeader().setDefaultSectionSize(80)
        self.tableUser.verticalHeader().setDefaultSectionSize(18)
        self.tableUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableUser.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableUser.horizontalHeader().setStretchLastSection(True)
        self.tableUser.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.verticalLayoutBox.addWidget(self.tableUser)

        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.verticalLayout.addWidget(self.buttonBox)

    # setupUi

    def setSession(self):
        PipeCad.CurrentProject.updateSession()

        aSessionList = PipeCad.CurrentProject.Sessions

        self.tableUser.setRowCount(len(aSessionList))

        for i in range(self.tableUser.rowCount):
            aSession = aSessionList[i]

            aCurrent = aSession.Entered
            if aSession == PipeCad.CurrentSession:
                aCurrent = "*" + aSession.Entered
            # if

            aUserName = ""
            if aSession.User is not None:
                aUserName = aSession.User.Name
            # if

            aSessionItem = QTableWidgetItem(aCurrent)
            aSessionItem.setData(Qt.UserRole, aSession)

            self.tableUser.setItem(i, 0, aSessionItem)
            self.tableUser.setItem(i, 1, QTableWidgetItem(aSession.Login))
            self.tableUser.setItem(i, 2, QTableWidgetItem(aSession.Host))
            self.tableUser.setItem(i, 3, QTableWidgetItem(aUserName))
            self.tableUser.setItem(i, 4, QTableWidgetItem(aSession.Module))
        # for

    # setSession

    def accept(self):
        aRow = self.tableUser.currentRow()
        aSessionItem = self.tableUser.item(aRow, 0)
        if aSessionItem is None:
            return
        # if

        aSession = aSessionItem.data(Qt.UserRole)
        if aSession is None:
            return
        # if

        PipeCad.CurrentProject.expungeSession(aSession)

        self.setSession()
    # accept

# UserProcessDialog

# Singleton Instance.
aUserProcessDlg = UserProcessDialog(PipeCad)

def ExpungeUser():
    aUserProcessDlg.setSession()
    aUserProcessDlg.show()
# ExpungeUser

def ExpungeData():
    QMessageBox.warning(PipeCad, "", "Not implement yet!")
# ExpungeData
