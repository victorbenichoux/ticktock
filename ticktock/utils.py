import inspect
import os
from enum import Enum
from typing import Tuple

time_factors = [
    (24 * 60 * 60 * 1e9, "d"),
    (60 * 60 * 1e9, "h"),
    (60 * 1e9, "m"),
    (1e9, "s"),
    (1e6, "ms"),
    (1e3, "us"),
    (1, "ns"),
]


def format_ns_interval(v_ns: float, max_terms: int = 2):
    remainder = v_ns
    out_str = ""
    n_terms = 0
    for fact, name in time_factors:
        current, remainder = divmod(remainder, fact)
        if current:
            out_str += f"{int(current):d}{name}"
            n_terms += 1
        if n_terms >= max_terms:
            return out_str
    return out_str


def value_from_env(env_var: str, default):
    if env_var in os.environ:
        return type(default)(os.environ[env_var])
    return default


def get_frame_info(level: int = 1) -> Tuple[str, int]:
    frame = inspect.currentframe()
    if frame:
        for _ in range(level + 1):
            if not frame:
                return "<no frame info>", -1
            frame = frame.f_back
        if not frame:
            return "<no frame info>", -1
        return (
            frame.f_code.co_filename,
            frame.f_lineno,
        )
    else:
        return "<no frame info>", -1


class _TockName(Enum):
    DECORATOR = 1
    CONTEXTMANAGER = 2
