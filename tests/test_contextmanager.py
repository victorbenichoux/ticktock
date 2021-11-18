from ticktock.std import StandardRenderer
from ticktock.timers import ticktock


def test_contextmanager(fresh_clock_collection):
    with ticktock(collection=fresh_clock_collection):
        pass
    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert (
        next(StandardRenderer(format="{name}").render_times(clock)) == "timers.py:32-41"
    )

    fresh_clock_collection.clear()
    with ticktock(name="name", collection=fresh_clock_collection):
        pass
    assert len(fresh_clock_collection.clocks) == 1
    clock = next(iter(fresh_clock_collection.clocks.values()))
    assert next(StandardRenderer(format="{name}").render_times(clock)) == "name"
