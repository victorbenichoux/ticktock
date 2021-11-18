
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

### `tick` parameters

You can specify some options for each call to `tick`: 
```python
tick(
    name: str = "",
    format: Optional[str] = None,
    timer: Optional[Callable[[], int]] = None,
    enabled: Optional[bool] = None,
    collection: Optional["ClockCollection"] = None,
    frame_info: Optional[Tuple[str, int]] = None
)
```

Where:

- `name` sets a name for your clock, which you can retrieve in the `tick_name` key in formatters
- `format` sets a format only for this clock (it will be ignored if using a `LoggingRenderer`)
- `timer` sets the timer method for this clock. Note that default formatting in `ticktock` expects this function to return time in nanoseconds. Defaults to `timing.perf_counter_ns`.
- `enabled` sets the state of the clock, if set to `False`, the clock will be ignored and will not be rendered
- (Advanced) `collection` sets the parent `ClockCollection` of this clock
- (Advanced) `frame_info` is a tuple (string and int) that is used to uniquely identify the clock. If left unset, this will be the filename and line number where `tick` is called


### Clock with multiple `tock` calls

A `Clock` can measure times between a `tick` and multiple `tock`: intervals are measured and reported between the `tick` and all `tock` calls.

For example, the clock below will track the timing between `tick` and `first tock` as well as between `tick` and `second_tock`:

```python
from ticktock import tick

clock = tick("tick")
clock.tock("first_tock")
clock.tock("second_tock")
```

These will be reported as two separate lines (or two log messages).


## The `Clock` object

You can also instantiate a `Clock`, and use its `tick` and `tock` methods:

```python
from ticktock.clocks import Clock

clock = Clock()
clock.tick()  # returns the Clock instance
clock.tock()  # returns the time between the last tick and tock
```

The `Clock` initialization has the exact same signature as `tick` above.
```python
clock = Clock("some_name")
```

Or its parent `ClockCollection`:
```python
clock = Clock("some_name", collection=my_collection)
```

## `Clock.times` attribute

Internally, `Clock` objects maintain a `times` attribute. It is a dictionary of `ticktock.data.AggegateTimes` dataclasses (one for each `tock`) that holds statistics on the measured times.

Everytime a `tock` is performed on the clock, it updates its estimates in the `times` attribute (all time values are in nanoseconds):

- `tock_name: str` the name of the tock
- `tock_filename: str` the filename where tock was called
- `tock_line: int` the line number where tock was called
- `count: int` the number of times `tock` was called
- `avg_time_ns: float` the running average of time intervals
- `min_time_ns: float` and `max_time_ns: float` the running extrema of time intervals
- `last_time_ns: float` the last measured time interval
- `std_time_ns: float = 0` the running standard deviation of  time intervals
