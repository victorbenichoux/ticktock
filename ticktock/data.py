import math
from dataclasses import dataclass


@dataclass
class AggregateTimes:
    avg_time_ns: float
    min_time_ns: float
    max_time_ns: float
    last_tick_time_ns: float
    last_tock_time_ns: float

    n_periods: int = 1

    def last_time_ns(self):
        return self.last_tock_time_ns - self.last_tick_time_ns

    def update(self, tock_time_ns: int, tick_time_ns: int) -> None:
        self.last_tock_time_ns = tock_time_ns
        self.last_tick_time_ns = tick_time_ns
        last_time_ns: float = self.last_time_ns()

        self.n_periods += 1
        self.max_time_ns = max(last_time_ns, self.max_time_ns or -math.inf)
        self.min_time_ns = min(last_time_ns, self.min_time_ns or math.inf)
        self.avg_time_ns = (
            (self.avg_time_ns or 0) * (self.n_periods - 1) + last_time_ns
        ) / self.n_periods
