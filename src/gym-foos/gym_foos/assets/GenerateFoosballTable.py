import math

indent = 0

metersPerInch = 0.0254
tableWidth = 48 * metersPerInch
tableDepth = 27 * metersPerInch
tableHeight = 6.25 * metersPerInch #4.25 * metersPerInch
wall = 1 * metersPerInch
goalWidth = 8.25 * metersPerInch
goalHeight = 3 * metersPerInch
rodDistance = 6 * metersPerInch
rodLength = 60 * metersPerInch
rodDiameter = 3/8 * metersPerInch
manWidth = 1 * metersPerInch
manDepth = 0.5 * metersPerInch
manHeight = 4.0 * metersPerInch
manOffset = 1.0 * metersPerInch

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

def fixedJoint(name, parent, child, x=0, y=0, z=0, rpy='0 0 0'):
    stag('joint', {'name': name, 'type': 'fixed'})
    ctag('origin', {'xyz': f'{x:f} {y:f} {z:f}', 'rpy': rpy})
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

def continuousJoint(name, parent, child, x=0, y=0, z=0, rpy='0 0 0'):
    stag('joint', {'name': name, 'type': 'continuous'})
    ctag('origin', {'xyz': f'{x:f} {y:f} {z:f}', 'rpy': rpy})
    ctag('axis', {'xyz': '0 1 0'})
    ctag('parent', {'link': parent})
    ctag('child', {'link': child})
    ctag('limit', {'effort': 100, 'velocity': 100})
    etag('joint')

def inertial():
    stag('inertial')
    ctag('mass', {'value': 1})
    ctag('inertia', {'ixx': 1, 'ixy': 0, 'ixz':0, 'iyy':1, 'iyz':0, 'izz':1})
    etag('inertial')

def table():
    stag('link', {'name': 'table'})
    inertial()
    visualBox('black', 0, -(tableDepth+wall)/2, 0, tableWidth, wall, tableHeight)
    collisionBox(      0, -(tableDepth+wall)/2, 0, tableWidth, wall, tableHeight)
    visualBox('black', 0,  (tableDepth+wall)/2, 0, tableWidth, wall, tableHeight)
    collisionBox(      0,  (tableDepth+wall)/2, 0, tableWidth, wall, tableHeight)
    visualBox('black', -(tableWidth+wall)/2, 0, 0, wall, tableDepth + wall*2, tableHeight)
    collisionBox(      -(tableWidth+wall)/2, 0, 0, wall, tableDepth + wall*2, tableHeight)
    visualBox('black',  (tableWidth+wall)/2, 0, 0, wall, tableDepth + wall*2, tableHeight)
    collisionBox(       (tableWidth+wall)/2, 0, 0, wall, tableDepth + wall*2, tableHeight)
    etag('link')
    stag('link', {'name': 'floor'})
    inertial()
    visualBox('green', 0, 0, -(tableHeight+wall)/2, tableWidth+wall*2, tableDepth+wall*2, wall)
    collisionBox(      0, 0, -(tableHeight+wall)/2, tableWidth+wall*2, tableDepth+wall*2, wall)
    etag('link')
    fixedJoint('floor_joint', 'table', 'floor')

def man(rodIndex, manIndex, color, xOffset, yOffset):
    stag('link', {'name': f'rod{rodIndex}_man{manIndex}'})
    inertial()
    visualBox(color, 0, 0, -manOffset, manDepth, manWidth, manHeight)
    collisionBox(       0, 0, -manOffset, manDepth, manWidth, manHeight)
    etag('link')
    if manIndex == 0:
        continuousJoint(f'rod{rodIndex}_man{manIndex}_joint', f'rod{rodIndex}', f'rod{rodIndex}_man{manIndex}', xOffset, yOffset)
    else:
        fixedJoint(f'rod{rodIndex}_man{manIndex}_joint', f'rod{rodIndex}_man0', f'rod{rodIndex}_man{manIndex}', 0, yOffset)

def rod(index, color, xOffset, manCount, manDistance):
    stag('link', {'name': f'rod{index}'})
    inertial()
    visualCylinder('silver', xOffset, 0, 0, rodDiameter, rodLength, f'{math.pi/2:f} 0 0')
    etag('link')
    prismaticJoint(f'rod{index}_joint', 'table', f'rod{index}')
    yOffset = -manDistance * (manCount-1) / 2
    man(index, 0, color, xOffset, yOffset)
    for manIndex in range(1, manCount):
        man(index, manIndex, color, xOffset, manDistance * manIndex)

import sys

orig_stdout = sys.stdout
f = open('FoosballTable.urdf', 'w')
sys.stdout = f

stag('robot', {'name': 'foosball_table'})
material('black', '0.1 0.1 0.1 1.0')
material('green', '0.1 0.4 0.1 1.0')
material('silver','0.5 0.5 0.5 1.0')
material('yellow','0.9 0.9 0.1 1.0')
table()
goalieDistance =   8.125*metersPerInch
twomanDistance =   9.500*metersPerInch
fivebarDistance =  4.750*metersPerInch
threemanDistance = 7.250*metersPerInch
rod(1, 'yellow', rodDistance * -3.5, 3, goalieDistance)
rod(2, 'yellow', rodDistance * -2.5, 2, twomanDistance)
rod(3, 'black',  rodDistance * -1.5, 3, threemanDistance)
rod(4, 'yellow', rodDistance * -0.5, 5, fivebarDistance)
rod(5, 'black',  rodDistance *  0.5, 5, fivebarDistance)
rod(6, 'yellow', rodDistance *  1.5, 3, threemanDistance)
rod(7, 'black',  rodDistance *  2.5, 2, twomanDistance)
rod(8, 'black',  rodDistance *  3.5, 3, goalieDistance)
etag('robot')

sys.stdout = orig_stdout
f.close()