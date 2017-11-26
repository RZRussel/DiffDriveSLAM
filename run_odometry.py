from ev3dev import ev3
from odometry import Odometry
from math import pi

odometry = Odometry(ev3.LargeMotor("outB"),
                    ev3.LargeMotor("outC"),
                    6.0,
                    2.7,
                    6.0,
           2 * pi / 5.0)
odometry.drive_to(-30.0, 0.0, 0)
odometry.drive_to(-30.0, 30.0, 0)
odometry.drive_to(-60.0, 60.0, pi)