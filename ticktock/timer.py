import inspect
import math
import time
from dataclasses import dataclass
from typing import Dict, Optional

from ticktock.utils import format_ns_interval

DEFAULT_PERIOD = 2.0


class ClockCollection:
    def __init__(self, period: Optional[float] = None) -> None:
        self.clocks: Dict[str, Clock] = {}
        self._last_refresh_time_s: Optional[float] = None
        self._period: float = period or DEFAULT_PERIOD

    def update(self):
        if (
            self._last_refresh_time_s is None
            or time.perf_counter() - self._last_refresh_time_s > self._period
        ):
            self.print()
            self._last_refresh_time_s = time.perf_counter()

    def print(self):
        print("# Clocks")
        for clock in self.clocks.values():
            for key, info in clock.aggregate_times.items():
                print(
                    f"{clock.name} [{key}] "
                    f"avg = {format_ns_interval(info.avg_time_ns)}, "
                    f"last = {format_ns_interval(info.last_time_ns())}, "
                    f"n = {info.n_periods}"
                )


_INTIME_CLOCKS = ClockCollection()


@dataclass
class TickTimeInfo:
    file_name: str
    line_no: str


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


class Clock:
    def __init__(
        self,
        name: str = None,
        collection: Optional[ClockCollection] = None,
        tick_time_ns: Optional[float] = None,
        tick_frame_info: Optional[inspect.FrameInfo] = None,
    ) -> None:
        self.collection: ClockCollection = collection or _INTIME_CLOCKS

        self.name: str = name or f"clock_{len(self.collection.clocks)}"

        self._tick_frame_info: inspect.FrameInfo = tick_frame_info or inspect.stack()[1]
        self._unique_id = (
            name or f"{self._tick_frame_info.filename}:{self._tick_frame_info.lineno}"
        )

        self.aggregate_times: Dict[str, AggregateTimes] = {}

        self.collection.clocks[self._unique_id] = self

        self._tick_time_ns: Optional[float] = tick_time_ns

    def tick(self) -> float:
        self._tick_time_ns = time.perf_counter_ns()
        return self._tick_time_ns

    def tock(self, name: str = None) -> float:
        if not name:
            tock_caller_frame = inspect.stack()[1]
            name = (
                f"{tock_caller_frame.filename}:"
                f"{self._tick_frame_info.lineno}-"
                f"{tock_caller_frame.lineno}"
            )

        tock_time_ns = time.perf_counter_ns()

        if name in self.aggregate_times:
            self.aggregate_times[name].update(tock_time_ns, self._tick_time_ns)
        else:
            if self._tick_time_ns is None:
                raise ValueError(f"Clock {self.name} was not ticked.")
            dt = tock_time_ns - self._tick_time_ns
            self.aggregate_times[name] = AggregateTimes(
                last_tick_time_ns=self._tick_time_ns,
                last_tock_time_ns=tock_time_ns,
                avg_time_ns=dt,
                min_time_ns=dt,
                max_time_ns=dt,
            )

        self.collection.update()
        return tock_time_ns


def tick(
    name: str = None,
    collection: Optional[ClockCollection] = None,
    tick_time_ns: Optional[int] = None,
) -> Clock:
    collection = collection or _INTIME_CLOCKS
    if not name:
        tick_frame_info: inspect.FrameInfo = inspect.stack()[1]
        if f"{tick_frame_info.filename}:{tick_frame_info.lineno}" in collection.clocks:
            clock = collection.clocks[
                f"{tick_frame_info.filename}:{tick_frame_info.lineno}"
            ]
            clock.tick()
            return clock
    clock = Clock(
        name=name,
        collection=collection,
        tick_time_ns=tick_time_ns,
        tick_frame_info=tick_frame_info,
    )
    clock.tick()
    return clock
