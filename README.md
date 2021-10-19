</p>
<h1 align="center"> ticktock </h1>
<p align="center">
  <em>Simple Python code metering library.</em>
</p>
    
---
`ticktock` is a minimalist library to view Python time performance of Python code.

First, install `ticktock`:
```
pip install py-ticktock
```

Then, anywhere in your code you can use `tick` to start a clock, and `tock` to register the end of the snippet you want to time:

```python
t = tick()
# do some work
t.tock()
```

Even if the code is called many times within a loop, measured times will only periodially (2 seconds by default):

```python
import time
from ticktock import tick

for _ in range(1000):
    t = tick()
    # do some work
    time.sleep(1)
    t.tock()
```

You can create multiple independent ticks, which will appear as two separate clocks:

```python
for _ in range(1000):
    t = tick()
    # do some work
    time.sleep(1)
    t.tock()

    t = tick()
    # do some other work
    time.sleep(0.5)
    t.tock()
```

Ticks can share a common starting point:

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