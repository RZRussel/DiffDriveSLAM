from odometry import Odometry
from controller import WheeledRobotController
from math import pi
from ev3dev import ev3
from logger import Logger

odometry = Odometry(ev3.LargeMotor("outB"),
                    ev3.LargeMotor("outC"),
                    6.0,
                    2.7,
                    10.0,
                    2 * pi / 5.0)

controller = WheeledRobotController(ev3.UltrasonicSensor("in2"),
                                    ev3.UltrasonicSensor("in1"),
                                    ev3.UltrasonicSensor("in3"),
                                    odometry)

logger = Logger("resources/map.csv")
controller.run_closed_loop(kp=0.025,
                           ki=0.0,
                           kd=0.01,
                           avg_n=3,
                           stop_threshold=5.0,
                           logger=logger,
                           delta=0.1)
logger.complete()
