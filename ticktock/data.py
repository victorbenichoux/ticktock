import math
from dataclasses import dataclass
from typing import Union

from ticktock.utils import _TockName


@dataclass
class AggregateTimes:
    tock_name: Union[str, _TockName]
    tock_filename: str
    tock_line: int

    avg_time_ns: float
    min_time_ns: float
    max_time_ns: float
    last_time_ns: float
    std_time_ns: float = 0
    _m2_time_ns: float = 0

    count: int = 1

    def update(self, tock_time_ns: int, tick_time_ns: int) -> None:

        self.last_time_ns = tock_time_ns - tick_time_ns

        self.count += 1
        self.max_time_ns = max(self.last_time_ns, self.max_time_ns or -math.inf)
        self.min_time_ns = min(self.last_time_ns, self.min_time_ns or math.inf)

        delta = self.last_time_ns - self.avg_time_ns
        self.avg_time_ns += delta / self.count

        delta2 = self.last_time_ns - self.avg_time_ns
        self._m2_time_ns += delta * delta2

        if self.count >= 2:
            self.std_time_ns = math.sqrt(self._m2_time_ns / (self.count - 1))
