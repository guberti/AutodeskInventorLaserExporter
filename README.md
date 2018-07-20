# AutodeskInventorLaserExporter
Easily laser cut faces from Autodesk Inventor without complicated workarounds

![Demonstration Image](https://i.imgur.com/9FZlrst.png)

## Installation

The only non-standard dependency is `dxfgrabber`.
If you dan't have it already, please install with
your favourite package manager, e.g.
```
pip install dxfgrabber
```

## Usage

Right-click on your desired face with Inventor, and select "Export Face As"
Save it somewhere with default settings (i.e. as a DXF)
Then, either run
```
python DXFtoSVG.py myDxfFile.dxf
```
to convert a single file, or run 
```
python batchConvertSVG.py myDxfFile.dxf
```
