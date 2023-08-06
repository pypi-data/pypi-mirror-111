# chinacoordtran
Python 版本百度坐标（BD09）、国测局坐标（火星坐标，GCJ02）和WGS84坐标相互转换
##  运行环境
支持Python2.X 和Python3.X
## 安装方式
```python
pip install chinacoordtran
```

## 引用方式
```python
from chinacoordtran import gcj02towgs84
from chinacoordtran import wgs84togcj02
from chinacoordtran import gcj02tobd09
from chinacoordtran import bd09togcj02
from chinacoordtran import CoordTran
```
## 目录
- [坐标转换类](#坐标转换类)
   - [gcj02towgs84类](#gcj02towgs84类)
      - [gcj02towgs84调用示例](#gcj02towgs84调用示例)
   - [wgs84togcj02类](#wgs84togcj02类)
      - [wgs84togcj02调用示例](#wgs84togcj02调用示例)
   - [gcj02tobd09类](#gcj02tobd09类)
      - [gcj02tobd09调用示例](#gcj02tobd09调用示例)
   - [bd09togcj02类](#bd09togcj02类)
      - [bd09togcj02调用示例](#bd09togcj02调用示例)
- [坐标转换CoordTran类方法](#坐标转换CoordTran类方法)
    - [gcj02towgs84方法](#gcj02towgs84方法)
    - [wgs84togcj02方法](#wgs84togcj02方法)
    - [gcj02tobd09方法](#gcj02tobd09方法)
    - [bd09togcj02方法](#bd09togcj02方法)
## 坐标转换类
### gcj02towgs84类
```python
from chinacoordtran import gcj02towgs84
gcj02towgs84Instance = gcj02towgs84()
```
#### gcj02towgs84调用示例
```python
from chinacoordtran import gcj02towgs84
gcj02towgs84Instance = gcj02towgs84()
result =gcj02towgs84Instance.CoordTran(121.467152, 31.235441)
```
### wgs84togcj02类
```python
from chinacoordtran import wgs84togcj02
wgs84togcj02Instance= wgs84togcj02()
```
#### wgs84togcj02调用示例
```python
from chinacoordtran import wgs84togcj02
wgs84togcj02Instance= wgs84togcj02()
result =wgs84togcj02Instance.CoordTran(121.467152, 31.235441)
```
### gcj02tobd09类
```python
from chinacoordtran import gcj02tobd09
gcj02tobd09Instance =gcj02tobd09()
```
#### gcj02tobd09调用示例
```python
from chinacoordtran import gcj02tobd09
gcj02tobd09Instance =gcj02tobd09()
result =gcj02tobd09Instance.CoordTran(121.467152, 31.235441)
```

### bd09togcj02类
```python
from chinacoordtran import bd09togcj02
bd09togcj02Instance=bd09togcj02()
```
#### bd09togcj02调用示例
```python
from chinacoordtran import bd09togcj02
bd09togcj02Instance=bd09togcj02()
result =bd09togcj02Instance.CoordTran(121.467152, 31.235441)
```
## 坐标转换CoordTran类方法
### gcj02towgs84方法
```python
from chinacoordtran import CoordTran
coordTranInstance=CoordTran()
coordTranInstance.gcj02towgs84(121.467152, 31.235441)
```
### wgs84togcj02方法
```python
from chinacoordtran import CoordTran
coordTranInstance=CoordTran()
coordTranInstance.wgs84togcj02(121.467152, 31.235441)
```
### gcj02tobd09方法
```python
from chinacoordtran import CoordTran
coordTranInstance=CoordTran()
coordTranInstance.gcj02tobd09(121.467152, 31.235441)
```
### bd09togcj02方法
```python
from chinacoordtran import CoordTran
coordTranInstance=CoordTran()
coordTranInstance.bd09togcj02(121.467152, 31.235441)
```