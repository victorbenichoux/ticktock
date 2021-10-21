import time

import pytest

from ticktock.timer import Clock, ClockCollection, tick, ticktock


@pytest.fixture(scope="function")
def fresh_clock_collection():
    return ClockCollection()


def test_tick_simple(fresh_clock_collection):
    t = tick(collection=fresh_clock_collection)
    t.tock()

    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert len(clock.aggregate_times) == 1

    t.tock()
    assert len(clock.aggregate_times) == 2


def test_tick_simple_in_function(fresh_clock_collection):
    def f():
        t = tick(collection=fresh_clock_collection)
        t.tock()

    for _ in range(2):
        f()

    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert len(clock.aggregate_times) == 1

    def f2():
        t = tick(collection=fresh_clock_collection)
        t.tock()

    assert len(fresh_clock_collection.clocks) == 1
    f2()
    assert len(fresh_clock_collection.clocks) == 2


def test_clock_no_tick(fresh_clock_collection):
    clock = Clock()
    with pytest.raises(ValueError):
        clock.tock()


def test_contextmanager(fresh_clock_collection):
    with ticktock(collection=fresh_clock_collection):
        pass
    assert len(fresh_clock_collection.clocks) == 1


def test_decorator(fresh_clock_collection):
    @ticktock(collection=fresh_clock_collection)
    def f(x):
        time.sleep(x)

    f(0.1)
    f(0.1)
    assert len(fresh_clock_collection.clocks) == 1
