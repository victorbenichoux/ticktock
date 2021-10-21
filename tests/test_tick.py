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


@pytest.mark.parametrize("name_tick", [None, "ok"])
def test_tick_identity(name_tick, fresh_clock_collection):
    t_id = None
    for _ in range(2):
        t = tick(name=name_tick, collection=fresh_clock_collection)
        assert len(fresh_clock_collection.clocks) == 1
        if t_id is not None:
            assert t_id == id(t)
        t_id = id(t)


@pytest.mark.parametrize(
    "name_tick, name_tock_1, name_tock_2, num_times",
    [
        (None, None, None, 2),
        ("ok", None, None, 2),
        ("ok", "boomer", None, 2),
        ("ok", "boomer", "boomer", 1),
        ("ok", "boomer", "boomer_2", 2),
        (None, "ok", None, 2),
        (None, "ok", "boomer", 2),
        (None, "ok", "ok", 1),
        ("ok", None, "boomer", 2),
    ],
)
def test_tick_name(
    name_tick, name_tock_1, name_tock_2, num_times, fresh_clock_collection
):
    t = tick(name=name_tick, collection=fresh_clock_collection)
    t.tock(name_tock_1)
    t.tock(name_tock_2)

    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert len(clock.aggregate_times) == num_times


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
