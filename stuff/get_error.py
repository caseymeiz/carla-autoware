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

result = subprocess.check_output(['rostopic', 'echo', '-n', '1', '/current_pose'])

result = result[:result.find("---")]

x = yaml.safe_load(result)

print(x)

