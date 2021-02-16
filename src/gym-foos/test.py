import gym
import gym_foos
from stable_baselines3 import TD3
from stable_baselines3.td3 import MlpPolicy
from stable_baselines3.common.monitor import Monitor
import os

if __name__ == "__main__":
    log_dir='./log'
    os.makedirs(log_dir, exist_ok=True)

    env = gym.make('Foos-v0')
    env = Monitor(env, log_dir)

    model = TD3(MlpPolicy, env, verbose=1, tensorboard_log="td3")
    model.learn(total_timesteps=1e6)
    model.save("ppo_foos")

    total_reward = 0.0
    total_steps = 0
    obs = env.reset()

    while True:
        env.render()
        action, _states = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        total_steps += 1
        if done:
            break

    print("Episode done in %d steps, total reward %.2f" % (total_steps, total_reward))
    env.close()