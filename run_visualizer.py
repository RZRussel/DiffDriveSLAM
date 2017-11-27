import matplotlib.pyplot as plt
import csv

path = "resources/map.csv"

robot = []
env_map = []

with open(path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ')

    for row in csv_reader:
        robot.append((float(row[0]), float(row[1])))
        env_map.append((float(row[3]), float(row[4])))
        env_map.append((float(row[5]), float(row[6])))

robot = sorted(robot, key=lambda x: x[0])
env_map = sorted(env_map, key=lambda x: x[0])

robot_x = list(map(lambda pair: pair[0], robot))
robot_y = list(map(lambda pair: pair[1], robot))

map_x = list(map(lambda pair: pair[0], env_map))
map_y = list(map(lambda pair: pair[1], env_map))

plt.plot(robot_x, robot_y, 'go', label="robot's path")
plt.plot(map_x, map_y, 'ro', label="obstacles")

plt.legend(loc='upper right')
plt.show()
