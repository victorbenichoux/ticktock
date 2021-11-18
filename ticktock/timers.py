import inspect
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from ticktock.collection import ClockCollection

from ticktock.clocks import tick
from ticktock.utils import _TockName, get_frame_info


class ticktock:
    _func: Optional[Callable] = None

    def __init__(
        self,
        *args,
        name: str = "",
        format: Optional[str] = None,
        timer: Optional[Callable[[], int]] = None,
        enabled: Optional[bool] = None,
        collection: Optional["ClockCollection"] = None,
    ) -> None:
        if args and callable(args[0]):
            self._func = args[0]
        self._name = name
        self._format = format
        self._timer = timer
        self._collection = collection
        self._enabled = enabled

    def __enter__(self):
        self.clock = tick(
            name=self._name,
            format=self._format,
            timer=self._timer,
            enabled=self._enabled,
            collection=self._collection,
            frame_info=get_frame_info(1),
        )

    def __exit__(self, *_):
        self.clock.tock(name=_TockName.CONTEXTMANAGER, frame_info=get_frame_info(1))

    def __call__(self, *args, **kwargs):
        def _decorate(func):
            func_n_lines = len(inspect.getsource(func).split("\n")) - 2
            func_first_lineno = func.__code__.co_firstlineno
            func_filename = func.__code__.co_filename

            def wrapper(*args, **kwargs):
                t = tick(
                    name=self._name or func.__name__,
                    format=self._format,
                    timer=self._timer,
                    enabled=self._enabled,
                    collection=self._collection,
                    frame_info=(func_filename, func_first_lineno),
                )
                retval = func(*args, **kwargs)
                t.tock(
                    name=_TockName.DECORATOR,
                    frame_info=(func_filename, func_n_lines + func_first_lineno),
                )
                return retval

            return wrapper

        if self._func:
            return _decorate(self._func)(*args, **kwargs)
        else:
            return _decorate(args[0])
