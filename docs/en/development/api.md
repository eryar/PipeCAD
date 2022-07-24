# PipeCAD Customization Guide {#pipecad_customization_guide}

# Introduction
This manual describes how to use Python to customize PipeCAD.

You do not have to be a professional programmer to start to learn Python, although you may find this manual difficult to follow unless you have some understanding of programming concepts such as if statements and do loops. If you have no programming experience, you should consider attending a Python Training Course.

## Customizing a Graphical User Interface

PipeCAD make use of a Graphical User Interface (GUI) to drive the software. The interfaces provided with your PipeCAD software are designed to apply to a wide range of situations and business needs. However, as you become more experienced with PipeCAD you may wish to design an interface that is more closely related to your requirements.
Qt has been specifically introduced for writing and customising the Forms and Menus for PipeCAD. 
Before you begin customising a GUI, you must have a good working knowledge of PipeCAD.

## Serious Warning About Software Customization

The ability to customise individual Applications to suit your own specific needs gives you great flexibility in the ways in which you use your system.
But it also introduces the risk that your modified macros may not be compatible with future versions of the software, since they are no longer under PipeCAD’s control.
Your own Applications may diverge from future standard versions and may not take advantage of product enhancements incorporated into the standard product.
To minimise this risk, it is most important that your in-house customisation policies constrain any changes which you make to the Applications so that they retain maximum compatibility with the standard product at all times.
Remember that PipeCAD can give you full technical support only for products over which it has control. We cannot guarantee to solve problems caused by software which you have written yourself.

# Object Type Details

## Position
Position point in 3D space.

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| X | double | The X component |
| Y | double | The Y component |
| Z | double | The Z component |
| Origin | TreeItem | The TreeItem that is the origin |

**Methods**

| Name | Result | Description |
| :--- | :--- | :--- |
| Offset(Direction theDir, double theOffset) | Position | Returns a position offset by the supplied length in the supplied direction. |
| Distance(Position thePosition) | Position | Returns the distance between two positions. |

## Direction
Describes a unit vector in 3D space. This unit vector is also called "Direction".

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| X | double | The X component |
| Y | double | The Y component |
| Z | double | The Z component |
| Origin | TreeItem | The TreeItem that is the origin |

**Methods**

| Name | Result | Description |
| :--- | :--- | :--- |
| Reversed() | Direction | Reversed the direction and return the opposite direction. |
| IsParallel(Direction theDir, double theTolerance) | bool | Returns True if the supplied direction is parallel according to tolerance supplied, false otherwise. |

## Orientation
This defines the orientation of a frame of reference (i.e. the directions of the XYZ axes) in the frame of reference of that defined by an origin database reference. It does not define a position.

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| Alpha | double | The Alpha component |
| Beta | double | The Beta component |
| Gamma | double | The Gamma component |
| XDirection | Direction | Return X axis direction of the ORIENTATION as a DIRECTION. |
| YDirection | Direction | Return Y axis direction of the ORIENTATION as a DIRECTION. |
| ZDirection | Direction | Return Z axis direction of the ORIENTATION as a DIRECTION. |
| Origin | TreeItem | The TreeItem that is the origin |

## LinkPoint
LinkPoint is P-Point for piping component.

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| Key | string | P-Point key, such as P1 |
| Bore | string | P-Point bore |
| Type | string | P-Point connection type |
| Position | Position | P-Point position |
| Direction | Direction | P-Point direction |

## TreeItem

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| RefNo | string | Reference number |
| Type | string | Item type |
| Name | string | Item name |
| Owner | TreeItem | Parent item |
| Member | list | Member list |

## Project
Project data.

**Property**

| Name | Type | Description |
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

| Name | Type | Description |
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

| Name | Type | Description |
| :--- | :--- | :--- |
| Name | string | MDB name |
| Description | string | MDB description |
| RefNo | string | String containing Database reference number |

## User
User can login project.

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| Name | string | User name |
| Description | string | User description |
| Access | string | User access rights(FREE, GENERAL) |
| RefNo | string | STRING containing Database reference number |
| Password | string | User password |

# PipeCad API
PipeCad is a core object of PipeCAD, the PipeCad object is a mechanism for providing methods which are not specific to the standard objects, such as TreeItem, QWidget etc.

**Property**

| Name | Type | Description |
| :--- | :--- | :--- |
| Projects | list | The project list by environment variables |
| CurrentProject | Project | The login project |
| CurrentSession | Session | The current session |

**Methods**

| Name  | Description |
| :---  | :--- |
| About | Show about dialog|
| GetVersion | Get PipeCAD version string |
| SaveWork | Save the modification to database |
| AddAidLine | Add aid line to 3d viewer |
| AddAidText | Add aid text to 3d viewer |
| AddAidAxis | Add aid axis to 3d viewer |
| AddAidArrow | Add aid arrow to 3d viewer |
| AddAidCylinder | Add aid cylinder to 3d viewer |
| AddAidPolygon | Add aid polygon to 3d viewer |
| NextAidNumber | Generate next available aid number |
| RemoveAid | Remove the aid items by supplied aid number from 3d view |
| ClearAid | Clear all aid items from 3d view |
| CurrentItem | Get current selected item |
| SetCurrentItem | Set current item |
| GetItem | Get item by name |
| StartTransaction | Start transaction to combine the following command to one |
| CommitTransaction | Commit transaction |
| CreateItem | Create a supplied type item |
| DeleteItem | Delete selected item |
| CreateTeam | Create team in Admin module |
| CreateUser | Create user in Admin module |
| CreateMdb | Creeate MDB in Admin module |
| CreateDb | Create DB in Admin module |
| CollectItem | Collect items by supplied type |
| SearchItem | Search items by supplied key and type |
| IncludeItem | Include the item into current item |
| Translate | Translate the current item |
| Rotate | Rotate the current item |
| PickItem | Pick item in the 3d viewer |
| PickPoint | Pick point in the 3d viewer |
| LookAt | Zoom 3d viewer by supplied item |
| Display | Display the selected item |
| DisplayOnly | Only display the selected item |
| DisplayConnected | Display the items connected with the current item |
| Remove | Remove the selected items from 3d viewer |
| Clear | Clear all items from 3d viewer |
| UpdateViewer | Update 3d viewer |
| SetIndicator | Set indicator for line edit |
| Login | Login PipeCAD |
| GetLinearIncrement | Get linear increment for Model Editor |
| GetAngularIncrement | Get angular increment for Model Editor |
| SetIncrements | Set linear and angular increment for Model Editor |
| SetProjector | Set projector to produce 2D drawing |
| AddProjectItem | Add item that will be projected to 2d drawing |
| ProjectPoint | Project the point to 2d point |
| ProjectDXF | Project items to 2d drawing |

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

