import carla
import subprocess
import yaml
import pandas as pd
import time
import os
import signal

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

cmd1 = "roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 x:={x} y:={y} z:={z} pitch:={pitch} yaw:={yaw} roll:={roll} > /dev/null 2>&1 &"

for i, sp in pd.read_csv('spawn_points.csv').iloc[:2].iterrows():
    autoware_ros = subprocess.Popen(cmd1.format(x=sp.x, y=sp.y, z=sp.z, pitch=sp.pitch, yaw=sp.yaw, roll=sp.roll), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    time.sleep(10)

    world = client.get_world()
    vehicle = world.get_actors().filter('*vehicle*')[0]
    vehicle_transform = vehicle.get_transform()
    print(vehicle_transform.location)
    result = subprocess.check_output(['rostopic', 'echo', '-n', '1', '/current_pose'])
    result = result[:result.find("---")]
    print(yaml.safe_load(result)['pose']['position'])

    time.sleep(5)
    os.killpg(os.getpgid(autoware_ros.pid), signal.SIGTERM)
    time.sleep(5)
