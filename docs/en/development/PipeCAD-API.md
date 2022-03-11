## PipeCad.AddAidLine

```python
    PipeCad.AddAidLine(aPs, aPe, 1)
```
## PipeCad.AddAidText

```python
    PipeCad.AddAidText(aPe, aT, 1)
```
## PipeCad.addDockWidget

```python
    PipeCad.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
```
## PipeCad.ClearAid

```python
    PipeCad.ClearAid()
```
## PipeCad.CollectItem

```python
    aDbItems = PipeCad.CollectItem("DB")
```
## PipeCad.CommitTransaction

```python
    PipeCad.CommitTransaction()
```
## PipeCad.CreateItem

```python
    PipeCad.CreateItem("TEAM", "*" + aName)
```
## PipeCad.CurrentItem

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
## PipeCad.CurrentProject.Code

```python
    self.textCode = QLineEdit(PipeCad.CurrentProject.Code)
```
## PipeCad.DeleteItem

```python
    PipeCad.DeleteItem("TEAM")
```
## PipeCad.GetItem

```python
    self.statItem = PipeCad.GetItem("/*S")
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

```python
    for aProject in ( PipeCad.Projects ):
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

```python
    PipeCad.SaveWork()
```
## PipeCad.setCentralWidget

```python
    PipeCad.setCentralWidget(aMain)
```
## PipeCad.SetCurrentItem

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
