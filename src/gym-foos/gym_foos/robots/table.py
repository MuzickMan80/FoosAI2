import pybullet as p
import numpy as np
import os

class Table:
    def __init__(self, client):
        self.client = client
        f_name = os.path.join(os.path.dirname(__file__),'../assets/FoosballTable2.urdf')
        self.table = p.loadURDF(fileName=f_name,
                                basePosition=[0, 0, 0.1],
                                physicsClientId=client,
                                useFixedBase=1)
        f_name = os.path.join(os.path.dirname(__file__),'../assets/FoosballBall.urdf')
        self.ball = p.loadURDF(fileName=f_name,
                                basePosition=[-.05, 0, 0.15],
                                physicsClientId=client)

        self.tran_joints = [1,5,8,12,18,24,28,31]
        self.rot_joints =  [2,6,9,13,19,25,29,32]

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

        self.tran_limits = [ tran_limit(3, goalieDistance),
                             tran_limit(2, twomanDistance),
                             tran_limit(3, threemanDistance),
                             tran_limit(5, fivebarDistance),
                             tran_limit(5, fivebarDistance),
                             tran_limit(3, threemanDistance),
                             tran_limit(2, twomanDistance),
                             tran_limit(3, goalieDistance) ]

    def get_ids(self):
        return self.client, self.table, self.ball
    
    def apply_action(self, action):
        agent1_action = np.reshape(action, [4,2])
        agent2_action = [[0,-1],[0,-1],[0,-1],[0,-1]]
        agent1_rod_indices=[0,1,3,5]
        agent2_rod_indices=[7,6,4,2]

        for rod in range(4):
            tran,rot=agent1_action[rod]
            rod_idx=agent1_rod_indices[rod]
            self.apply_rod_action(rod_idx,tran,rot)

            tran,rot=agent2_action[rod]
            rod_idx=agent2_rod_indices[rod]
            self.apply_rod_action(rod_idx,tran,rot)

    def apply_rod_action(self,rod,tran,rot):
        p.setJointMotorControl2(self.table, self.tran_joints[rod],
                            p.POSITION_CONTROL,
                            targetPosition=self.tran_limits[rod]*tran,
                            maxVelocity=0.5)
        p.setJointMotorControl2(self.table, self.rot_joints[rod],
                            p.POSITION_CONTROL,
                            targetPosition=3.14*rot,
                            maxVelocity=5)

    def get_observation(self):
        pos, ang = p.getBasePositionAndOrientation(self.ball,self.client)
        vel = p.getBaseVelocity(self.ball,self.client)[0]
        pos = (pos[0] / .59, pos[1] / .324)
        vel = (vel[0] / .59, vel[1] / .324)
        return (pos+vel)