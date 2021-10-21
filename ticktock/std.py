from typing import Callable, Dict

from ticktock.data import AggregateTimes
from ticktock.utils import format_ns_interval

UP: Callable[[int], str] = lambda x: f"\x1B[{x}A" if x else ""
CLR = "\x1B[0K"


class StandardRenderer:
    def __init__(self) -> None:
        self._has_printed = 0

    def render(self, render_data: Dict[str, Dict[str, AggregateTimes]]):
        ls = []
        for clock_name, clock_data in render_data.items():
            for line in StandardRenderer.render_clock(clock_name, clock_data):
                ls.append(line)
        print(UP(self._has_printed) + CLR + f"\n{CLR}".join(ls))
        self._has_printed = len(ls)

    @staticmethod
    def render_clock(clock_name: str, clock_data: Dict[str, AggregateTimes]):
        for tick_key, times in clock_data.items():
            yield (
                CLR + f"⏱️ {clock_name} [{tick_key}] "
                f"{format_ns_interval(times.avg_time_ns)} "
                f"({format_ns_interval(times.std_time_ns)} std), "
                f"min = {format_ns_interval(times.min_time_ns)}, "
                f"max = {format_ns_interval(times.max_time_ns)}, "
                f"last = {format_ns_interval(times.last_time_ns())}, "
                f"count = {times.n_periods}"
            )
