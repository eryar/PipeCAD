# Developing of new utility

## Code development
Each developer can evaluate his own macros library for using inside PipeCAD. In this case all macros have to be placed in dedicated folder inside folder **%PYTHONPATH%**. For example, developer's library will be named **omp** and placed in default library folder of PipeCAD:
![Developer's Library Folder](../../images/development/new_utility/sample_file.png)  
## Calling Utility in PipeCAD
For loading utility there needs to run command for importing utility module into PipeCAD:
```python 
import omp.sample as sm
```

After importing module there will be possible to show utility form on screen:
```python 
sm.ShowSample()
```

In result form will be shown: 

![Sample Utility Window](../../images/development/new_utility/sample_window.png)



