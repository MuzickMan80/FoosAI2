import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import pybullet as p
from gym_foos.robots.table import Table
from gym_foos.opponents.constant_spin import DefaultOpponent
import matplotlib.pyplot as plt

class FoosEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, opponent=DefaultOpponent(), goal_reward=1, loss_reward=-1,pass_reward=.01,fwd_pass_reward=.1):
    # Action space is the target rotation and translation 
    # position of each rod controlled by the player
    self.action_space = gym.spaces.box.Box(
      low=np.array([-1,-1,-1,-1,-1,-1,-1,-1], dtype=np.float32),
      high=np.array([1,1,1,1,1,1,1,1], dtype=np.float32)
    )

    # Observation space is the x,y location of the ball
    # and x,y velocity of the ball
    self.observation_space = gym.spaces.box.Box(
      low=np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], dtype=np.float32),
      high=np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=np.float32),
    )

    self.opponent = opponent
    self.goal_reward = goal_reward
    self.loss_reward = loss_reward
    self.pass_reward = pass_reward
    self.fwd_pass_reward = fwd_pass_reward

    self.n_agents=2
    self.np_random, _ = gym.utils.seeding.np_random()

    self.client = p.connect(p.DIRECT)
    self.reset()

  def step(self, action):
    self.table.apply_action(1,action)
    
    opponent_ob = self.table.get_observation(player=2)
    opponent_ob = np.array(opponent_ob, dtype=np.float32)
    opponent_action, _states = self.opponent.predict(opponent_ob)
    self.table.apply_action(player=2,action=opponent_action)

    p.stepSimulation(physicsClientId=self.client)

    ball_ob = self.table.get_observation(player=1)
    ob = np.array(ball_ob, dtype=np.float32)
    goal,loss,lateral_pass,forward_pass = self.table.get_rewards()
    reward = goal*self.goal_reward + loss*self.loss_reward + lateral_pass*self.pass_reward + forward_pass*self.fwd_pass_reward

    self.step_count = self.step_count+1
    print(self.step_count)
    if self.step_count >= 500 or goal or loss:
      self.done = True
    
    return ob, reward, self.done, dict()

  def reset(self):
    p.resetSimulation(physicsClientId=self.client)
    p.setTimeStep(1/30, physicsClientId=self.client)
    p.setGravity(0,0,-10, physicsClientId=self.client)
    self.table = Table(self.client)
    self.done = False
    self.step_count = 0
    self.rendered_img = None
    return np.array(self.table.get_observation(player=1), dtype=np.float32)

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

    frame = p.getCameraImage(im_width,im_height,view_matrix,proj_matrix,physicsClientId=self.client)[2]
    frame = np.reshape(frame,(im_height,im_width,4))
    self.rendered_img.set_data(frame)
    plt.draw()
    plt.waitforbuttonpress(.03)

  def close(self):
    p.disconnect(self.client)

  def seed(self, seed=None):
    self.np_random, seed = gym.utils.seeding.np_random(seed)
    return [seed]