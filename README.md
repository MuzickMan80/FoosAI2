# About
This repo consists of several (probably seperable) parts:

1. gym - A Foosball OpenAI style gym for training agents
2. train - A few sample scripts for training agents using stable-baselines3
3. A custom motion controller for a real foosball table
4. 3D models and a BOM for automating a tornado foosball table
5. Scripts for using Raspberry Pi to capture the ball position (and eventually run the agent)

## Setting up the Raspberry Pi
apt-get install libatlas-base-dev libhdf5-dev
pip3 install opencv-contrib-python
pip3 install opencv-python (maybe not needed)
sudo rmmod uvcvideo
sudo modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80
