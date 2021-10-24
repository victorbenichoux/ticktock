import inspect
import os
import time
from typing import Callable, Dict, Optional

from ticktock.data import AggregateTimes, ClockData
from ticktock.renderers import AbstractRenderer, StandardRenderer
from ticktock.utils import value_from_env


class ClockCollection:
    def __init__(
        self,
        period: Optional[float] = None,
        renderer: Optional[AbstractRenderer] = None,
    ) -> None:
        self.clocks: Dict[str, Clock] = {}
        self._last_refresh_time_s: Optional[float] = None
        self._period: float = period or value_from_env("TICKTOCK_DEFAULT_PERIOD", 2.0)
        self.renderer = renderer or StandardRenderer()

    def update(self):
        if (
            self._last_refresh_time_s is None
            or time.perf_counter() - self._last_refresh_time_s > self._period
        ):
            self.renderer.render(
                [
                    ClockData(tick_name=clock.tick_name, times=clock.aggregate_times)
                    for clock in self.clocks.values()
                ]
            )
            self._last_refresh_time_s = time.perf_counter()


_DEFAULT_COLLECTION = ClockCollection()


def set_collection(collection: ClockCollection):
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION = collection


class Clock:
    def __init__(
        self,
        name: Optional[str] = None,
        collection: Optional[ClockCollection] = None,
        tick_time_ns: Optional[int] = None,
        tick_frame_info: Optional[inspect.FrameInfo] = None,
        timer: Optional[Callable[[], int]] = None,
    ) -> None:
        self.timer = timer or time.perf_counter_ns

        self.collection: ClockCollection = collection or _DEFAULT_COLLECTION

        tick_frame_info = tick_frame_info or inspect.stack()[1]
        self._tick_frame_info: inspect.FrameInfo = tick_frame_info

        self._tick_id = name or f"{tick_frame_info.filename}:{tick_frame_info.lineno}"
        if not name:
            if os.path.exists(tick_frame_info.filename):
                self.tick_name = os.path.basename(self._tick_id)
            else:
                self.tick_name = f"{tick_frame_info.lineno}"
        else:
            self.tick_name = name

        self.aggregate_times: Dict[str, AggregateTimes] = {}

        self.collection.clocks[self._tick_id] = self

        self._tick_time_ns: Optional[int] = tick_time_ns

    def tick(self) -> float:
        self._tick_time_ns = self.timer()
        return self._tick_time_ns

    def tock(
        self,
        name: Optional[str] = None,
        tock_frame_info: Optional[inspect.FrameInfo] = None,
    ) -> float:
        _tock_frame_info: inspect.FrameInfo = tock_frame_info or inspect.stack()[1]

        tock_id = name or f"{_tock_frame_info.filename}:{_tock_frame_info.lineno}"
        tock_name = name or str(_tock_frame_info.lineno)

        tock_time_ns = self.timer()

        if self._tick_time_ns is None:
            raise ValueError(f"Clock {self.tick_name} was not ticked.")

        if tock_id in self.aggregate_times:
            self.aggregate_times[tock_id].update(tock_time_ns, self._tick_time_ns)
        else:
            dt = tock_time_ns - self._tick_time_ns
            self.aggregate_times[tock_id] = AggregateTimes(
                tock_name=tock_name,
                last_tick_time_ns=self._tick_time_ns,
                last_tock_time_ns=tock_time_ns,
                last_time_ns=dt,
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
    timer: Optional[Callable[[], int]] = None,
) -> Clock:
    collection = collection or _DEFAULT_COLLECTION
    tick_frame_info: inspect.FrameInfo = inspect.stack()[1]
    if name and name in collection.clocks:
        clock = collection.clocks[name]
    elif f"{tick_frame_info.filename}:{tick_frame_info.lineno}" in collection.clocks:
        clock = collection.clocks[
            f"{tick_frame_info.filename}:{tick_frame_info.lineno}"
        ]
    else:
        clock = Clock(
            name=name,
            collection=collection,
            tick_time_ns=tick_time_ns,
            tick_frame_info=tick_frame_info,
            timer=timer,
        )
    clock.tick()
    return clock


class ticktock:
    def __init__(
        self,
        name: str = None,
        collection: Optional[ClockCollection] = None,
        tick_time_ns: Optional[int] = None,
        timer: Optional[Callable[[], int]] = None,
    ) -> None:
        self._func: Optional[Callable] = None
        self.timer = timer
        if callable(name):
            self._func = name
        else:
            self.name = name
            self.tick_time_ns = tick_time_ns
            self.t = None
        self.collection = collection

    def __enter__(self):
        self.t = tick(
            name=self.name,
            collection=self.collection,
            tick_time_ns=self.tick_time_ns,
            timer=self.timer,
        )

    def __exit__(self, *_):
        self.t.tock()

    def __call__(self, *args, **kwargs):
        def _decorate(func):
            func_n_lines = len(inspect.getsource(func).split("\n")) - 2
            func_first_lineno = func.__code__.co_firstlineno

            def wrapper(*args, **kwargs):
                t = tick(
                    name=f"{func.__name__}:{func_first_lineno}",
                    collection=self.collection,
                    timer=self.timer,
                )
                retval = func(*args, **kwargs)
                t.tock(name=func_n_lines + func_first_lineno)
                return retval

            return wrapper

        if self._func:
            return _decorate(self._func)(*args, **kwargs)
        else:
            return _decorate(args[0])
