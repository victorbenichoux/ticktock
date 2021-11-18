import atexit
import logging
import time
import weakref
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from ticktock.renderers import AbstractRenderer
    from ticktock.clocks import Clock

from ticktock.std import StandardRenderer
from ticktock.utils import value_from_env

logger = logging.getLogger("ticktock.timer")

_ALL_COLLECTIONS = []


class ClockCollection:
    def __init__(
        self,
        period: Optional[float] = None,
        renderer: Optional["AbstractRenderer"] = None,
        enabled: Optional[bool] = None,
    ) -> None:
        self._enabled = enabled
        if self._enabled is None:
            self._enabled = not value_from_env("TICKTOCK_DISABLE", False)
        self.clocks: Dict[str, "Clock"] = {}
        self._last_refresh_time_s: Optional[float] = None
        self._period: float = period or value_from_env("TICKTOCK_DEFAULT_PERIOD", 2.0)
        self.renderer = renderer or StandardRenderer()
        _ALL_COLLECTIONS.append(weakref.ref(self))

    def update(self, force: bool = False):
        if self._enabled and (
            force
            or (
                self._last_refresh_time_s is None
                or time.perf_counter() - self._last_refresh_time_s > self._period
            )
        ):
            self.renderer.render([clock for clock in self.clocks.values()])
            self._last_refresh_time_s = time.perf_counter()

    def clear(self):
        self.clocks = {}

    def enable(self):
        for clock in self.clocks.values():
            clock.enable()
        self._enabled = True

    def disable(self):
        for clock in self.clocks.values():
            clock.enable()
        self._enabled = False

    def set_format(
        self,
        format: str = None,
        tick_id: str = None,
        max_terms: int = None,
        no_update: bool = None,
    ):
        if not isinstance(self.renderer, StandardRenderer):
            logger.warn("Setting format of a renderer that does not support format")
            return
        if format is not None:
            self.renderer.set_format(format, tick_id=tick_id)
        if max_terms is not None:
            self.renderer._max_terms = max_terms
        if no_update is not None:
            self.renderer._no_update = no_update


_DEFAULT_COLLECTION = ClockCollection()


def set_collection(collection: ClockCollection):
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION = collection


def set_period(period: float):
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION._period = period


def clear_collection():
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION.clear()


def enable():
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION.enable()


def disable():
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION.disable()


def set_format(format: str = None, max_terms: int = None, no_update: bool = None):
    global _DEFAULT_COLLECTION
    _DEFAULT_COLLECTION.set_format(
        format=format, max_terms=max_terms, no_update=no_update
    )


@atexit.register
def final_update():
    for collection_ref in _ALL_COLLECTIONS:
        collection = collection_ref()
        if collection is not None:
            try:
                collection.update(force=True)
            except:  # noqa: E722
                pass