| Parameter | Type | Description |
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

| Parameter | Type | Description |
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

| Parameter | Type | Description |
| :--- | :--- | :--- |
| theAxis | LinkPoint | The aid axis point and direction. |
| theNumber | int | The aid axis group number. Design aids can be grouped together by using the number. |

## PipeCad.AddAidArrow
Add aid arrow to 3d viewer.

```python
PipeCad.AddAidArrow(Position thePoint, Direction theDir, double theHeight, double theTubeRadius, double theProportion, int theNumber)
```

**Parameter List**

| Parameter | Type | Description |
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

| Parameter | Type | Description |
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

| Parameter | Type | Description |
| :--- | :--- | :--- |
| thePointList | list | The aid polygon point list. |
| theNumber | int | The aid axis group number. Design aids can be grouped together by using the number. |

**Example**

```python
   aPointList = list()
   
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

| Parameter | Type | Description |
| :--- | :--- | :--- |
| theNumber | int | The aid group number. Design aids can be grouped together by using the number. |

## PipeCad.ClearAid
Clear all aid items from 3d view.

```python
PipeCad.ClearAid()
```

## PipeCad.addDockWidget

```python
    PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
```
## PipeCad.CollectItem
Collect all items with required type (for ex. Sites) in mdb
```python
    aDbItems = PipeCad.CollectItem("SITE")
```
## PipeCad.CommitTransaction
```python
    PipeCad.CommitTransaction()
```
## PipeCad.CreateItem

```python
    PipeCad.CreateItem("SITE", SiteName)
```
## PipeCad.CurrentItem
Get current element
```python
    aItem = PipeCad.CurrentItem()
```
## PipeCad.currentItemChanged.connect

```python
    PipeCad.currentItemChanged.connect(self.currentItemChanged)
```
## PipeCad.currentItemChanged.disconnect

```python
    PipeCad.currentItemChanged.disconnect()
```
## PipeCad.CurrentProject
Get current project
```python
    CurProject = PipeCad.CurrentProject
```
## PipeCad.DeleteItem
Delete required element
```python
    PipeCad.DeleteItem("TEAM")
```
## PipeCad.GetItem
Goto to required element
```python
    aCatref = PipeCad.GetItem("/AAZFBD0TT")
```
## PipeCad.Login

```python
    PipeCad.Login()
```
## PipeCad.PickItem

```python
    aPickItem = PipeCad.PickItem()
```
## PipeCad.Projects
Getting list of projects
```python
    ProjectsList = PipeCad.Projects
```
## PipeCad.removeDockWidget

```python
    PipeCad.removeDockWidget(self.dockWidget)
```
## PipeCad.Rotate

```python
    PipeCad.Rotate(self.currentItem.ArrivePoint, aAngle)
```
## PipeCad.SaveWork
Save of current session changes 
```python
    PipeCad.SaveWork()
```
## PipeCad.setCentralWidget

```python
    PipeCad.setCentralWidget(aMain)
```
## PipeCad.SetCurrentItem

Syntax:
```python
    PipeCad.SetCurrentItem(aItem.data(Qt.UserRole))
```

## PipeCad.SetIndicator

```python
    PipeCad.SetIndicator(self.textPassword)
```
## PipeCad.StartTransaction

```python
    PipeCad.StartTransaction("Create Team")
```
## PipeCad.Translate

```python
    PipeCad.Translate(aPs, aDir, aOffset)
```
## PipeCad.Update

```python
    PipeCad.Update()
```

## PipeCad.CreateDb( Team/Name, Type, Number, Description )
### Input
|Name|Type|Purpose|
|----|----|-------|
|Team|STRING|Owning Team|
|Name|STRING|The name of the database, up to ??? symbols|
|Type|STRING|Database type from the list: DESI, PADD, CATA|
|Number|INT|Database nubmber ( in range from 1 to ???? )|
|Description|STRING|The database description, up to ??? characters|

### Output
PipeCad will create Database in proper Team hierarchy.

## Example
```python
    PipeCad.CreateDb("PIPE/DESI-1-XYZ-001", "DESI", 2000, "Database for module 1-XYZ-001 - Piping Discipline" )
```

## PipeCad.CreateTeam( Name, Description )
### Input
|Name|Type|Purpose|
|----|----|-------|
|Name|STRING|The name of the team, up to ??? symbols|
|Description|STRING|The database description, up to ??? characters|

### Output
PipeCad will create Team in /*T world hierarchy.

### Example
```python
    PipeCad.CreateTeam("PIPE", "Team for Piping Discipline" )
```
