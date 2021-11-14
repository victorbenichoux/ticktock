## Advanced timing

`ticktock` gives you different ways to specify which parts of your code you want to time: functions, a decorator, or a context manager.


### `tick` and `tock`


Use `tick` to create a `Clock` and signal the start of a measurement:

```python
from ticktock import tick

t = tick() # t is a Clock instance
```

Then, use the `tock` method to signal the end of the measurement for this clock:

```python
t.tock()
```

!!! info
    `tick` and `tock` function by recording the specific line in your code that they are created at. 
    
    This allows `ticktock` to aggregate times together although the `Clock` is redefined everytime the code is visited:

    ```python
    for _ in range(100):
        t = tick() # <- this is always the same object
        ...
        t.tock()
        id(t) # <- this is always the same value
    ```

### Context manager

It is possible to use `ticktock` as a context manager to track the timing of a chunk of code:

```python
from ticktock import ticktock

with ticktock():
    time.sleep(1)
```

### Function decorator

`ticktock` doubles as a decorator that tracks the timing of each call to a function:

```python
from ticktock import ticktock

@ticktock
def f():
    time.sleep(1)

f()
```

## Timer names

By default, `tick` creates a clock named after *where* it is first created (e.g. `path/to/the/code.py:line_number`), and `tock` is named after the line in which it is called. 

As a result, a `Clock` is typically renderer as `path/to/the/code.py:start-stop` where `start` and `stop` are the line numnbers of the `tick` and `tock`.


### Explicit clock naming

It is possible to explicitly name the beginning ("tick") and the end ("tock") of timers as so

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

Of course, can create multiple independent ticks, which will appear as separate clocks:

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


### Multiple Clock end times

More subtlely, a clock can have a multiple `tocks`, which will be displayed as different lines

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
