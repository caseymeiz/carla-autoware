import carla
import subprocess
import yaml

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

world = client.get_world()
vehicle = world.get_actors().filter('*vehicle*')[0]


vehicle_transform = vehicle.get_transform()
print(vehicle_transform.location)

print(vehicle_transform.rotation)


clock = subprocess.check_output(['rostopic', 'echo', '-n', '1', '/clock'])
points_raw = subprocess.check_output(['rostopic', 'echo', '-n', '1', '/points_raw'])
pose = subprocess.check_output(['rostopic', 'echo', '-n', '1', '/current_pose'])

pose = pose[:pose.find("---")]
pose = yaml.safe_load(pose)

clock = clock[:clock.find("---")]
clock = yaml.safe_load(clock)

points_raw = points_raw[:points_raw.find("---")]
points_raw = yaml.safe_load(points_raw)


print(points_raw['header'])
print(pose['header'])
