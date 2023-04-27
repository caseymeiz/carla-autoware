# Carla Autoware Benchmarks

This is a fork of the repo [link](https://github.com/carla-simulator/carla-autoware).

In this project we are looking at running Autoware in the Carla simulator and collecting accuracy and latency metrics on components of the Autoware autonoums driving stack.


## Prerequisite 

### Carla

Before we run the scripts lets make sure we can get carla up and running using a docker container. 
Use the instructions [here](./CARLA.md) and change the version to `0.9.10.1` that is the version that we have this working on / point maps.

Current specs I am using:
* AMD Ryzen™ 9 7950X 16-Core
* Nvidia 4080 GPU 16GB
* Ubuntu 22.04.2 LTS
* 32 GB RAM

Once this is running you should see a 3d visualization of a town, you can also move around in it.

You can now kill the container `docker ps` then find the `id` and then kill it `docker kill id_here`.

## Connect Carla and Autoware

The [main.sh](./main.sh) script will kill any docker containers and boot up carla and autoware and connect them together.

```shell
./main.sh
```

Now you are in the Autoware container.
The prompt should be something like `autoware@zebra:/home/autoware$ `. 

You can now run the following scripts.

#### Benchmarks 
Run these after you run the main.sh

The result will be printed to the console.

Note: there will be GUIs popping up and disappearing, ignore them

There are a set number of locations that the script collects from, those locations were collected with [this](./stuff/get_spawn_locations.py) script. It will attempt to collect from them but might skip over some if there are errors. 

#### Localization accuracy
```shell
python /home/autoware/carla-autoware/stuff/localization_error.py
```
You can see the script [here](./stuff/localization_error.py), if you make changes you have to rerun the main.sh.

This will run Autoware / ROS and spawn a car in the map and the collect the localization results by subscribing to the topic `/current_pose` then compare the current location to some ground truth collected from Carla.


#### Localization latency
```shell
python /home/autoware/carla-autoware/stuff/localization_latency.py
```
You can see the script [here](./stuff/localization_latency.py), if you make changes you have to rerun the main.sh.

This will run Autoware / ROS and spawn a car in the map and the collect the localization results by subscribing to the topic `/current_pose` then calculate how long it takes to publish the next pose on average.


