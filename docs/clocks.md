
The most important objects in `ticktock` are clocks, which record timing.
## `tick` and `Clock`

### Creating clocks with `tick`

The normal way to initialize a `Clock` is to use the `tick` method:

```python
from ticktock import tick

clock = tick()
```

Which returns an instance of `Clock`. Calling the `tock` method of the `Clock` will record the time and return the elapsed time interval:

```
time_interval = clock.tock()
```

!!! info
    By default, `ticktock` return time intervals in nanoseconds, to change this change the [timer function](#timer-function).


### `tick` and `Clock` instances

An important feature of `ticktock` is that any call to `tick` will return *the same instance* of a clock. This is because `Clock` instances are identified by *where they are defined*:

```python
from ticktock import tick

for _ in range(10):
    clock = tick()
    print(id(clock))  # will print the *same* value
```

??? note

    Normally, instances of objects are different everytime they are created:

    ```python
    from ticktock import tick

    class A:
        pass

    for _ in range(10):
        instance = A()
        print(id(instance))  # will print different values
    ```

    Whenever a `Clock` is created with `tick`, `ticktock` will inspect the calling frame to determine which line in the code is being run. 

A consequence is that you can redefine and discard `clocks` as you wish. 

For example, the following code creates and tracks *two clocks*: one starting at line 3, and finishing at line 4, and the other one starting at line 6 and finishing at line 7.

``` python linenums="1"
from ticktock import tick

clock = tick()
clock.tock()

clock = tick()
clock.tock()
```

## Clocks

You can define a `Clock` directly, and use its `tick` and `tock` methods:

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

The `Clock` object maintains a list of dataclasses with the current values of the last measured times for each of the `Clock`'s `tock`s in `Clock.times`.

Each item in the list has the following attributes, that are updated everytime a `tock` is performed on the clock. All time values are in nanoseconds:

- `tock_name: str` the name of the tock
- `n_periods: int` the number of measured `tocks`
- `avg_time_ns: float` the running average measured time
- `std_time_ns: float = 0` the running standard deviation
- `min_time_ns: float` and `max_time_ns: float` the running extrema
- `last_tick_time_ns: float` the last time this was `tick`ed
- `last_tock_time_ns: float` the last time this was `tock`ed
- `last_time_ns: float` the last measured time