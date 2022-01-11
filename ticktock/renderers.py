import abc
import logging
import os
from typing import TYPE_CHECKING, List

from ticktock.utils import _TockName

if TYPE_CHECKING:
    from ticktock.clocks import Clock
    from ticktock.data import AggregateTimes


logger = logging.getLogger("ticktock.renderers")


class AbstractRenderer(abc.ABC):
    def render(self, render_data: List["Clock"]) -> None:
        ...


class MultipleRenderers(AbstractRenderer):
    def __init__(self, renderers: List[AbstractRenderer]) -> None:
        super().__init__()
        self.renderers = renderers

    def render(self, render_data: List["Clock"]) -> None:
        for renderer in self.renderers:
            renderer.render(render_data)


TIME_FIELDS = {
    "mean": lambda times: times.avg_time_ns,
    "std": lambda times: times.std_time_ns,
    "min": lambda times: times.min_time_ns,
    "max": lambda times: times.max_time_ns,
    "last": lambda times: times.last_time_ns,
}


def name_field_fn(clock: "Clock", times: "AggregateTimes"):
    if times.tock_name == _TockName.DECORATOR:
        return clock.tick_name
    if times.tock_name == _TockName.CONTEXTMANAGER:
        if clock.tick_name:
            return clock.tick_name
    if clock.tick_name:
        if times.tock_name:
            return f"{clock.tick_name}-{times.tock_name}"
        else:
            return f"{clock.tick_name}:{clock.tick_line}-{times.tock_line}"
    else:
        if os.path.exists(clock.tick_filename):
            tick_name = os.path.basename(clock.tick_filename)
        else:
            tick_name = clock.tick_filename
        return f"{tick_name}:{clock.tick_line}-{times.tock_line}"


CONSTANT_FIELDS = {
    "name": name_field_fn,
    "tick_name": lambda clock, times: clock.tick_name,
    "tock_name": lambda clock, times: times.tock_name,
    "tick_line": lambda clock, times: clock.tick_line,
    "tock_line": lambda clock, times: times.tock_line,
    "tick_filename": lambda clock, times: clock.tick_filename,
    "tock_filename": lambda clock, times: times.tock_filename,
}

RAW_FIELDS = {
    "count": lambda clock, times: times.count,
    "avg_time_ns": lambda clock, times: times.avg_time_ns,
    "std_time_ns": lambda clock, times: times.std_time_ns,
    "min_time_ns": lambda clock, times: times.min_time_ns,
    "max_time_ns": lambda clock, times: times.max_time_ns,
    "last_time_ns": lambda clock, times: times.last_time_ns,
}


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

    def render(self, render_data: List["Clock"]) -> None:
        for clock in render_data:
            for times in clock.times.values():
                self._log(
                    "clock",
                    clock_name=name_field_fn(clock, times),
                    mean=times.avg_time_ns * 1e-9,
                    std=times.std_time_ns * 1e-9,
                    min=times.min_time_ns * 1e-9,
                    max=times.max_time_ns * 1e-9,
                    count=times.count,
                )
