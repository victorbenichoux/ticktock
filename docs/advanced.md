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