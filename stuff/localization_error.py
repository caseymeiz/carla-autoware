import carla
import subprocess

import numpy as np
import yaml
import pandas as pd
import time
import os
import signal
import math

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

cmd1 = "roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 x:={x} y:={y} z:={z} pitch:={pitch} yaw:={yaw} roll:={roll} > /dev/null 2>&1 &"
errors = list()
for i, sp in pd.read_csv('/home/autoware/carla-autoware/stuff/spawn_points.csv').iloc[:10].iterrows():
    try:
        print(i)
        autoware_ros = subprocess.Popen(cmd1.format(x=sp.x, y=sp.y, z=sp.z, pitch=sp.pitch, yaw=sp.yaw, roll=sp.roll), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        time.sleep(10)
        world = client.get_world()

        vehicle = world.get_actors().filter('*vehicle*')[0]
        vehicle_transform = vehicle.get_transform()
        # print(vehicle_transform.location)
        result = subprocess.check_output(['rostopic', 'echo', '-n', '1', '/current_pose'])
        result = result[:result.find("---")]
        # print(yaml.safe_load(result)['pose']['position'])
        position = yaml.safe_load(result)['pose']['position']

        x1 = vehicle_transform.location.x
        y1 = vehicle_transform.location.y
        z1 = vehicle_transform.location.z

        x2 = position['x']
        y2 = position['y']
        z2 = position['z']

        error = math.sqrt((x1-x2)**2 + (-y1-y2)**2 + (z1-z2)**2)
        print(round(error, 3))
        errors.append(round(error, 3))
    except Exception as e:
        print("Unable to process location", i)
    finally:
        os.killpg(os.getpgid(autoware_ros.pid), signal.SIGTERM)
        time.sleep(2)


print(errors)
print("Localization Error:", np.average(errors))
