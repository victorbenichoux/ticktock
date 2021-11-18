import logging
import time
from typing import TYPE_CHECKING, Callable, Dict, Optional, Tuple, Union

if TYPE_CHECKING:
    from ticktock.collection import ClockCollection

from ticktock import collection as collection_module
from ticktock.data import AggregateTimes
from ticktock.utils import _TockName, get_frame_info, value_from_env

logger = logging.getLogger("ticktock.clocks")


class Clock:
    def __init__(
        self,
        name: str = "",
        format: Optional[str] = None,
        timer: Optional[Callable[[], int]] = None,
        enabled: Optional[bool] = None,
        collection: Optional["ClockCollection"] = None,
        frame_info: Optional[Tuple[str, int]] = None,
    ) -> None:
        self.tick_filename, self.tick_line = frame_info or get_frame_info(1)
        self._tick_id = f"{self.tick_filename}:{self.tick_line}"

        self.tick_name = name

        self._timer = timer or time.perf_counter_ns
        self._tick_time_ns: Optional[int] = None

        self._enabled = enabled
        if self._enabled is None:
            self._enabled = not value_from_env("TICKTOCK_DISABLE", False)

        self.times: Dict[str, AggregateTimes] = {}

        self.collection: "ClockCollection" = (
            collection or collection_module._DEFAULT_COLLECTION
        )
        self.collection.clocks[self._tick_id] = self

        if format:
            self.collection.set_format(format, tick_id=self._tick_id)

    def tick(self) -> "Clock":
        if self.is_enabled():
            self._tick_time_ns = self._timer()
        return self

    def tock(
        self,
        name: Union[str, _TockName] = "",
        frame_info: Optional[Tuple[str, int]] = None,
    ) -> Optional[float]:
        if not self.is_enabled():
            return None
        tock_time_ns = self._timer()
        tock_id = "{}:{}".format(*(frame_info or get_frame_info(1)))
        if self._tick_time_ns is None:
            raise ValueError(f"Clock {self.tick_name} was not ticked.")
        if tock_id in self.times:
            self.times[tock_id].update(tock_time_ns, self._tick_time_ns)
            self.collection.update(force=False)
        else:
            dt = tock_time_ns - self._tick_time_ns
            tock_filename, tock_line = frame_info or get_frame_info(1)
            self.times[tock_id] = AggregateTimes(
                tock_name=name,
                tock_line=tock_line,
                tock_filename=tock_filename,
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
    name: str = "",
    format: Optional[str] = None,
    timer: Optional[Callable[[], int]] = None,
    enabled: Optional[bool] = None,
    collection: Optional["ClockCollection"] = None,
    frame_info: Optional[Tuple[str, int]] = None,
) -> Clock:
    collection = collection or collection_module._DEFAULT_COLLECTION
    tick_id = "{}:{}".format(*(frame_info or get_frame_info(1)))
    if tick_id in collection.clocks:
        return collection.clocks[tick_id].tick()
    return Clock(
        name=name,
        format=format,
        collection=collection,
        frame_info=frame_info or get_frame_info(1),
        timer=timer,
        enabled=enabled,
    ).tick()
