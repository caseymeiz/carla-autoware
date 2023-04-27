import carla

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()


spawn_points = world.get_map().get_spawn_points()


with open('spawn_points.csv', 'w') as f:
    cols = ['x', 'y', 'z', 'pitch', 'yaw', 'roll']
    f.write(','.join(cols))
    f.write('\n')
    for sp in spawn_points:
        f.write(str(sp.location.x) + ',')
        f.write(str(sp.location.y) + ',')
        f.write(str(sp.location.z) + ',')
        f.write(str(sp.rotation.pitch) + ',')
        f.write(str(sp.rotation.yaw) + ',')
        f.write(str(sp.rotation.roll))
        f.write('\n')



