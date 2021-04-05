
# Training Agents using the Open AI Gym
1. Create virtual environment
    * python -m venv foos_env
2. Activate the virtual environment
    * foos_env/Scripts/activate.bat
3. Install the gym
    * pip install -e gym/gym-foos
4. Install training dependencies
    * git clone --recursive https://github.com/DLR-RM/rl-baselines3-zoo
    * uncomment gSDE lines in rl-baselines3-zoo/utils/hyperparams_opt.py
    * pip install -r rl-baselines3-zoo/requirements.txt
5. Tune the hyperparameters for training
    * python train.py --algo ppo --env Foos-v0 -n 50000 -optimize --n-trials 1000 --sampler tpe --pruner median
6. Train and enjoy