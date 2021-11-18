import abc
import logging
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ticktock.clocks import Clock


logger = logging.getLogger("ticktock.renderers")


class AbstractRenderer(abc.ABC):
    def render(self, render_data: List["Clock"]) -> None:
        ...


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
                    tick_name=clock.tick_name,
                    tock_name=times.tock_name,
                    mean=times.avg_time_ns * 1e9,
                    std=times.std_time_ns * 1e9,
                    min=times.min_time_ns * 1e9,
                    max=times.max_time_ns * 1e9,
                    count=times.n_periods,
                )
