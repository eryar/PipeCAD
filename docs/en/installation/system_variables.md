# System variables which are used by PipeCAD 

To customise PipeCAD installation in according with company IT rules, administrator can modify different system variables.

* Path to folder, where projects are located:
```batch
SET PROJECTS_DIR=C:\PipeCAD\projects
```

* Path to folders, where Python libraries are installed:
```batch
SET PYTHONPATH=%PYTHONPATH%;%~dp0lib\site-packages;C:\Github\PipeCAD\lib;C:\PipeCAD\lib;
```

* Path to folder, where Python cache will be created:
```batch
SET PYTHONPYCACHEPREFIX=%TEMP%
```

* Path to folder, where from PipeCAD will take user documentation
```batch
SET PIPECAD_HELP_PATH=C:\Github\PipeCAD\docs
```

* Path to folder with menu files of PipeCAD
```batch
SET PIPECAD_MENU_PATH=C:\Github\PipeCAD\uic
```

* Path to folder with PipeCAD settings
```
SET PIPECAD_SETTINGS_PATH=C:\Github\PipeCAD\settings
```

