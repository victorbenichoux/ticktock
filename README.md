</p>
<h1 align="center"> ticktock </h1>
<p align="center">
  <em>Simple Python code metering library.</em>
</p>

<p align="center">
  <a href="https://github.com/victorbenichoux/ticktock/actions?query=branch%3Amain+"><img src="https://img.shields.io/github/workflow/status/victorbenichoux/ticktock/CI/main" /></a>
  <a href="https://github.com/victorbenichoux/ticktock/actions/workflows/main.yml?query=branch%3Amain+"><img src="badges/tests.svg" /></a>
  <a href="https://victorbenichoux.github.io/ticktock/coverage/index.html"><img src="badges/coverage.svg" /></a>
  <a href="https://pypi.org/project/py-ticktock/"><img src="https://img.shields.io/pypi/v/py-ticktock" /></a>
  <a href="https://pypi.org/project/py-ticktock/"><img src="https://img.shields.io/pypi/pyversions/py-ticktock" /></a>
  <a href="https://victorbenichoux.github.io/ticktock/index.html"><img src="https://img.shields.io/badge/docs-latest-blue" /></a>
  <a href="https://github.com/victorbenichoux/ticktock/blob/main/LICENSE"><img src="https://img.shields.io/github/license/victorbenichoux/ticktock" /></a>
</p>

---

`ticktock` is a minimalist library to profile Python code, it displays timing of code snippets periodically.

# Quickstart


First, install `ticktock`:
```
pip install py-ticktock
```

Anywhere in your code you can use `tick` to start a clock, and `tock` to register the end of the snippet you want to time:

```python
from ticktock import tick

clock = tick()
# do some work
clock.tock()
```

This will print
```
⏱️ [3-5] 1ms count=1
```
Indicating that lines 3-5 take <1ms to run.


If the timed snippet is called multiple times (for example within a loop), measured times will be aggregated and printed periodically (every 2 seconds by default).

As a result, the following code:

```python
from ticktock import tick

for _ in range(1000):
    clock = tick()
    # do some work
    clock.tock()
```

Will output:
```
⏱️ [4-6] 1ms count=1000
```

# Advanced usage

## Multiple Clocks

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

## Context manager

It is also possible to use `ticktock` as a context manager to track the timing of a chunk of code:

```python
from ticktock import ticktock

with ticktock():
    time.sleep(1)
```

## Function decorator

Use the `ticktock` decorator to track the timing of each call to a function:

```python
from ticktock import ticktock

@ticktock
def f():
    time.sleep(1)

f()
```
