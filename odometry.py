from math import atan2, sqrt, pi, fabs, cos, sin
from ev3dev.ev3 import *
from time import sleep


class Odometry:
    def __init__(self,
                 left_motor: LargeMotor,
                 right_motor: LargeMotor,
                 wheel_base_half: float,
                 wheel_radius: float,
                 v: float,
                 w: float,
                 x: float=0.0,
                 y: float=0.0,
                 theta: float=0.0):
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._wheel_base_half = wheel_base_half
        self._wheel_radius = wheel_radius
        self._x = x
        self._y = y
        self._theta = theta
        self._w = w
        self._v = v

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def theta(self) -> float:
        return self._theta

    def start_driving(self, angle: float, dt: float):
        w = angle / dt

        v, w = self._drive(self._v, w)

        self._x = self._x + v*dt*cos(self._theta + w * dt)
        self._y = self._y + v*dt*sin(self._theta + w * dt)
        self._theta = self._theta + angle

    def stop_driving(self):
        self._stop_motors()

    def autonomous_rotation(self, src_angle_offset: float, distance: float, target_angle_offset: float):
        alpha = self.theta + src_angle_offset

        new_x = self._x + distance*cos(alpha)
        new_y = self._y + distance*sin(alpha)
        new_theta = alpha + target_angle_offset

        self.drive_to(new_x, new_y, new_theta)

    def drive_to(self, new_x: float, new_y: float, new_theta: float):
        alpha = atan2(new_y - self._y, new_x - self._x)
        beta = alpha - self._theta

        dt = fabs(beta / self._w)

        if beta >= 0:
            w = self._w
        else:
            w = -self._w

        self._drive_while(0.0, w, dt)
        sleep(dt)

        distance = sqrt((new_x - self._x) ** 2 + (new_y - self._y) ** 2)

        dt = distance / self._v
        self._drive_while(self._v, 0.0, dt)
        sleep(dt)

        gamma = new_theta - alpha
        dt = fabs(gamma / self._w)

        if gamma >= 0:
            w = self._w
        else:
            w = -self._w

        self._drive_while(0.0, w, dt)
        sleep(dt)

        self._x = new_x
        self._y = new_y
        self._theta = new_theta

    def _drive_while(self, v: float, w: float, dt: float):
        wl = (v - w * self._wheel_base_half) / self._wheel_radius
        wr = (v + w * self._wheel_base_half) / self._wheel_radius

        wl = wl * self._left_motor.count_per_rot / (2 * pi)
        wr = wr * self._right_motor.count_per_rot / (2 * pi)

        self._drive_rel_pos(wl, wr, dt)

    def _drive(self, v: float, w: float):
        wl = (v - w * self._wheel_base_half) / self._wheel_radius
        wr = (v + w * self._wheel_base_half) / self._wheel_radius

        wl = wl * self._left_motor.count_per_rot / (2 * pi)
        wr = wr * self._right_motor.count_per_rot / (2 * pi)

        wl = self._restrict_motor(wl)
        wr = self._restrict_motor(wr)

        self._drive_forever(wl, wr)

        return self.wheel_speed_to_linear_and_angular(wl, wr)

    def _drive_rel_pos(self, wl: float, wr: float, dt: float):
        self._left_motor.speed_sp = wl
        self._left_motor.run_to_rel_pos(position_sp=wl * dt)

        self._right_motor.speed_sp = wr
        self._right_motor.run_to_rel_pos(position_sp=wr * dt)

    def _drive_forever(self, wl: float, wr: float):
        self._left_motor.run_forever(speed_sp=wl)
        self._right_motor.run_forever(speed_sp=wr)

    def _stop_motors(self):
        self._left_motor.stop()
        self._right_motor.stop()

    def wheel_speed_to_linear_and_angular(self, wl: float, wr: float):
        wl_to_ang = wl * 2.0 * pi / self._left_motor.count_per_rot
        wr_to_ang = wr * 2.0 * pi / self._right_motor.count_per_rot
        return (wl_to_ang + wr_to_ang)*self._wheel_radius / 2.0,\
               (wr_to_ang - wl_to_ang) * self._wheel_radius / (2.0 * self._wheel_base_half)

    K_MAX_MOTOR = 960

    def _restrict_motor(self, value):
        if value > self.K_MAX_MOTOR:
            return self.K_MAX_MOTOR

        if value < -self.K_MAX_MOTOR:
            return -self.K_MAX_MOTOR

        return value
