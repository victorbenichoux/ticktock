import abc
import logging
from string import Formatter
from typing import Callable, Iterable, List, Optional

from ticktock.data import ClockData
from ticktock.utils import format_ns_interval, value_from_env

UP: Callable[[int], str] = lambda x: f"\x1B[{x}A" if x else ""
CLR = "\x1B[0K"

FIELDS = {
    "mean": lambda times: format_ns_interval(times.avg_time_ns),
    "std": lambda times: format_ns_interval(times.std_time_ns),
    "min": lambda times: format_ns_interval(times.min_time_ns),
    "max": lambda times: format_ns_interval(times.max_time_ns),
    "last": lambda times: format_ns_interval(times.last_time_ns),
    "count": lambda times: times.n_periods,
}


class AbstractRenderer(abc.ABC):
    def render(self, render_data: List[ClockData]) -> None:
        ...


FORMATS = {
    "short": "{mean} count={count}",
    "long": "{mean} ({std} std) min={min} max={max} count={count} last={last}",
}


class StandardRenderer(AbstractRenderer):
    def __init__(self, format: Optional[str] = None) -> None:
        self._format: str = format or value_from_env("TICKTOCK_DEFAULT_FORMAT", "short")
        if self._format in FORMATS:
            self._format = FORMATS[self._format]

        self._fields: List[str] = []
        for (_, field_name, _, _) in Formatter().parse(self._format):
            if field_name is not None:
                if field_name not in FIELDS:
                    raise ValueError(f"Field {field_name} unknown in format string")
                self._fields.append(field_name)
        self._has_printed = 0

    def render(self, render_data: List[ClockData]) -> None:
        ls: List[str] = []
        for clock_data in render_data:
            for line in self.render_times(clock_data):
                ls.append(line)
        print(UP(self._has_printed) + CLR + f"\n{CLR}".join(ls))
        self._has_printed = len(ls)

    def render_times(self, clock_data: ClockData) -> Iterable[str]:
        for times in clock_data.times.values():
            yield (
                CLR
                + "⏱️ "
                + f"[{clock_data.tick_name}-{times.tock_name}] "
                + self._format.format(
                    **{key: FIELDS[key](times) for key in self._fields}
                )
            )


class LoggingRenderer(AbstractRenderer):
    def __init__(
        self, logger=None, level: str = "INFO", extra_as_kwargs: bool = False
    ) -> None:
        self.logger = logger or logging.getLogger("ticktock")
        _log_function = {
            "DEBUG": self.logger.debug,
            "INFO": self.logger.info,
            "WARNING": self.logger.warning,
            "ERROR": self.logger.error,
            "CRITICAL": self.logger.critical,
        }[level]
        if extra_as_kwargs:

            def _log(msg, **kwargs):
                _log_function(msg, **kwargs)

        else:

            def _log(msg, **kwargs):
                _log_function(msg, extra=kwargs)

        self._log = _log

    def render(self, render_data: List[ClockData]) -> None:
        for clock_data in render_data:
            for times in clock_data.times.values():
                self._log(
                    "clock",
                    tick_name=clock_data.tick_name,
                    tock_name=clock_data.tick_name,
                    mean=times.avg_time_ns * 1e9,
                    std=times.std_time_ns * 1e9,
                    min=times.min_time_ns * 1e9,
                    max=times.max_time_ns * 1e9,
                    count=times.n_periods,
                )
