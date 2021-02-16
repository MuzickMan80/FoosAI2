import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import pybullet as p
from  gym_foos.robots.table import Table
import matplotlib.pyplot as plt

class FoosEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    # Action space is the target rotation and translation 
    # position of each rod controlled by the player
    self.action_space = gym.spaces.box.Box(
      low=np.array([-1,-1,-1,-1,-1,-1,-1,-1]),
      high=np.array([1,1,1,1,1,1,1,1])
    )

    # Observation space is the x,y location of the ball
    # and x,y velocity of the ball
    self.observation_space = gym.spaces.box.Box(
      low=np.array([-1,-1,-1,-1]),
      high=np.array([1,1,1,1])
    )
    self.n_agents=2
    self.np_random, _ = gym.utils.seeding.np_random()

    self.client = p.connect(p.DIRECT)
    p.setTimeStep(1/30, self.client)
    self.reset()

  def step(self, action):
    self.table.apply_action(action)
    p.stepSimulation()
    ball_ob = self.table.get_observation()

    # Width of goal, and distance from 
    goal_width = 0.4
    goal_offset = .02
    reward = 0

    x,y,vx,vy=ball_ob
    if (x > (1-goal_offset) and y > (-goal_width/2) and y < (0.5+goal_width/2)):
      self.done = True
      reward = 100
    
    if (x < (-1+goal_offset) and y > (-goal_width/2) and y < (0.5+goal_width/2)):
      self.done = True
      reward = -100

    self.step_count = self.step_count+1
    if self.step_count >= 200:
      self.done = True

    ob = np.array(ball_ob, dtype=np.float32)
    return ob, reward, self.done, dict()

  def reset(self):
    p.resetSimulation(self.client)
    p.setGravity(0,0,-10)
    self.table = Table(self.client)
    self.done = False
    self.step_count = 0
    self.rendered_img = None
    return np.array(self.table.get_observation(), dtype=np.float32)

  def render(self, mode='human'):
    im_width = 200
    im_height = 120
    im_fov = 40

    if self.rendered_img is None:
      self.rendered_img = plt.imshow(np.zeros((im_height,im_width,4)))

    proj_matrix = p.computeProjectionMatrixFOV(fov=im_fov, aspect=im_width/im_height,
                                                nearVal=0.01, farVal=100)
    tableStartPos = [0,0,.08]
    view_matrix = p.computeViewMatrixFromYawPitchRoll(
      yaw=0, pitch=-90, roll=0, upAxisIndex=2, distance=1, 
      cameraTargetPosition=tableStartPos)

    frame = p.getCameraImage(im_width,im_height,view_matrix,proj_matrix)[2]
    frame = np.reshape(frame,(im_height,im_width,4))
    self.rendered_img.set_data(frame)
    plt.draw()
    plt.pause(.00001)

  def close(self):
    p.disconnect(self.client)

  def seed(self, seed=None):
    self.np_random, seed = gym.utils.seeding.np_random(seed)
    return [seed]