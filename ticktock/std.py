from typing import Dict

from ticktock.data import AggregateTimes
from ticktock.utils import format_ns_interval


class StandardRenderer:
    def render(self, render_data: Dict[str, Dict[str, AggregateTimes]]):
        print(f"# {len(render_data)} clocks")
        for clock_name, clock_data in render_data.items():
            for tick_key, times in clock_data.items():
                print(
                    f"{clock_name} [{tick_key}] "
                    f"avg = {format_ns_interval(times.avg_time_ns)}, "
                    f"last = {format_ns_interval(times.last_time_ns())}, "
                    f"n = {times.n_periods}"
                )
