
import pybullet as p
import time
import pybullet_data
import GenerateFoosballTable

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,.08]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
p.resetDebugVisualizerCamera( cameraDistance=1, cameraYaw=88, cameraPitch=-90, cameraTargetPosition=cubeStartPos)
w,h,vm,pm = p.getDebugVisualizerCamera()
print(vm)
print(pm)

p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
boxId = p.loadURDF("assets/FoosballTable2.urdf",cubeStartPos, cubeStartOrientation, useFixedBase=1)
ball = p.loadURDF("assets/FoosballBall.urdf", [0,0,.12], cubeStartOrientation)

number_of_joints = p.getNumJoints(boxId)
for joint_number in range(number_of_joints):
    info = p.getJointInfo(boxId, joint_number)
    print(info)

tran_joints = [1,5,8,12,18,24,28,31]

metersPerInch = 0.0254
goalieDistance =   8.125*metersPerInch
twomanDistance =   9.500*metersPerInch
fivebarDistance =  4.750*metersPerInch
threemanDistance = 7.250*metersPerInch

def tran_limit(numMen, manDistance):
    tableDepth = 27 * metersPerInch
    manWidth = 1 * metersPerInch
    menWidth = (numMen - 1) * manDistance + manWidth
    return (tableDepth - menWidth) / 2

tran_limits = [ tran_limit(3, goalieDistance),
                tran_limit(2, twomanDistance),
                tran_limit(3, threemanDistance),
                tran_limit(5, fivebarDistance),
                tran_limit(5, fivebarDistance),
                tran_limit(3, threemanDistance),
                tran_limit(2, twomanDistance),
                tran_limit(3, goalieDistance) ]

rot_joints = [2,6,9,13,19,25,29,32]
for i in range (10000):
    if (i % 200) == 0:
        if (i % 400) == 0:
            for j in range(8):
                p.setJointMotorControl2(boxId, tran_joints[j],
                                    p.POSITION_CONTROL,
                                    targetPosition=-tran_limits[j])
                p.setJointMotorControl2(boxId, rot_joints[j],
                                    p.VELOCITY_CONTROL,
                                    targetVelocity=-25)
        else:
            for j in range(8):
                p.setJointMotorControl2(boxId, tran_joints[j],
                                    p.POSITION_CONTROL,
                                    targetPosition=tran_limits[j])
                p.setJointMotorControl2(boxId, rot_joints[j],
                                    p.VELOCITY_CONTROL,
                                    targetVelocity=25)

    p.stepSimulation()
    time.sleep(1./240.)
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)
p.disconnect()
