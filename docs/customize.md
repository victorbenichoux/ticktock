`ticktock` defaults to writing clock times to `sys.stderr`.

It is possible to [change the renderer used](#specifying-a-renderer), which is useful if you want to customize the output, or send log messages.


## Changing format

It is possible to change the output of `ticktock` clocks by changing the *format* string.

### Setting the format string

The format string is a regular Python format string describing the desired output. Set the format string for the current default clock using `set_format`.

For example, to print the minimum and maximum times of a clock, one could write:

```python
from ticktock import set_format

set_format("{min} < {mean} < {max}")
```

Equivalently, to globally set the format string, set the `TICKTOCK_DEFAULT_FORMAT` environment variable.

### Format string keys


The keys in the format string have to be amongst the available attributes, and will be replaced by their value at render.

Keys are of two distinct types, *time keys* and normal keys. Time keys will be replaced by a string representing the timing value with its unit attached:

- `mean`: the average of all past time intervals
- `std`: the standard deviation of all past time intervals
- `min`: the minimum measured time
- `max`: the maximum measured time
- `last`: the last measured time
- `count`: the numer of intervals measured.

Normal keys have properties related to the position of the tick or tock:

- `tick_name`: the tick name if set when calling `tick`, otherwise equal to `{tick_filename}:{tick_line}`
- `tock_name`: the tock name if set when calling `tock`, otherwise equal to `{tock_line}`
- `tick_line`: the line at which `tick` was called in your code
- `tock_line`: the line at which `tock` was called in your code
- `tick_filename`: the name of the file in which `tick` was called
- `tock_filename`: the name of the file in which `tock` was called

In addition, two special cased formats are accepted too:

- `short` with just the average time and the count 
```python
"⏱️ [{tick_name}-{tock_name}] {mean} count={count}"
```
- `long` corresponding to 
```python
"⏱️ [{tick_name}-{tock_name}] {mean} ({std} std) min={min} max={max} count={count} last={last}"
```

### Units

By default, `ticktock` renders *two unit levels* such that 1.3 seconds will be written as `1s300ms`, or 1 day and two hours and 50 minuts will be written as `1d2h`.

If you need more precision, you can also set the number of units you want displayed using the `max_terms` keyword in `set_format` as so:


```python
from ticktock import set_format

set_format(max_terms = 3)
```

### Raw time fields

You can access the raw (floating point) values of the time aggregates as keys in the `format` string as well.

These are all recorded in nanoseconds (unless you specified a different `timer` function):

- `avg_time_ns`:the average of all past time intervals
- `std_time_ns`: the standard deviation of all past time intervals
- `min_time_ns`: the minimum measured time
- `max_time_ns`: the maximum measured time
- `last_time_ns`: the last measured time


### Updated lines

By default, `ticktock` attempts to update the last clock lines it has displayed with the new values.

However, it can be undesirable in some instandes:
- it can fail if other things are being written to the stream (e.g. using `print` in the code, or using `tqdm`), or delete printed messages
- it uses ASCII contol chars, which may be unwelcome if you are writing to a file

If you want `ticktock` to write all clocks sequentially, without attempting to update previously renderered lines, set the format with `no_update=True`:

```python
from ticktock import set_format

set_format(no_update=True)
```

## Change rendering period

By default, `ticktock` renders clocks with a fixed period of two seconds. This can be changed globally by using `set_period`:

```python
from ticktock import tick

set_period(1)
```

Internally, `ticktock` will render all clocks whenever the period is elapsed, and a clock's `tock` was called. In addition to this, rendering also occurs:

- at the first `tock` of any clock
- when the program exits


## Enabling or disabling clocks

It is possible to disable `ticktock` clocks: when disabled, the intervals between ticks and tocks are no longer recorded, and will not be rendered either.

### With an environment variable

Set the `TICKTOCK_DISABLE` environment variable to disable all clocks and their rendering.

### With `enable/disable`

`ticktock` also provide functions to enable or disable all clocks (and rendering):

```python
from ticktock import tick, enable, disable

def some_function():
    t = tick()
    pass
    t.tock()

# This call will be timed and collected
some_function()

disable()
# This call will NOT be timed
some_function()

enable()
# This call will be timed again
some_function()
```

!!! warn
    `enable` and `disable` act on the current default `ClockCollection` (as set by `set_collection`)

### Disabling a `Clock` vs. disabling a `ClockCollection`

!!! warn
    This is an advanced topic, and should not occur unless you set the enabled/disabled state of `Clock` objects directly.

Both `Clock` and `ClockCollection` objects can be enabled or disabled independently via their `enable`/`disable` methods.

This can be misleading if a `Clock`'s state does not match its `ClockCollection` state.

Simply put, here are the gotchas:

- a disabled `Clock` will not record any timing information, but if its `ClockCollection` is enabled, its state *will* be rendered
- disabling and enabling a `ClockCollection` will set the state of all of the `Clock`s that are *currently attached* to it
- disabling a clock *does not* disable its `ClockCollection`