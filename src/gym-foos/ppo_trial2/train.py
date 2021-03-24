import gym
import gym_foos
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
import os

trial = "trial2"

if __name__ == "__main__":
    log_dir=f'./{trial}/log'
    os.makedirs(log_dir, exist_ok=True)

    env = gym.make('Foos-v0')
    env = Monitor(env, log_dir)
    env.reset()

    #model = PPO(MlpPolicy, env, verbose=1, tensorboard_log=f"{trial}/tb")
    model = PPO.load(f"./{trial}/sessions/85/final_model", tensorboard_log=f"{trial}/tb")
    model.set_env(env)

    for i in range(86,1000):
        eval_callback = EvalCallback(env, 
                                    best_model_save_path=f'./{trial}/sessions/{i}/',
                                    log_path=f'./{trial}/sessions/{i}/')
        model.learn(total_timesteps=1e5, callback=eval_callback, reset_num_timesteps=False)
        model.save(f"./{trial}/sessions/{i}/final_model")

        env.close()
        env = gym.make('Foos-v0', opponent=PPO.load(f"./{trial}/sessions/{i}/final_model"))
        env = Monitor(env, log_dir)
        model.set_env(env)
        env.reset()