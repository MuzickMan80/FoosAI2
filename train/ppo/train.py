import gym
import gym_foos
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name of the training session')

    args = parser.parse_args()
    name = args.name

    log_dir=f'./log'
    os.makedirs(log_dir, exist_ok=True)

    env = gym.make('Foos-v0')
    env.reset()

    eval_env = gym.make('Foos-v0')
    eval_env = Monitor(eval_env, log_dir)
    eval_env.reset()

    model = PPO(MlpPolicy, env, verbose=1, tensorboard_log=f"tb", 
      batch_size=4*1024, n_steps=16*1024, learning_rate=3e-4)
    #model = PPO.load(f"./{trial}/sessions/85/final_model", tensorboard_log=f"{trial}/tb")
    model.set_env(env)

    for i in range(1,1000):
        eval_callback = EvalCallback(eval_env, 
                                    best_model_save_path=f'./{name}/{i}/',
                                    log_path=f'./{name}/{i}/', render=True)
        model.learn(total_timesteps=1e5, callback=eval_callback, reset_num_timesteps=False, tb_log_name=name)
        model.save(f"./{name}/{i}/final_model")

        env.close()

        env = gym.make('Foos-v0', opponent=PPO.load(f"./{name}/{i}/final_model"))
        model.set_env(env)
        env.reset()

        eval_env.close()
            
        eval_env = gym.make('Foos-v0')
        eval_env = Monitor(eval_env, log_dir)
        eval_env.reset()