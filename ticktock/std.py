import logging
import os
import sys
from dataclasses import dataclass
from functools import partial
from string import Formatter
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    TextIO,
    Union,
)

from ticktock.renderers import (
    CONSTANT_FIELDS,
    RAW_FIELDS,
    TIME_FIELDS,
    AbstractRenderer,
)
from ticktock.utils import format_ns_interval

if TYPE_CHECKING:
    from ticktock.clocks import Clock
    from ticktock.data import AggregateTimes

try:
    import tqdm

    has_tqdm = True
except ImportError:
    has_tqdm = False

logger = logging.getLogger("ticktock.renderers")

UP: Callable[[int], str] = lambda x: f"\x1B[{x}A" if x else ""
CLR = "\r\x1B[0K"

FORMATS = {
    "short": "⏱️ [{name}] {mean} count={count}",
    "long": "⏱️ [{name}] "
    "{mean} ({std} std) min={min} max={max}"
    " count={count} last={last}",
}


@dataclass
class FormattingData:
    format: str
    precomputed_format: Dict[str, Callable[..., str]]
    raw_fields: List[str]
    time_fields: List[str]
    constant_fields: List[str]
    max_terms: int

    def render(self, clock: "Clock", tock_id: str, times: "AggregateTimes") -> str:
        if tock_id not in self.precomputed_format:
            self.precomputed_format[tock_id] = partial(
                self.format.format,
                **{
                    key: CONSTANT_FIELDS[key](clock, times)
                    for key in self.constant_fields
                },
            )
        return self.precomputed_format[tock_id](
            **{
                key: format_ns_interval(
                    TIME_FIELDS[key](times), max_terms=self.max_terms
                )
                for key in self.time_fields
            },
            **{key: str(RAW_FIELDS[key](clock, times)) for key in self.raw_fields},
        )


class StandardRenderer(AbstractRenderer):
    _formats: Dict[Union[str, None], str] = {}
    _formatting_data: Dict[Union[str, None], FormattingData] = {}
    _max_terms: int
    _out: TextIO
    _no_update: bool = False

    def __init__(
        self,
        format: Optional[str] = None,
        out: TextIO = sys.stderr,
        max_terms: int = 2,
        no_update: bool = False,
    ) -> None:
        self._max_terms = max_terms
        self._out = out
        self._no_update = no_update
        self._has_printed = 0
        self.set_format(format or os.environ.get("TICKTOCK_DEFAULT_FORMAT") or "short")

    def set_format(self, format: str, tick_id: Optional[str] = None):
        if format in FORMATS:
            format = FORMATS[format]
        self._formats[tick_id] = format

        raw_fields = []
        time_fields = []
        constant_fields = []
        for (_, field_name, _, _) in Formatter().parse(format):
            if field_name is not None:
                if field_name in RAW_FIELDS:
                    raw_fields.append(field_name)
                    continue
                if field_name in TIME_FIELDS:
                    time_fields.append(field_name)
                    continue
                if field_name in CONSTANT_FIELDS:
                    constant_fields.append(field_name)
                    continue
                raise ValueError(f"Field {field_name} unknown in format string")
        self._formatting_data[tick_id] = FormattingData(
            format=format,
            precomputed_format={},
            raw_fields=raw_fields,
            time_fields=time_fields,
            constant_fields=constant_fields,
            max_terms=self._max_terms,
        )

    def render(self, clocks: List["Clock"]) -> None:
        logger.debug("Rendering clock format={self._format}")
        ls: List[str] = []
        for clock in clocks:
            for line in self.render_times(clock):
                ls.append(line)
        if has_tqdm:
            with tqdm.tqdm.external_write_mode(sys.stderr, nolock=True):
                if self._no_update:
                    self._out.write("\n".join(ls) + "\n")
                else:
                    self._out.write(
                        UP(self._has_printed) + CLR + f"\n{CLR}".join(ls) + "\n"
                    )
                self._out.flush()
        else:
            if self._no_update:
                self._out.write("\n".join(ls) + "\n")
            else:
                self._out.write(
                    UP(self._has_printed) + CLR + f"\n{CLR}".join(ls) + "\n"
                )
            self._out.flush()
        self._has_printed = len(ls)

    def render_times(self, clock: "Clock") -> Iterable[str]:
        if clock._tick_id in self._formatting_data:
            for tock_id, times in clock.times.items():
                yield self._formatting_data[clock._tick_id].render(
                    clock, tock_id, times
                )
            return
        for tock_id, times in clock.times.items():
            yield self._formatting_data[None].render(clock, tock_id, times)
