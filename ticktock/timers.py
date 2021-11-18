import inspect
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from ticktock.collection import ClockCollection

from ticktock.clocks import tick
from ticktock.utils import TockName


class ticktock:
    def __init__(
        self,
        name: str = None,
        collection: Optional["ClockCollection"] = None,
        timer: Optional[Callable[[], int]] = None,
    ) -> None:
        self._func: Optional[Callable] = None
        self.timer = timer
        if callable(name):
            self._func = name
        else:
            self.name = name
            self.t = None
        self.collection = collection

    def __enter__(self):
        self.t = tick(
            name=self.name,
            collection=self.collection,
            timer=self.timer,
        )

    def __exit__(self, *_):
        self.t.tock()

    def __call__(self, *args, **kwargs):
        def _decorate(func):
            func_n_lines = len(inspect.getsource(func).split("\n")) - 2
            func_first_lineno = func.__code__.co_firstlineno
            func_filename = func.__code__.co_filename

            def wrapper(*args, **kwargs):
                t = tick(
                    name=func.__name__,
                    frame_info=(func_filename, func_first_lineno),
                    collection=self.collection,
                    timer=self.timer,
                )
                retval = func(*args, **kwargs)
                t.tock(
                    name=TockName.DECORATOR,
                    frame_info=(func_filename, func_n_lines + func_first_lineno),
                )
                return retval

            return wrapper

        if self._func:
            return _decorate(self._func)(*args, **kwargs)
        else:
            return _decorate(args[0])
