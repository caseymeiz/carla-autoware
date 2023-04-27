## CARLA Docker
Installation, follow these directions https://carla.readthedocs.io/en/latest/build_docker/
Use version 0.9.14
Might have to use `xhost +`
This section was helpful for nvidia issues https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit

Run the CARLA docker image
```shell
sudo docker run -p 2000-2002:2000-2002 --privileged --gpus all --net=host -e DISPLAY=$DISPLAY carlasim/carla:0.9.14 /bin/bash ./CarlaUE4.sh
```

## Setup Python CARLA Client
Install Python 3.8

```shell
sudo apt install python3.8
sudo apt install python3.8-venv
```

Create virtual environment 

```shell
python3.8 -m venv ./venv
```

Activate environment

```shell
source ./venv/bin/activate
```

Install dependencies 

```shell
pip install -r requirements.txt
```

## Spawn some cars, make them move, and save some images
https://carla.readthedocs.io/en/latest/tuto_first_steps/

Run with docker image and connect on port 2000