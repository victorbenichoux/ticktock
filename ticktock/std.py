from typing import Dict

from ticktock.data import AggregateTimes
from ticktock.utils import format_ns_interval


class StandardRenderer:
    def render(self, render_data: Dict[str, Dict[str, AggregateTimes]]):
        ls = []
        for clock_name, clock_data in render_data.items():
            for line in StandardRenderer.render_clock(clock_name, clock_data):
                ls.append(line)
        print("\n".join(ls))

    def render_clock(clock_name, clock_data: Dict[str, AggregateTimes]):
        for tick_key, times in clock_data.items():
            yield (
                f"⏱️ {clock_name} [{tick_key}] "
                f"avg = {format_ns_interval(times.avg_time_ns)}, "
                f"last = {format_ns_interval(times.last_time_ns())}, "
                f"n = {times.n_periods}"
            )
