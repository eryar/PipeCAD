# PipeCAD Customization Guide {#pipecad_customization_guide}

# Introduction
This manual describes how to use Python to customize PipeCAD.

You do not have to be a professional programmer to start to learn Python, although you may find this manual difficult to follow unless you have some understanding of programming concepts such as if statements and do loops. If you have no programming experience, you should consider attending a Python Training Course.

## Customizing a Graphical User Interface

PipeCAD make use of a Graphical User Interface (GUI) to drive the software. The interfaces provided with your PipeCAD software are designed to apply to a wide range of situations and business needs. However, as you become more experienced with PipeCAD you may wish to design an interface that is more closely related to your requirements.
Qt has been specifically introduced for writing and customising the Forms and Menus for PipeCAD. 
Before you begin customising a GUI, you must have a good working knowledge of PipeCAD and Qt.

### Simple Widget
You define a widget using following python code, input the code to the Python Console:

```python
from PythonQt.QtCore import *
from PythonQt.QtGui import *

aButton = QPushButton("Hello World")
aButton.clicked.connect(lambda x: print("Hello World"))
aButton.show()
```
The example code defines a small button labelled "Hello World", and connec the button clicked to a lambda function to show "Hello World" in the console.

## Serious Warning About Software Customization

The ability to customise individual Applications to suit your own specific needs gives you great flexibility in the ways in which you use your system.
But it also introduces the risk that your modified macros may not be compatible with future versions of the software, since they are no longer under PipeCAD’s control.
Your own Applications may diverge from future standard versions and may not take advantage of product enhancements incorporated into the standard product.
To minimise this risk, it is most important that your in-house customisation policies constrain any changes which you make to the Applications so that they retain maximum compatibility with the standard product at all times.
Remember that PipeCAD can give you full technical support only for products over which it has control. We cannot guarantee to solve problems caused by software which you have written yourself.

# Object Type Details
In order to distinguish from Qt, all property and methods name of PipeCAD start with a capital letter.

## Position
Position point in 3D space.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| X | double | The X component |
| Y | double | The Y component |
| Z | double | The Z component |
| Origin | TreeItem | The TreeItem that is the origin |

**Methods**

| Name | Result | Purpose |
| :--- | :--- | :--- |
| Offset(Direction theDir, double theOffset) | Position | Returns a position offset by the supplied length in the supplied direction. |
| Distance(Position thePosition) | Position | Returns the distance between two positions. |

## Direction
Describes a unit vector in 3D space. This unit vector is also called "Direction".

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| X | double | The X component |
| Y | double | The Y component |
| Z | double | The Z component |
| Origin | TreeItem | The TreeItem that is the origin |

**Methods**

| Name | Result | Purpose |
| :--- | :--- | :--- |
| Reversed() | Direction | Reversed the direction and return the opposite direction. |
| IsParallel(Direction theDir, double theTolerance) | bool | Returns True if the supplied direction is parallel according to tolerance supplied, false otherwise. |

## Orientation
This defines the orientation of a frame of reference (i.e. the directions of the XYZ axes) in the frame of reference of that defined by an origin database reference. It does not define a position.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Alpha | double | The Alpha component |
| Beta | double | The Beta component |
| Gamma | double | The Gamma component |
| XDirection | Direction | Return X axis direction of the ORIENTATION as a DIRECTION. |
| YDirection | Direction | Return Y axis direction of the ORIENTATION as a DIRECTION. |
| ZDirection | Direction | Return Z axis direction of the ORIENTATION as a DIRECTION. |
| Origin | TreeItem | The TreeItem that is the origin |

## LinkPoint
LinkPoint is P-Point for piping component and equipment primitives.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Key | string | P-Point key, such as P1 |
| Bore | string | P-Point bore |
| Type | string | P-Point connection type |
| Position | Position | P-Point position |
| Direction | Direction | P-Point direction |

## TreeItem

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| RefNo | string | Reference number |
| Type | string | Item type |
| Name | string | Item name |
| Owner | TreeItem | Parent item |
| Member | list | Member list |

## Project
Project data.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Name | string | Project name |
| Evar | string | Project environment variable, e.g. SAM000 |
| Path | string | Project directory path |
| Code | string | Project code, 3 characters, e.g. SAM |
| Number | string | Project number |
| Message | string | Project message, information about the project |
| Description | string | Project description |
| CurrentSession | Session | Project current session |
| MdbList | list | Project MDB list |
| UserList | list | Project User list |
| Sessions | list | Return list of all sessions of the project |

