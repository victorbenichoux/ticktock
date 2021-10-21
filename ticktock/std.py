from string import Formatter
from typing import Callable, Dict, Iterable, List, Optional

from ticktock.config import CURRENT_CONFIGURATION
from ticktock.data import AggregateTimes
from ticktock.utils import format_ns_interval

UP: Callable[[int], str] = lambda x: f"\x1B[{x}A" if x else ""
CLR = "\x1B[0K"

FIELDS = {
    "mean": lambda times: format_ns_interval(times.avg_time_ns),
    "std": lambda times: format_ns_interval(times.std_time_ns),
    "min": lambda times: format_ns_interval(times.min_time_ns),
    "max": lambda times: format_ns_interval(times.max_time_ns),
    "last": lambda times: format_ns_interval(times.last_time_ns),
    "count": lambda times: format_ns_interval(times.n_periods),
}


class StandardRenderer:
    def __init__(self, format: Optional[str] = None) -> None:
        self._format: str = format or CURRENT_CONFIGURATION.get("DEFAULT_FORMAT")
        self._fields: List[str] = []
        for (_, field_name, _, _) in Formatter().parse(self._format):
            if field_name is not None:
                if field_name not in FIELDS:
                    raise ValueError(f"Field {field_name} unknown in format string")
                self._fields.append(field_name)
        self._has_printed = 0

    def render(self, render_data: Dict[str, Dict[str, AggregateTimes]]) -> None:
        ls: List[str] = []
        for clock_name, clock_data in render_data.items():
            for line in self.render_times(clock_name, clock_data):
                ls.append(line)
        print(UP(self._has_printed) + CLR + f"\n{CLR}".join(ls))
        self._has_printed = len(ls)

    def render_times(
        self, clock_name: str, clock_data: Dict[str, AggregateTimes]
    ) -> Iterable[str]:
        for tick_key, times in clock_data.items():
            yield (
                CLR
                + f"⏱️ {clock_name} [{tick_key}] "
                + self._format.format(
                    **{key: FIELDS[key](times) for key in self._fields}
                )
            )
