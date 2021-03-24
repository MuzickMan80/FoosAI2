


## Setting up the Raspberry Pi
apt-get install libatlas-base-dev libhdf5-dev
pip3 install opencv-contrib-python
pip3 install opencv-python (maybe not needed)
sudo rmmod uvcvideo
sudo modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80
