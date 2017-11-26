class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, initial=0.0):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._accumulator = 0.0
        self._prev = initial

    def filter(self, value: float) -> float:
        self._accumulator += value
        result = self._kp*value + self._ki*self._accumulator + self._kd*(value - self._prev)
        self._prev = value
        return result


class AverageFilter:
    def __init__(self, n):
        self._n = n
        self._values = []

    @property
    def n(self):
        return self._n

    def next_value(self, value: float):
        self._values = [value] + self._values

        if len(self._values) > self._n:
            self._values = self._values[0:len(self._values)-1]

        return sum(self._values)/len(self._values)