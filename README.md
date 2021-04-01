# About
This repo consists of several (probably seperable) parts:

1. gym - A Foosball OpenAI style gym for training agents
2. train - A few sample scripts for training agents using stable-baselines3
3. motion - A custom motion controller for a real foosball table
4. 3d_models - 3D models and a BOM for automating a tornado foosball table
5. control - Scripts for using Raspberry Pi to capture the ball position (and eventually run the agent)

This repository is designed to be used with the following software:

1. Microsoft Windows 10 PC
    1. Preferably with an NVidia GPU and CUDA
2. Microsoft VS Code
    1. PlatformIO IDE Extension
3. Python 3.8 for Windows

# Training Agents using the Open AI Gym
See [train/README.md](./train/README.md)
