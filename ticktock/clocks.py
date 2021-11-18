import logging
import os
import time
from typing import TYPE_CHECKING, Callable, Dict, Optional, Tuple, Union

if TYPE_CHECKING:
    from ticktock.collection import ClockCollection

from ticktock import collection as collection_module
from ticktock.data import AggregateTimes
from ticktock.utils import TockName, get_frame_info, value_from_env

logger = logging.getLogger("ticktock.clocks")


class Clock:
    def __init__(
        self,
        name: Optional[str] = None,
        collection: Optional["ClockCollection"] = None,
        tick_time_ns: Optional[int] = None,
        frame_info: Optional[Tuple[str, int]] = None,
        timer: Optional[Callable[[], int]] = None,
        format: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> None:
        self._enabled = enabled
        if self._enabled is None:
            self._enabled = not value_from_env("TICKTOCK_DISABLE", False)

        self.timer = timer or time.perf_counter_ns

        self.tick_filename, self.tick_line = frame_info or get_frame_info(1)
        self._tick_id = name or f"{self.tick_filename}:{self.tick_line}"
        if not name:
            if os.path.exists(self.tick_filename):
                self.tick_name = os.path.basename(self._tick_id)
            else:
                self.tick_name = f"{self.tick_line}"
        else:
            self.tick_name = name

        self.times: Dict[str, AggregateTimes] = {}
        self._tick_time_ns: Optional[int] = tick_time_ns

        self.collection: "ClockCollection" = (
            collection or collection_module._DEFAULT_COLLECTION
        )
        self.collection.clocks[self._tick_id] = self
        if format:
            self.collection.set_format(format, tick_id=self._tick_id)

    def tick(self) -> Optional[float]:
        if not self.is_enabled():
            return None
        self._tick_time_ns = self.timer()
        return self._tick_time_ns

    def tock(
        self,
        name: Optional[Union[str, TockName]] = None,
        frame_info: Optional[Tuple[str, int]] = None,
    ) -> Optional[float]:
        if not self.is_enabled():
            return None
        tock_filename, tock_line = frame_info or get_frame_info(1)
        tock_id = f"{tock_filename}:{tock_line}"
        tock_name = name if name is not None else str(tock_line)

        tock_time_ns = self.timer()

        if self._tick_time_ns is None:
            raise ValueError(f"Clock {self.tick_name} was not ticked.")

        if tock_id in self.times:
            self.times[tock_id].update(tock_time_ns, self._tick_time_ns)
            self.collection.update(force=False)
        else:
            dt = tock_time_ns - self._tick_time_ns
            self.times[tock_id] = AggregateTimes(
                tock_name=tock_name,
                tock_line=tock_line,
                tock_filename=tock_filename,
                last_tick_time_ns=self._tick_time_ns,
                last_tock_time_ns=tock_time_ns,
                last_time_ns=dt,
                avg_time_ns=dt,
                min_time_ns=dt,
                max_time_ns=dt,
            )

            self.collection.update(force=True)
        return tock_time_ns - self._tick_time_ns

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self):
        return self._enabled and self.collection._enabled


def tick(
    name: str = None,
    format: Optional[str] = None,
    collection: Optional["ClockCollection"] = None,
    tick_time_ns: Optional[int] = None,
    frame_info: Optional[Tuple[str, int]] = None,
    timer: Optional[Callable[[], int]] = None,
    enabled: Optional[bool] = None,
) -> Clock:
    collection = collection or collection_module._DEFAULT_COLLECTION
    frame_info = frame_info or get_frame_info(1)
    filename, lineno = frame_info
    if name and name in collection.clocks:
        clock = collection.clocks[name]
    elif f"{filename}:{lineno}" in collection.clocks:
        clock = collection.clocks[f"{filename}:{lineno}"]
    else:
        clock = Clock(
            name=name,
            format=format,
            collection=collection,
            tick_time_ns=tick_time_ns,
            frame_info=frame_info,
            timer=timer,
            enabled=enabled,
        )
    clock.tick()
    return clock