## Session
When a user login a project will create a session.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Id | int | Session ID |
| Name | string | Session name |
| Login | string | User's login ID |
| Host | string | ID of the Machine running the session |
| Entered | string | Time of entering the session |
| Module | string | User's login module |
| MDB | MDB | The current MDB of the SESSION |
| User | User | The user of this SESSION object |

## MDB
The Multiple Databases(MDB) can contain database.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Name | string | MDB name |
| Description | string | MDB description |
| RefNo | string | String containing Database reference number |

## User
User can login project.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Name | string | User name |
| Description | string | User description |
| Access | string | User access rights(FREE, GENERAL) |
| RefNo | string | STRING containing Database reference number |
| Password | string | User password |

## SnapOption
The object snap option:

| Option | Description |
| :--- | :--- |
| SnapEnd | Snap object end point. |
| SnapMiddle | Snap object middle point. |
| SnapCenter | Snap circle center point. |
| SnapPpoint | Snap object P-Point. |


# PipeCad API
PipeCad is a core object of PipeCAD, the PipeCad object is a mechanism for providing methods which are not specific to the standard objects, such as TreeItem, QWidget etc.

**Property**

| Name | Type | Purpose |
| :--- | :--- | :--- |
| Projects | list | The project list by environment variables |
| CurrentProject | Project | The login project |
| CurrentSession | Session | The current session |

## PipeCad.Projects
The project list by environment variables.

```python
aProjectsList = PipeCad.Projects
```

## PipeCad.CurrentProject
The login project.

```python
aCurrentProject = PipeCad.CurrentProject
```

## PipeCad.CurrentSession
The current session.

```python
aCurrentSession = PipeCad.CurrentSession
```

**Methods**

| Name  | Purpose |
| :---  | :--- |
| About | Show about dialog|
| AddAidArrow | Add aid arrow to 3d viewer |
| AddAidAxis | Add aid axis to 3d viewer |
| AddAidCylinder | Add aid cylinder to 3d viewer |
| AddAidLine | Add aid line to 3d viewer |
| AddAidPolygon | Add aid polygon to 3d viewer |
| AddAidText | Add aid text to 3d viewer |
| AddProjectItem | Add item that will be projected to 2d drawing |
| Clear | Clear all items from 3d viewer |
| ClearAid | Clear all aid items from 3d view |
| CollectItem | Collect items by supplied type |
| CommitTransaction | Commit transaction |
| CreateDb | Create DB in Admin module |
| CreateItem | Create a supplied type item |
| CreateMdb | Creeate MDB in Admin module |
| CreateTeam | Create team in Admin module |
| CreateUser | Create user in Admin module |
| CurrentItem | Get current selected item |
| DeleteItem | Delete selected item |
| Display | Display the selected item |
| DisplayConnected | Display the items connected with the current item |
| DisplayOnly | Only display the selected item |
| GetAngularIncrement | Get angular increment for Model Editor |
| GetItem | Get item by name |
| GetLinearIncrement | Get linear increment for Model Editor |
| GetVersion | Get PipeCAD version string |
| IncludeItem | Include the supplied item into current item |
| Login | Login PipeCAD |
| LookAt | Zoom 3d viewer by supplied item |
| NextAidNumber | Generate next available aid number |
| PickItem | Pick item in the 3d viewer |
| PickPoint | Pick point in the 3d viewer |
| ProjectDXF | Project items to 2d drawing |
| ProjectPoint | Project the point to 2d point |
| Remove | Remove the selected items from 3d viewer |
| RemoveAid | Remove the aid items by supplied aid number from 3d view |
| ReorderItem | Reorder the supplied item to target row |
| Rotate | Rotate the current item |
| SaveWork | Save the modification to database |
| SearchItem | Search items by supplied key and type |
| SetCurrentItem | Set current item |
| SetIncrements | Set linear and angular increment for Model Editor |
| SetIndicator | Set indicator for line edit |
| SetProjector | Set projector to produce 2D drawing |
| SetSnapOptions | Set snap options. |
| StartTransaction | Start transaction to combine the following command to one |
| Translate | Translate the current item |
| TestSnapOption | Test which snap option is set. |
| UpdateViewer | Update 3d viewer |


**Signals**

| Name  | Purpose |
| :---  | :--- |
| currentItemChanged | This signal is sent when the current item changed |

## PipeCad.About
Show about dialog.

```python
PipeCad.About()
```

## PipeCad.GetVersion
Get PipeCAD version string.

```python
PipeCad.GetVersion()
```

**Return**
The PipeCAD version string.

## PipeCad.SaveWork
Save the modification to database. It is good practice to use this function on a regular basis during a long session to ensure maximum data security.

```python
PipeCad.SaveWork()
```

