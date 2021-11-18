from ticktock import tick


def test_timing_incremental(fresh_clock_collection, incremental_timer):
    clock = tick(collection=fresh_clock_collection, timer=incremental_timer)
    v = clock.tock()
    assert v == 1
    v = clock.tock()
    assert v == 2

    assert clock._tick_time_ns == 1
    first_timer = list(clock.times.values())[0]
    second_timer = list(clock.times.values())[1]

    assert first_timer.avg_time_ns == 1
    assert first_timer.std_time_ns == 0
    assert first_timer.count == 1
    assert first_timer.last_time_ns == 1

    assert second_timer.std_time_ns == 0
    assert second_timer.count == 1
    assert second_timer.avg_time_ns == 2
    assert second_timer.last_time_ns == 2


def test_timing_constant(fresh_clock_collection, constant_timer):
    for _ in range(10):
        t = tick(collection=fresh_clock_collection, timer=constant_timer)
        t.tock()
        t.tock()

    clock = list(fresh_clock_collection.clocks.values())[0]
    first_timer = list(clock.times.values())[0]
    second_timer = list(clock.times.values())[1]

    assert first_timer.avg_time_ns == 0
    assert first_timer.std_time_ns == 0
    assert first_timer.min_time_ns == 0
    assert first_timer.max_time_ns == 0
    assert first_timer.last_time_ns == 0
    assert first_timer.count == 10

    assert second_timer.avg_time_ns == 0
    assert second_timer.std_time_ns == 0
    assert second_timer.min_time_ns == 0
    assert second_timer.max_time_ns == 0
    assert second_timer.last_time_ns == 0
    assert second_timer.count == 10
