
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
5. Tune the hyperparameters for training
6. Train and enjoy