import gym
import gym_foos
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
import os

if __name__ == "__main__":
    log_dir='./log'
    os.makedirs(log_dir, exist_ok=True)

    opponent = PPO.load("trial2/sessions/148/best_model.zip")
    env = gym.make('Foos-v0',opponent=opponent)

    model = PPO(MlpPolicy, env, verbose=1)
    model.load("trial2/sessions/148/best_model.zip")

    total_reward = 0.0
    total_steps = 0
    obs = env.reset()

    while True:
        env.render()
        #action = env.action_space.sample()
        action, _states = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        total_steps += 1
        if done:
            break

    print("Episode done in %d steps, total reward %.2f" % (total_steps, total_reward))
    env.close()