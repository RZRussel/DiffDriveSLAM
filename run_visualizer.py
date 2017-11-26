import matplotlib.pyplot as plt
import csv

path = "resources/map.csv"

robot = []
env_map = []

with open(path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ')

    for row in csv_reader:
        robot.append((row[0], row[1]))
        env_map.append((row[3], row[4]))
        env_map.append((row[5], row[6]))

robot = sorted(robot)
env_map = sorted(env_map)

robot_x = list(map(lambda pair: pair[0], robot))
robot_y = list(map(lambda pair: pair[1], robot))

map_x = list(map(lambda pair: pair[0], env_map))
map_y = list(map(lambda pair: pair[1], env_map))

plt.plot(robot_x, robot_y, 'g-', label="robot's path")
plt.plot(map_x, map_y, 'r-', label="map")

plt.legend(loc='upper right')
plt.show()
