from ev3dev.ev3 import UltrasonicSensor
from odometry import Odometry
from filters import PIDController, AverageFilter
from math import atan2, cos, sin, pi
from time import sleep
from logger import Logger


class WheeledRobotController:
    def __init__(self, left_sonar: UltrasonicSensor,
                 right_sonar: UltrasonicSensor,
                 center_sonar: UltrasonicSensor,
                 odometry: Odometry):
        self._left_sonar = left_sonar
        self._right_sonar = right_sonar
        self._center_sonar = center_sonar
        self._odometry = odometry

    @property
    def odometry(self):
        return self._odometry

    def run_closed_loop(self,
                        kp: float,
                        ki: float,
                        kd: float,
                        avg_n: float,
                        stop_threshold: float,
                        logger: Logger = None,
                        delta: float = 0.1):
        pid = PIDController(kp, ki, kd)

        left_filter = AverageFilter(avg_n)
        right_filter = AverageFilter(avg_n)
        center_filter = AverageFilter(avg_n)

        while True:
            left_distance = left_filter.next_value(self._left_sonar.distance_centimeters)
            right_distance = right_filter.next_value(self._right_sonar.distance_centimeters)
            center_distance = center_filter.next_value(self._center_sonar.distance_centimeters)

            if logger is not None:
                left_mx, left_my = self._occupied_from(self._odometry.x,
                                                       self.odometry.y,
                                                       self._odometry.theta,
                                                       pi / 2.0,
                                                       left_distance)

                right_mx, right_my = self._occupied_from(self._odometry.x,
                                                         self.odometry.y,
                                                         self._odometry.theta,
                                                         -pi / 2.0,
                                                         right_distance)

                logger.log([self._odometry.x,
                            self._odometry.y,
                            self._odometry.theta,
                            left_mx,
                            left_my,
                            right_mx,
                            right_my])

            if center_distance < stop_threshold:
                break

            err = atan2(left_distance - right_distance, 1.0)

            angle = pid.filter(err)

            self._odometry.start_driving(angle, delta)
            sleep(delta)

    @staticmethod
    def _occupied_from(x: float, y: float, theta: float, sonar_angle: float, distance: float) -> (float, float):
        occupied_x = x + distance*cos(sonar_angle + theta)
        occupied_y = y + distance*sin(sonar_angle + theta)

        return occupied_x, occupied_y
