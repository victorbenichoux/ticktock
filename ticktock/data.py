import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class AggregateTimes:
    tock_name: str
    avg_time_ns: float
    min_time_ns: float
    max_time_ns: float
    last_tick_time_ns: float
    last_tock_time_ns: float
    last_time_ns: float
    std_time_ns: float = 0
    m2_time_ns: float = 0

    n_periods: int = 1

    def update(self, tock_time_ns: int, tick_time_ns: int) -> None:
        self.last_tock_time_ns = tock_time_ns
        self.last_tick_time_ns = tick_time_ns

        self.last_time_ns = tock_time_ns - tick_time_ns

        self.n_periods += 1
        self.max_time_ns = max(self.last_time_ns, self.max_time_ns or -math.inf)
        self.min_time_ns = min(self.last_time_ns, self.min_time_ns or math.inf)

        delta = self.last_time_ns - self.avg_time_ns
        self.avg_time_ns += delta / self.n_periods

        delta2 = self.last_time_ns - self.avg_time_ns
        self.m2_time_ns += delta * delta2

        if self.n_periods >= 2:
            self.std_time_ns = math.sqrt(self.m2_time_ns / (self.n_periods - 1))


@dataclass
class ClockData:
    times: Dict[str, AggregateTimes]
    tick_name: str
