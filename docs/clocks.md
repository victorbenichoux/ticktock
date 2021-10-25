
## Clocks

It is possible to use `Clock` objects directly:

```python
from ticktock.timer import Clock

clock = Clock()
clock.tick()
clock.tock()
```

This allows one to explicitly set the name of the clock:
```python
clock = Clock("some_name")
```

Or its parent `ClockCollection`:
```python
clock = Clock("some_name", collection=my_collection)
```

### `tick` and `tock` recording

Whenever a `Clock` is created, and when `tock` is called, `ticktock` will inspect the calling frame to determine which line in the code is being run. 

This allows one to redefine and discard `clocks`. For example, the following code creates and tracks *two separate clocks*: one starting at line 3, and finishing at line 4, and the other one starting at line 6 and finishing at line 7.

```python
from ticktock import tick

clock = tick()
clock.tock()

clock = tick()
clock.tock()
```

### timer function

It is possible to change the `timer` function of a clock (which defaults to `timing.perf_counter_ns`). When called without arguments, the timer function should return a measure of the current time in nanoseconds:

```python
clock = Clock(timer=my_timer)
```

### Clock with multiple `tock` calls

A `Clock` can measure times between a *single call to `tick`* and multiple `tock`: everytime `tick` is called it is reset, and intervals are measured between this `tick` and all the possible `tock`s. 

For example, in this snippet, the `clock` will track the timing between `tick` and `first tock` as well as between `tick` and `second_tock`:

```python
from ticktock.timer import Clock

clock = Clock(name="tick")
clock.tick()
clock.tock("first_tock")
clock.tock("second_tock")
```

On the other hand, when `tick` is called, the timer is reset, and as a result the first call to `tick` below is discarded:

```python
from ticktock.timer import Clock

clock = Clock()
clock.tick() # will be disregarded
clock.tick() # resets the clock
clock.tock("first_tock")
clock.tock("second_tock")
```

### Aggregate times attribute

The `Clock` object maintains a list of dataclasses with the current values of the last measured times for each of the `Clock`'s `tock`s in `Clock.aggregate_times`.

Each item in the list has the following attributes, that are updated everytime a `tock` is performed on the clock. All time values are in nanoseconds:

- `tock_name: str` the name of the tock
- `n_periods: int` the number of measured `tocks`
- `avg_time_ns: float` the running average measured time
- `std_time_ns: float = 0` the running standard deviation
- `min_time_ns: float` and `max_time_ns: float` the running extrema
- `last_tick_time_ns: float` the last time this was `tick`ed
- `last_tock_time_ns: float` the last time this was `tock`ed
- `last_time_ns: float` the last measured time