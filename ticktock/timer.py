import inspect
import time
from typing import Dict, Optional

from ticktock.config import CURRENT_CONFIGURATION
from ticktock.data import AggregateTimes
from ticktock.std import StandardRenderer


class ClockCollection:
    def __init__(self, period: Optional[float] = None) -> None:
        self.clocks: Dict[str, Clock] = {}
        self._last_refresh_time_s: Optional[float] = None
        self._period: float = period or CURRENT_CONFIGURATION["DEFAULT_PERIOD"]
        self.renderer = StandardRenderer()

    def update(self):
        if (
            self._last_refresh_time_s is None
            or time.perf_counter() - self._last_refresh_time_s > self._period
        ):
            self.render()
            self._last_refresh_time_s = time.perf_counter()

    def render(self):
        self.renderer.render(
            {
                clock.name: {
                    name: times for name, times in clock.aggregate_times.items()
                }
                for _, clock in self.clocks.items()
            }
        )


_TICKTOCK_CLOCKS = ClockCollection()


class Clock:
    def __init__(
        self,
        name: str = None,
        collection: Optional[ClockCollection] = None,
        tick_time_ns: Optional[int] = None,
        tick_frame_info: Optional[inspect.FrameInfo] = None,
    ) -> None:
        self.collection: ClockCollection = collection or _TICKTOCK_CLOCKS

        self.name: str = name or f"clock_{len(self.collection.clocks)}"

        self._tick_frame_info: inspect.FrameInfo = tick_frame_info or inspect.stack()[1]
        self._unique_id = (
            name or f"{self._tick_frame_info.filename}:{self._tick_frame_info.lineno}"
        )

        self.aggregate_times: Dict[str, AggregateTimes] = {}

        self.collection.clocks[self._unique_id] = self

        self._tick_time_ns: Optional[int] = tick_time_ns

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

        if self._tick_time_ns is None:
            raise ValueError(f"Clock {self.name} was not ticked.")

        if name in self.aggregate_times:
            self.aggregate_times[name].update(tock_time_ns, self._tick_time_ns)
        else:
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
    collection = collection or _TICKTOCK_CLOCKS
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


class ticktock:
    def __init__(
        self,
        name: str = None,
        collection: Optional[ClockCollection] = None,
        tick_time_ns: Optional[int] = None,
    ) -> None:
        self.collection = collection
        self.name = name
        self.tick_time_ns = tick_time_ns
        self.t = None

    def __enter__(self):
        self.t = tick(
            name=self.name, collection=self.collection, tick_time_ns=self.tick_time_ns
        )

    def __exit__(self, *_):
        self.t.tock()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            t = tick(
                name=self.name,
                collection=self.collection,
                tick_time_ns=self.tick_time_ns,
            )
            retval = func(*args, **kwargs)
            t.tock()
            return retval

        return wrapper
