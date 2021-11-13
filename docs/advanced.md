## Advanced timing

### Interfaces

#### Context manager

It is possible to use `ticktock` as a context manager to track the timing of a chunk of code:

```python
from ticktock import ticktock

with ticktock():
    time.sleep(1)
```

#### Function decorator

`ticktock` doubles as a decorator that track sthe timing of each call to a function:

```python
from ticktock import ticktock

@ticktock
def f():
    time.sleep(1)

f()
```

### Naming timers

It is possible to name the beginning ("tick") and the end ("tock") of timers as so

```python
from ticktock import tick

clock = tick("beginning")
clock.tock("end")
```

Which will then be displayed as 

```
⏱️ [beginning-end] 1ms count=1
```

### Multiple Clocks

You can create multiple independent ticks, which will appear as two separate clocks:

```python
for _ in range(1000):
    clock = tick()
    # do some work
    time.sleep(1)
    clock.tock()

    clock = tick()
    # do some other work
    time.sleep(0.5)
    clock.tock()
```

A single clock can have a multiple `tocks`, which will be displayed as different lines

```python
for k in range(1000):
    t = tick()
    # do some work
    time.sleep(1)
    if k % 2 == 1:
        time.sleep(1)
        t.tock()
    else:
        t.tock()
```


### Enabling/Disabling clocks

It is possible to disable `ticktock` clocks: when disabled, the intervals between ticks and tocks are no longer recorded, and will not be rendered either.

#### With an environment variable

Set the `TICKTOCK_DISABLE` environment variable to disable all clocks and their rendering.

#### With `enable/disable`

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

#### Disabling a `Clock` vs. disabling a `ClockCollection`

!!! warn
    This is an advanced topic, and should not occur unless you set the enabled/disabled state of `Clock` objects directly.

Both `Clock` and `ClockCollection` objects can be enabled or disabled independently via their `enable`/`disable` methods.

This can be misleading if a `Clock`'s state does not match its `ClockCollection` state.

Simply put, here are the gotchas:

- a disabled `Clock` will not record any timing information, but if its `ClockCollection` is enabled, its state *will* be rendered
- disabling and enabling a `ClockCollection` will set the state of all of the `Clock`s that are *currently attached* to it
- disabling a clock *does not* disable its `ClockCollection`