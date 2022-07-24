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

# PipeCad API
PipeCad is a core object of PipeCAD, the PipeCad object is a mechanism for providing methods which are not specific to the standard objects, such as TreeItem, QWidget etc.

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
| RemoveAid | Remove the aid item by supplied number |
| ClearAid | Clear all aid item |

## About
Show about dialog.

```python
   PipeCad.About()
```

## GetVersion
Get PipeCAD version string.

```python
   PipeCad.GetVersion()
```

**Return**
string.

## SaveWork
Save the modification to database. It is good practice to use this function on a regular basis during a long session to ensure maximum data security.

```python
   PipeCad.SaveWork()
```

## AddAidLine
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

**Return**
None.

## PipeCad.AddAidText
Add aid text to 3d viewer.

```python
   PipeCad.AddAidText(Position thePoint, QString theText, int theNumber)
```

**Parameter List**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| thePoint | Position | The aid text point. |
| theNumber | int | The aid text group number. Design aids can be grouped together by using the number. |

**Return**
None.

## PipeCad.addDockWidget

```python
    PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
```
## PipeCad.ClearAid
Remmove aid lines from 3d view
```python
    PipeCad.ClearAid()
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
