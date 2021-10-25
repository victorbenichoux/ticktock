from ticktock import ticktock
from ticktock.timer import ClockCollection, set_collection


def test_decorator_with_arguments(fresh_clock_collection):
    @ticktock("KO", collection=fresh_clock_collection)
    def f(x):
        return x

    assert f(0.1) == 0.1
    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    clock_times = list(clock.aggregate_times.values())
    assert len(clock_times) == 1
    assert clock_times[0].n_periods == 1
    assert f(0.1) == 0.1
    assert clock_times[0].n_periods == 2


def test_decorator_no_arguments(fresh_clock_collection):
    set_collection(fresh_clock_collection)

    @ticktock
    def f(x):
        return x

    assert f(0.1) == 0.1
    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    clock_times = list(clock.aggregate_times.values())
    assert len(clock_times) == 1
    assert clock_times[0].n_periods == 1
    assert f(0.1) == 0.1
    assert clock_times[0].n_periods == 2
    set_collection(ClockCollection())
