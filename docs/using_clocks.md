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

???+ tip "Naming"

    By default, `tick` creates a clock named after *where* it is first created (e.g. `path/to/the/code.py:line_number`), and `tock` is named after the line in which it is called. 

    As a result, a `Clock` is typically renderer as `path/to/the/code.py:start-stop` where `start` and `stop` are the line numbers of the `tick` and `tock`.

    You can name the beginning and end of timers:

    ```python
    clock = tick("beginning")
    clock.tock("end")
    ```

    Which will then be displayed as `⏱️ [beginning-end] 1ms count=1`


??? info "Clock identity"

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

???+ tip "Naming"
    By default the name of the clock with a context manager is the filename and line numbers, but you can also provide a name to the context manager:

    ```python
    with ticktock(name="some name"):
        pass
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

???+ note "Naming"
    Naming `ticktock` function decorators
    By default the name of the clock with a function decorator is the name of the function:

    ```python
    @ticktock
    def f():
        pass
    ```

    Will render as: `⏱️ [f] 1ms count=1`

    You can also provide a name to the decorator

    ```python
    @ticktock(name="some name")
    def f():
        pass
    ```

    Will render as: `⏱️ [some name] 1ms count=1`

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


A clock can also have a multiple `tocks`, which will be displayed as different lines

```python linenums="1"
t = tick("start")
time.sleep(1)
if k % 2 == 1:
    time.sleep(1)
    t.tock("one")
else:
    t.tock("two")
```

Which will lead to two lines being renderered:

```
⏱️ [start-one] 1s count=1
⏱️ [start-two] 2s count=1
```