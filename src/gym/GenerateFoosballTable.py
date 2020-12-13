import math

indent = 0

metersPerInch = 0.0254
tableWidth = 48 * metersPerInch
tableDepth = 27 * metersPerInch
tableHeight = 4.25 * metersPerInch
wall = 1 * metersPerInch
goalWidth = 8.25 * metersPerInch
goalHeight = 3 * metersPerInch
rodDistance = 6 * metersPerInch
rodLength = 60 * metersPerInch

def stag(tagname, attributeDict={}):
    global indent
    attributes=''
    for attr in attributeDict:
        attributes = attributes + f' {attr}="{attributeDict[attr]}"'
    print(' ' * indent + f'<{tagname}{attributes}>')
    indent += 2

def ctag(tagname, attributeDict={}):
    global indent
    attributes=''
    for attr in attributeDict:
        attributes = attributes + f' {attr}="{attributeDict[attr]}"'
    print(' ' * indent + f'<{tagname}{attributes}/>')

def etag(tagname):
    global indent
    indent -= 2
    print(' ' * indent + f'</{tagname}>')

def material(name, rgba):
    stag('material', {'name': name})
    ctag('color', {'rgba': rgba})
    etag('material')

def materialRef(name):
    ctag('material', {'name': name})

def visualBox(color, x, y, z, sx, sy, sz, rpy='0 0 0'):
    stag('visual')
    ctag('origin', {'xyz': f'{x:f} {y:f} {z:f}', 'rpy': rpy})
    stag('geometry')
    ctag('box', {'size': f'{sx:f} {sy:f} {sz:f}'})
    etag('geometry')
    materialRef(color)
    etag('visual')

def collisionBox(x, y, z, sx, sy, sz, rpy='0 0 0'):
    stag('collision')
    ctag('origin', {'xyz': f'{x:f} {y:f} {z:f}', 'rpy': rpy})
    stag('geometry')
    ctag('box', {'size': f'{sx:f} {sy:f} {sz:f}'})
    etag('geometry')
    etag('collision')

def visualCylinder(color, x, y, z, radius, length, rpy='0 0 0'):
    stag('visual')
    ctag('origin', {'xyz': f'{x:f} {y:f} {z:f}', 'rpy': rpy})
    stag('geometry')
    ctag('cylinder', {'radius': f'{radius:f}', 'length': f'{length:f}'})
    etag('geometry')
    materialRef(color)
    etag('visual')

def fixedJoint(name, parent, child):
    stag('joint', {'name': name, 'type': 'fixed'})
    ctag('parent', {'link': parent})
    ctag('child', {'link': child})
    etag('joint')

def prismaticJoint(name, parent, child):
    stag('joint', {'name': name, 'type': 'prismatic'})
    ctag('axis', {'xyz': '0 1 0'})
    ctag('parent', {'link': parent})
    ctag('child', {'link': child})
    ctag('limit', {'effort': 100, 'velocity': 100})
    etag('joint')

def continuousJoint(name, parent, child):
    stag('joint', {'name': name, 'type': 'continuous'})
    ctag('axis', {'xyz': '0 1 0'})
    ctag('parent', {'link': parent})
    ctag('child', {'link': child})
    ctag('limit', {'effort': 100, 'velocity': 100})
    etag('joint')

def table():
    stag('link', {'name': 'table'})
    visualBox('black', 0, -(tableDepth+wall)/2, 0, tableWidth, wall, tableHeight)
    visualBox('black', 0,  (tableDepth+wall)/2, 0, tableWidth, wall, tableHeight)
    visualBox('black', -(tableWidth+wall)/2, 0, 0, wall, tableDepth + wall*2, tableHeight)
    visualBox('black',  (tableWidth+wall)/2, 0, 0, wall, tableDepth + wall*2, tableHeight)
    collisionBox(0, 0, 0, tableWidth, tableDepth, tableHeight)
    etag('link')
    stag('link', {'name': 'floor'})
    visualBox('green', 0, 0, -(tableHeight+wall)/2, tableWidth+wall*2, tableDepth+wall*2, wall)
    collisionBox(      0, 0, -(tableHeight+wall)/2, tableWidth+wall*2, tableDepth+wall*2, wall)
    etag('link')
    fixedJoint('floor_joint', 'table', 'floor')

def man(rodIndex, manIndex, xOffset, yOffset):
    stag('link', {'name': f'rod{rodIndex}_man{manIndex}'})
    visualBox('yellow', xOffset, yOffset, 0, wall, wall*2, tableHeight)
    etag('link')
    if manIndex == 0:
        continuousJoint(f'rod{rodIndex}_man{manIndex}_joint', f'rod{rodIndex}', f'rod{rodIndex}_man{manIndex}')
    else:
        fixedJoint(f'rod{rodIndex}_man{manIndex}_joint', f'rod{rodIndex}_man0', f'rod{rodIndex}_man{manIndex}')

def rod(index, xOffset, menPositions=[0]):
    stag('link', {'name': f'rod{index}'})
    visualCylinder('silver', xOffset, 0, 0, .015, rodLength, f'{math.pi/2:f} 0 0')
    etag('link')
    prismaticJoint(f'rod{index}_joint', 'table', f'rod{index}')
    for manIndex in range(len(menPositions)):
        man(index, manIndex, xOffset, menPositions[manIndex])

import sys

orig_stdout = sys.stdout
f = open('FoosballTable2.urdf', 'w')
sys.stdout = f

stag('robot', {'name': 'foosball_table'})
material('black', '0.1 0.1 0.1 1.0')
material('green', '0.1 0.4 0.1 1.0')
material('silver','0.5 0.5 0.5 1.0')
material('yellow','0.5 0.5 0.1 1.0')
table()
goalieDistance =   8.125*metersPerInch
twomanDistance =   9.500*metersPerInch
fivebarDistance =  4.750*metersPerInch
threemanDistance = 7.250*metersPerInch
rod(1, rodDistance * -3.5, [-goalieDistance, 0, goalieDistance])
rod(2, rodDistance * -2.5, [-twomanDistance/2, twomanDistance/2])
rod(3, rodDistance * -1.5, [-threemanDistance, 0, threemanDistance])
rod(4, rodDistance * -0.5, [-fivebarDistance*2, -fivebarDistance, 0, fivebarDistance, fivebarDistance*2])
rod(5, rodDistance *  0.5, [-fivebarDistance*2, -fivebarDistance, 0, fivebarDistance, fivebarDistance*2])
rod(6, rodDistance *  1.5, [-threemanDistance, 0, threemanDistance])
rod(7, rodDistance *  2.5, [-twomanDistance/2, twomanDistance/2])
rod(8, rodDistance *  3.5, [-goalieDistance, 0, goalieDistance])
#floor()
etag('robot')