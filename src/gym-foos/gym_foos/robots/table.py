# https://usermanual.wiki/Document/pybullet20quickstart20guide.479068914/html
# http://wiki.ros.org/pr2_controller_manager/safety_limits

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
        ball_pos = np.random.uniform(-.25,.25)
        self.ball = p.loadURDF(fileName=f_name,
                                basePosition=[-.05, ball_pos, 0.125],
                                physicsClientId=client)

        self.tran_joints = [1,5,8,12,18,24,28,31]
        self.rot_joints =  [2,6,9,13,19,25,29,32]
        self.rods = [[0,1,3,5],[7,6,4,2]]
        self.last_collision = None

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
    
    def apply_action(self, player, action):
        action = np.reshape(action, [4,2])
        rods = self.rods[player-1]
        for rod in range(4):
            tran,rot=action[rod]
            rod_idx=rods[rod]
            self.apply_rod_action(rod_idx,tran,rot)

    def apply_rod_action(self,rod,tran,rot):
        p.setJointMotorControl2(self.table, self.tran_joints[rod],
                            p.POSITION_CONTROL,
                            targetPosition=self.tran_limits[rod]*tran,
                            maxVelocity=0.5,
                            physicsClientId=self.client)
        p.setJointMotorControl2(self.table, self.rot_joints[rod],
                            p.POSITION_CONTROL,
                            targetPosition=3.14*rot,
                            maxVelocity=5,
                            physicsClientId=self.client)

    def get_rod_observation(self,rod):
        tran_obs = p.getJointState(self.table, self.tran_joints[rod], physicsClientId=self.client)
        rot_obs = p.getJointState(self.table, self.rot_joints[rod], physicsClientId=self.client)        
        return (tran_obs[0], tran_obs[1]/0.5, rot_obs[0], rot_obs[1]/5)

    def get_rod_observations(self, player):
        rods=self.rods[player-1]
        obs=()
        for rod in range(4):
            obs = obs + self.get_rod_observation(rods[rod])
        return obs

    def get_ball_observations(self, player):
        pos, ang = p.getBasePositionAndOrientation(self.ball,self.client)
        vel = p.getBaseVelocity(self.ball,self.client)[0]
        pos = (pos[0] / .59, pos[1] / .324)
        vel = (vel[0] / .59, vel[1] / .324)

        if player==2:
            pos = (pos[0],-pos[1])
            vel = (vel[0],-vel[1])

        return (pos+vel)

    def get_observation(self, player):
        ball = self.get_ball_observations(player)
        rods = self.get_rod_observations(player)
        return (ball+rods)

    def get_rewards(self):
        ball_ob = self.get_ball_observations(player=1)

        # Width of goal, and distance from 
        goal_width = 0.4
        goal_offset = .02
        reward = 0

        x,y,vx,vy=ball_ob[:4]
        goal = (x > (1-goal_offset) and y > (-goal_width/2) and y < (0.5+goal_width/2))
        loss = (x < (-1+goal_offset) and y > (-goal_width/2) and y < (0.5+goal_width/2))

        ball_collisions = p.getContactPoints(self.ball, physicsClientId=self.client)
        rods=[3,2,3,5,5,3,2,3]
        rodp=[1,1,2,1,2,1,2,2]

        fwd_pass = 0
        lateral_pass = 0

        for c in ball_collisions:
            if c[4] > 0:
                man = c[4]-2
                rod = 0

                while man >= rods[rod]:
                    man = man - (rods[rod]+1)
                    rod = rod + 1

                collision = (rodp[rod],rod,man)
                if self.last_collision != collision:
                    if collision[0] == 1:
                        if self.last_collision != None and collision[1] > self.last_collision[1]:
                            fwd_pass = 1
                        else:
                            lateral_pass = 1
                    
                    #print("last=",self.last_collision,"collision=",collision,fwd_pass,lateral_pass)
                    self.last_collision = collision

        return goal,loss,lateral_pass,fwd_pass

