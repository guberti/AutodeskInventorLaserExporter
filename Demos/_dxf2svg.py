#!/usr/bin/env python

import dxfgrabber
import math
import sys

# SVG TEMPLATES

SVG_PREAMBLE = \
'<svg xmlns="http://www.w3.org/2000/svg" ' \
'version="1.1" viewBox="{0} {1} {2} {3}">\n'

# SVG_MOVE_TO = 'M {0} {1:.2f} '
# SVG_LINE_TO = 'L {0} {1:.2f} '
# SVG_ARC_TO  = 'A {0} {1:.2f} {2} {3} {4} {5:.2f} {6:.2f} '

SVG_MOVE_TO = 'M {0} {1} '
SVG_LINE_TO = 'L {0} {1} '
SVG_CURVE_TO = 'C {0} {1} {2} {3} {4} {5} '
SVG_ARC_TO  = 'A {0} {1} {2} {3} {4} {5} {6} '


SVG_PATH = \
'<path d="{0}" fill="none" stroke="{1}" stroke-width="{2:.2f}" />\n'

SVG_LINE = \
'<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" stroke="{4}" stroke-width="{5:.2f}" />\n'

SVG_CIRCLE = \
'<circle cx="{0}" cy="{1}" r="{2}" stroke="{3}" stroke-width="{4}" fill="none" />\n'

LINE_THICKNESS = 0.096
SF = 95.338737

# SVG DRAWING HELPERS

def angularDifference(startangle, endangle):
  result = endangle - startangle
  while result >= 360:
    result -= 360
  while result < 0:
    result += 360
  return result

def moveTo(point):
    return SVG_MOVE_TO.format(point.x,height-point.y)

def lineTo(point):
    return SVG_LINE_TO.format(point.x,height-point.y)

def pathStringFromPoints(points):  
  pathString = SVG_MOVE_TO.format(*points[0])
  for i in range(1,len(points)):
    pathString += SVG_LINE_TO.format(*points[i])
  return pathString

def handleEntity(svgFile, e):
  if isinstance(e, dxfgrabber.dxfentities.Line):      
    svgFile.write(SVG_LINE.format(
      e.start[0] * SF, e.start[1] * SF, e.end[0] * SF, e.end[1] * SF,
      'red', LINE_THICKNESS
    ))

  elif isinstance(e, dxfgrabber.dxfentities.LWPolyline):
    pathString = pathStringFromPoints(e)
    if e.is_closed:
      pathString += 'Z'
    svgFile.write(SVG_PATH.format(pathString, 'red', LINE_THICKNESS))
    
  elif isinstance(e, dxfgrabber.dxfentities.Circle):
    svgFile.write(SVG_CIRCLE.format(e.center[0] * SF, e.center[1] * SF,
      e.radius * SF, 'red', LINE_THICKNESS))

  elif isinstance(e, dxfgrabber.dxfentities.Arc):
    
    # compute end points of the arc
    x1 = e.center[0] + e.radius * math.cos(math.pi * e.startangle / 180)
    y1 = e.center[1] + e.radius * math.sin(math.pi * e.startangle / 180)
    x2 = e.center[0] + e.radius * math.cos(math.pi * e.endangle / 180)
    y2 = e.center[1] + e.radius * math.sin(math.pi * e.endangle / 180)

    pathString  = SVG_MOVE_TO.format(x1 * SF, y1 * SF)
    pathString += SVG_ARC_TO.format(e.radius * SF, e.radius * SF, 0,
      int(angularDifference(e.startangle, e.endangle) > 180), 1, x2 * SF, y2 * SF)

    svgFile.write(SVG_PATH.format(pathString, 'red', LINE_THICKNESS))
  elif isinstance(e, dxfgrabber.dxfentities.Polyline):
    pathString = SVG_MOVE_TO.format(e.points[0][0] * SF, e.points[0][1] * SF)
    for i in range(0, len(e.points)):
      nextPoint = e.points[(i+1) % len(e.points)]

      if (e.bulge[i]): # If we need to draw an arc
        # First we'll compute the included angle
        angle = 4 * math.atan(e.bulge[i])
        # Now, the base of the isosceles triangle
        base = math.hypot(e.points[i][0] - nextPoint[0], e.points[i][1] - nextPoint[1])
        # Now, we'll solve the isosceles triangle for the radius
        radius = base / (2 * math.sin(angle / 2.0))

        pathString += SVG_ARC_TO.format(abs(radius) * SF, abs(radius) * SF, 0, \
          0, int(e.bulge[i] > 0), nextPoint[0] * SF, nextPoint[1] * SF)
      else:
        pathString += SVG_LINE_TO.format(nextPoint[0] * SF, nextPoint[1] * SF)

    if e.is_closed:
      pathString += 'Z'
    svgFile.write(SVG_PATH.format(pathString, 'red', LINE_THICKNESS))
  else:
    print "Unknown entity type " + str(e)

def saveToSVG(svgFile, dxfData):
  
  minX = dxfData.header['$EXTMIN'][0] * SF - 100
  minY = dxfData.header['$EXTMIN'][1] * SF - 100
  maxX = dxfData.header['$EXTMAX'][0] * SF + 100
  maxY = dxfData.header['$EXTMAX'][1] * SF + 100
  
  # TODO: also handle groups
  svgFile.write(SVG_PREAMBLE.format(
    minX, minY, maxX - minX, maxY - minY))

  for entity in dxfData.entities:
    layer = dxfData.layers[entity.layer]
    if layer.on and not layer.frozen:
      handleEntity(svgFile, entity)
     
  svgFile.write('</svg>\n')
#end: saveToSVG

if __name__ == '__main__':
  # TODO: error handling
  if len(sys.argv) < 2:
    sys.exit('Usage: {0} file-name'.format(sys.argv[0]))

  filename = sys.argv[1]

  # grab data from file
  dxfData = dxfgrabber.readfile(filename)

  svgName = '.'.join(filename.split('.')[:-1] + ['svg'])
  svgFile = open(svgName, 'w')

  saveToSVG(svgFile, dxfData)

  svgFile.close()
