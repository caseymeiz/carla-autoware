import carla
import subprocess

import numpy as np
import yaml
import pandas as pd
import time
import os
import signal
LOCATIONS_TO_ATTEMPT = 10
SAMPLES_TO_COLLECT = 10

def time_difference_milliseconds(t1_sec, t1_nsec, t2_sec, t2_nsec):
    # Convert both timestamps to nanoseconds
    t1_total_nsec = t1_sec * 10**9 + t1_nsec
    t2_total_nsec = t2_sec * 10**9 + t2_nsec

    # Calculate the difference in nanoseconds
    diff_nsec = abs(t2_total_nsec - t1_total_nsec)

    # Convert the difference to milliseconds
    diff_msec = diff_nsec / 10**6

    return diff_msec

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

cmd1 = "roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 x:={x} y:={y} z:={z} pitch:={pitch} yaw:={yaw} roll:={roll} > /dev/null 2>&1 &"
latencies = list()
for i, sp in pd.read_csv('/home/autoware/carla-autoware/stuff/spawn_points.csv').iloc[:LOCATIONS_TO_ATTEMPT].iterrows():
    try:
        print(i)
        autoware_ros = subprocess.Popen(cmd1.format(x=sp.x, y=sp.y, z=sp.z, pitch=sp.pitch, yaw=sp.yaw, roll=sp.roll), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        time.sleep(10)
        world = client.get_world()

        vehicle = world.get_actors().filter('*vehicle*')[0]
        vehicle_transform = vehicle.get_transform()
        result = subprocess.check_output(['rostopic', 'echo', '-n', str(SAMPLES_TO_COLLECT), '/current_pose'])
        sample_texts = result.split('---')[:-1]
        samples = [yaml.safe_load(sample_text) for sample_text in sample_texts]
        start = samples[0]
        end = samples[-1]

        get_sec = lambda t: t['header']['stamp']['secs']
        get_nsec = lambda t: t['header']['stamp']['nsecs']

        latency = time_difference_milliseconds(get_sec(start), get_nsec(start), get_sec(end), get_nsec(end))

        latencies.append(latency/SAMPLES_TO_COLLECT)
    except Exception as e:
        print("Unable to process location", i)
    finally:
        os.killpg(os.getpgid(autoware_ros.pid), signal.SIGTERM)
        time.sleep(2)



print("Localization Latency:", np.average(latencies))