## PipeCad.AddAidLine
Add aid line to 3d viewer to help you with design construction.

```python
PipeCad.AddAidLine(Position theStartPoint, Position theEndPoint, int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theStartPoint | Position | The aid line start point. |
| theEndPoint | Position | The aid line end point. |
| theNumber | int | The aid line group number. Design aids can be grouped together by using the number. |

## PipeCad.AddAidText
Add aid text to 3d viewer.

```python
PipeCad.AddAidText(Position thePoint, QString theText, int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| thePoint | Position | The aid text point. |
| theText | string | The aid text. |
| theNumber | int | The aid text group number. Design aids can be grouped together by using the number. |

## PipeCad.AddAidAxis
Add aid axis to 3d viewer, the axis use LinkPoint to get axis position and direction.

```python
PipeCad.AddAidAxis(LinkPoint theAxis, int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theAxis | LinkPoint | The aid axis point and direction. |
| theNumber | int | The aid axis group number. Design aids can be grouped together by using the number. |

## PipeCad.AddAidArrow
Add aid arrow to 3d viewer.

```python
PipeCad.AddAidArrow(Position thePoint, Direction theDir, double theHeight, double theTubeRadius, double theProportion, int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| thePoint | Position | The aid arrow datum position. |
| theDir | Direction | The aid arrow direction. |
| theHeight | double | The aid arrow total length. |
| theTubeRadius | double | The aid arrow tube radius. |
| theProportion | double | The aid arrow length proportion of total length. |
| theNumber | int | The aid axis group number. Design aids can be grouped together by using the number. |

**Example**

```python
PipeCad.AddAidArrow(aPosition, aTagDirection, 100, 2, 0.3, self.tagId)
```

## PipeCad.AddAidCylinder
Add aid cylinder to 3d viewer.

```python
PipeCad.AddAidCylinder(Position thePoint, Direction theDir, double theHeight, double theRadius, int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| thePoint | Position | The aid cylinder datum position. |
| theDir | Direction | The aid cylinder direction. |
| theHeight | double | The aid cylinder height. |
| theRadius | double | The aid cylinder radius. |
| theNumber | int | The aid axis group number. Design aids can be grouped together by using the number. |

**Example**

```python
PipeCad.AddAidCylinder(aPosition, aTagDirection, 100, 2, self.tagId)
```

## PipeCad.AddAidPolygon
Add aid polygon to 3d viewer to help you with plate design construction.

```python
PipeCad.AddAidPolygon(list thePointList, int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| thePointList | list | The aid polygon point list. |
| theNumber | int | The aid axis group number. Design aids can be grouped together by using the number. |

**Example**

```python
aPointList = list()

# Add some points to the point list.
aPoint = Position(aX, aY, aZ)
aPointList.append(aPoint)

PipeCad.AddAidPolygon(aPointList, self.tagId)
PipeCad.UpdateViewer()
```

## PipeCad.NextAidNumber
Generate next available aid number.

```python
aAidNumber = PipeCad.NextAidNumber()
```

**Return**

The next available aid number.

## PipeCad.RemoveAid
Remove the aid items by supplied aid number from 3d view.

```python
PipeCad.RemoveAid(int theNumber)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theNumber | int | The aid group number. Design aids can be grouped together by using the number. |

## PipeCad.ClearAid
Clear all aid items from 3d view.

```python
PipeCad.ClearAid()
```

## PipeCad.CurrentItem
At the user level there is a concept of current item. Most PipeCAD commands act on the current item. This is often refered to as the **CE**. There is an extensive set of commands to navigate around the database changing the **CE**.

```python
CE = PipeCad.CurrentItem()
```

## PipeCad.SetCurrentItem
Change the current item to the supplied item or name.

```python
PipeCad.SetCurrentItem(string theName)
PipeCad.SetCurrentItem(TreeItem theTreeItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theName | string | Set current item by supplied name |
| theTreeItem | TreeItem | Set current item by supplied item |

**Example**

```python
CE = PipeCad.CurrentItem()
PipeCad.SetCurrentItem("/PIPE")
PipeCad.SetCurrentItem(CE)
```

## PipeCad.GetItem
Get item by supplied name.

```python
PipeCad.GetItem(string theName)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theName | string | Get item by supplied name |

**Return**

Return the item by supplied name. If there is no named item, return None.

**Example**

```python
aCatref = PipeCad.GetItem("/AAZFBD0TT")
```

## PipeCad.StartTransaction
Start transaction to combine the following command to one.

```python
PipeCad.StartTransaction(string theText)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theText | string | Transaction description text |

## PipeCad.CommitTransaction
Commit the transcation.

```python
PipeCad.CommitTransaction()
```

**Example**

```python
PipeCad.StartTransaction("Create Site")

PipeCad.CreateItem("SITE")
aSiteItem = PipeCad.CurrentItem()
aSiteItem.Name = "PIPE-SITE"
aSiteItem.Purpose = "PIPE"

PipeCad.CommitTransaction()
```

## PipeCad.CreateItem
Create a tree item by supplied type and optional name, and set current item to the new item.

```python
PipeCad.CreateItem(string theType, string theName)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theType | string | Tree item type, e.g SITE, ZONE |
| theName | string | Tree item name, optional |

## PipeCad.DeleteItem
Delete the current selected item, the item type parameter is used to confirm the type.

```python
PipeCad.DeleteItem(string theType)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theType | string | Tree item type, e.g SITE, ZONE |

## PipeCad.CreateTeam
Create team item in Admin module.

```python
PipeCad.CreateTeam(string theName, string theDescription)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theName | string | The name of the team, up to ??? symbols |
| theDescription | string | The team description, up to ??? characters |

**Output**

PipeCad will create Team in /*T world hierarchy.

**Example**
```python
PipeCad.CreateTeam("PIPE", "Team for Piping Discipline" )
```

## PipeCad.CreateUser
Create user item in Admin module.

```python
PipeCad.CreateUser(string theName, string theDescription, string thePassword, string theSecurity, list theTeamList)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theName | string | The name of the user |
| theDescription | string | The user description |
| thePassword | string | The user password |
| theSecurity | string | The security of the user, e.g "Free, General" |
| theTeamList | list | The team list that user belong to |

## PipeCad.CreateMdb
Create MDB item in Admin module.

```python
PipeCad.CreateMdb(string theName, string theDescription)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theName | string | The name of the MDB |
| theDescription | string | The MDB description |

## PipeCad.CreateDb
Create DB item in Admin module.

```python
PipeCad.CreateDb(string theName, string theType, int theNumber, string theDescription)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theName | string | The Database name, its format is TeamName/DBName, e.g. /PIPE/DESI |
| theType | string | Database type from the list: DESI, PADD, CATA |
| theNumber| INT | Database nubmber ( in range from 1 to 9999 ) |
| theDescription| STRING | The database description, up to ??? characters |

**Output**

PipeCad will create Database in proper Team hierarchy.

**Example**

```python
PipeCad.CreateDb("PIPE/DESI-1-XYZ-001", "DESI", 2000, "Database for module 1-XYZ-001 - Piping Discipline" )
```

## PipeCad.CollectItem
Collect all items with required type (for ex. Sites) in MDB.

```python
PipeCad.CollectItem(string theType, TreeItem theParentItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theType | string | The item type, e.g "SITE", "ZONE", .etc |
| theParentItem | TreeItem | Collect item in parent item, if there is no parent item, will collect all items in MDB |

**Example**

```python
aSiteItems = PipeCad.CollectItem("SITE")
```

## PipeCad.SearchItem
Search items by supplied key and type.

```python
PipeCad.SearchItem(string theKey, string theType, TreeItem theParentItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theKey | string | Search the keyword in item name |
| theType | string | The search item type, if there is no type, will return all type items |
| theParentItem | TreeItem | Search item in parent item, if there is no parent item, will collect all items in MDB |

**Example**

```python
aPipeItems = PipeCad.SearchItem("PIPE-01", "PIPE")
```

## PipeCad.IncludeItem
Include the item into current item.

```python
PipeCad.IncludeItem(TreeItem theTreeItem, int thePosition)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The tree item will be included into current item |
| thePosition | int | The position in current item member list |

## PipeCad.ReorderItem
Reorder the supplied item to target row.

```python
PipeCad.ReorderItem(TreeItem theTreeItem, int theTargetRow)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The tree item will be included into current item |
| theTargetRow | int | The target row you want move the item to. |

## PipeCad.Translate
Translate the current item by a vector.

```python
PipeCad.Translate(double theDx, doubel theDy, double theDz)
PipeCad.Translate(Position thePos, Direction* theDir, double theOffset)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theDx | double | The translate vector's x component |
| theDy | double | The translate vector's y component |
| theDz | double | The translate vector's z component |
| thePos | Position | The translate start position |
| theDir | Direction | The translate along direction |
| theOffset | double | The translate distance along the direction |

## PipeCad.Rotate
Rotate the current item. If there is no theAxis, will roate about the current item Z axis.

```python
PipeCad.Rotate(LinkPoint theAxis, double theAngle)
PipeCad.Rotate(theAngle)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theAxis | LinkPoint | The rotation position and axis |
| theAngle | double | The ratate angle in degree |

## PipeCad.addDockWidget

```python
    PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
```

## PipeCad.currentItemChanged
This signal is sent when the current item changed. You can connect this signal to your own slot function.

```python
# Connect currentItemChanged signal to a slot function.
PipeCad.currentItemChanged.connect(self.currentItemChanged)

# Disconnect the signal.
PipeCad.currentItemChanged.disconnect()
```

## PipeCad.PickItem
Pick item in the 3d viewer.

```python
aPickItem = PipeCad.PickItem()
```

## PipeCad.PickPoint
Pick point in the 3d viewer.

```python
aPickPoint = PipeCad.PickPoint(int theMode)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theMode | int | The pick point mode, 1 is pick point; 0 is pick item |

## PipeCad.LookAt
Zoom 3d viewer by supplied item.

```python
PipeCad.LookAt(TreeItem theTreeItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The item zoomed to |

## PipeCad.Display
Display the selected item. If in Design module will add the selected to 3d viewer; If in Paragon module, will display the SComponent.

```python
PipeCad.Display(TreeItem theTreeItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The item will add to 3d viewer |

## PipeCad.DisplayOnly
Only display the selected item, other items will be removed from the 3d viewer.

```python
PipeCad.DisplayOnly(TreeItem theTreeItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The item will add to 3d viewer |

## PipeCad.DisplayConnected
Display the items connected with the current item.

```python
PipeCad.DisplayConnected()
```

## PipeCad.Remove
Remove the selected items from 3d viewer.

```python
PipeCad.Remove(TreeItem theTreeItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The item will remove from 3d viewer |

## PipeCad.Clear
Clear all items from 3d viewer.

```python
PipeCad.Clear()
```

## PipeCad.UpdateViewer
Update 3d viewer.

```python
PipeCad.UpdateViewer()
```

## PipeCad.removeDockWidget

```python
    PipeCad.removeDockWidget(self.dockWidget)
```

## PipeCad.setCentralWidget

```python
    PipeCad.setCentralWidget(aMain)
```

## PipeCad.SetIndicator
Set indicator for line edit.

```python
PipeCad.SetIndicator(QWidget theWidget)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theWidget | QWidget | The QLineEdit widget |

## PipeCad.Login
Login PipeCAD.

```python
PipeCad.Login()
```

## PipeCad.GetLinearIncrement
Get linear increment for Model Editor.

```python
PipeCad.GetLinearIncrement()
```
**Return**

Return the linear increment of the Model Editor.

## PipeCad.GetAngularIncrement
Get angular increment for Model Editor.

```python
PipeCad.GetAngularIncrement()
```
**Return**

Return the angular increment of the Model Editor.

## PipeCad.SetIncrements
Set linear and angular increment for Model Editor.

```python
PipeCad.SetIncrements(double theLinearIncrement, double theAngularIncrement)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theLinearIncrement | double | The linear increment |
| theAngularIncrement | double | The angular increment |

## PipeCad.SetProjector
Set projector to produce 2D drawing.

```python
PipeCad.SetProjector(Position theDatum, Direction theDn, Direction theDx, double theScale)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theDatum | Position | The project plane datum point |
| theDn | Direction | The project plane normal direction |
| theDx | Direction | The project plane x direction |
| theScale | double | The project scale, default is 1.0 |


## PipeCad.SetSnapOptions
Set snap object options.

```python
PipeCad.SetSnapOptions(PipeCad.SnapOptions theSnapOptions)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theSnapOptions | PipeCad.SnapOptions | The object snap options. |

**Example**

```python
PipeCad.SetSnapOptions(PipeCad.SnapEnd | PipeCad.SnapPpoint)
```

## PipeCad.TestSnapOption
Test which snap option is set.

```python
PipeCad.TestSnapOption(PipeCad.SnapOption theSnapOption)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theSnapOption | PipeCad.SnapOption | The object snap option. |

**Example**

```python
PipeCad.TestSnapOption(PipeCad.SnapEnd)
```

## PipeCad.AddProjectItem
Add item that will be projected to 2d drawing.

```python
PipeCad.AddProjectItem(TreeItem theTreeItem)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theTreeItem | TreeItem | The tree item to be projected |

## PipeCad.ProjectPoint
Project the point to 2d point.

```python
PipeCad.ProjectPoint(Position thePoint)
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| thePoint | Position | The point to be projected |

**Return**

Return the 2d point that projected to the plane.

## PipeCad.ProjectDXF
Project items to 2d DXF drawing.

```python
PipeCad.ProjectDXF(string theFileName);
```

**Parameter List**

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| theFileName | string | The output drawing DXF file name |
