from ticktock.collection import ClockCollection, set_collection
from ticktock.std import StandardRenderer
from ticktock.timers import ticktock
from ticktock.utils import _TockName


def test_decorator_with_arguments(fresh_clock_collection):
    @ticktock(name="KO", collection=fresh_clock_collection)
    def f(x):
        return x

    assert f(0.1) == 0.1
    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert clock.tick_name == "KO"
    clock_times = list(clock.times.values())
    assert len(clock_times) == 1
    assert clock_times[0].count == 1
    assert clock_times[0].tock_name == _TockName.DECORATOR
    assert f(0.1) == 0.1
    assert clock_times[0].count == 2
    assert clock_times[0].tock_name == _TockName.DECORATOR

    assert next(StandardRenderer(format="{name}").render_times(clock)) == "KO"


def test_decorator_no_arguments(fresh_clock_collection):
    set_collection(fresh_clock_collection)

    @ticktock
    def f(x):
        return x

    assert f(0.1) == 0.1
    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert clock.tick_name == "f"
    clock_times = list(clock.times.values())
    assert len(clock_times) == 1
    assert clock_times[0].count == 1
    assert clock_times[0].tock_name == _TockName.DECORATOR
    assert f(0.1) == 0.1
    assert clock_times[0].count == 2
    assert clock_times[0].tock_name == _TockName.DECORATOR

    assert next(StandardRenderer(format="{name}").render_times(clock)) == "f"

    set_collection(ClockCollection())
