from gym.envs.registration import register

register(id='Foos-v0',
         entry_point='gym_foos.envs:FoosEnv')