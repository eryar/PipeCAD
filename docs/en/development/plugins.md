# Python Libraries in PipeCAD
Using PIP module can be easily installed third-party modules of Python, such as Excel read-write module Pandas, which is convenient to generate material tables; computer vision module OpenCV; artificial intelligence AI module Caffe, TensorFlow and other machine learning frameworks.
## Installing PIP application 
To install PIP you need to start batch  file **%PIPECAD_EXE%\get_pip.bat**. During installation process it will be downloaded required modules into folder **%PIPECAD_EXE%\Scripts**. 
## Installing Python libraries

## Loading of Python script
For loading Python script (for ex. C:\Data\Script.py) there will use next command:
```python
    exec(open("C:\Data\PythonLoad.py",encoding='utf8').read())
```
