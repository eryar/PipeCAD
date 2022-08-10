# System variables which are used by PipeCAD 

To customise PipeCAD installation in according with company IT rules, administrator can modify different system variables.

* Path to folder where projects are located:
```batch
SET PROJECTS_DIR=C:\PipeCAD\projects
```

* Path to folders where Python libraries are installed:
```batch
SET PYTHONPATH=%PYTHONPATH%;%~dp0lib\site-packages;C:\PipeCAD\lib
```

* Path to folder where Python cache will be created:
```batch
SET PYTHONPYCACHEPREFIX=%TEMP%
batch
