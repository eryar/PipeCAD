## PipeCad.AddAidLine
Show aid line on 3d view
```python
    PipeCad.AddAidLine(aPs, aPe, 1)
```
## PipeCad.AddAidText
Show aid text on 3d view
```python
    PipeCad.AddAidText(aPe, aT, 1)
```
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

Syntax examples:
```python
    PipeCad.CreateDb("PIPE/DESI-1-XYZ-001", "DESI", 2000, "Database for module 1-XYZ-001 - Piping Discipline" )
```

## PipeCad.CreateTeam()
### Input
|Name|Type|Purpose|
|----|----|-------|
|Name|STRING|The name of the team, up to ??? symbols|
|Description|STRING|The database description, up to ??? characters|

### Output
PipeCad will create Team in /*T world hierarchy.

Syntax:
```python
    PipeCad.CreateTeam("PIPE", "Team for Piping Discipline" )
```
