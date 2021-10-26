</p>
<h1 align="center"> ticktock </h1>
<p align="center">
  <em>Simple Python code metering library.</em>
</p>

<p align="center">
  <a href="https://github.com/victorbenichoux/ticktock/actions?query=branch%3Amain+"><img src="https://img.shields.io/github/workflow/status/victorbenichoux/ticktock/CI/main" /></a>
  <a href="https://github.com/victorbenichoux/ticktock/actions/workflows/main.yml?query=branch%3Amain+"><img src="docs/badges/tests.svg" /></a>
  <a href="https://victorbenichoux.github.io/ticktock/coverage/index.html"><img src="docs/badges/coverage.svg" /></a>
  <a href="https://pypi.org/project/py-ticktock/"><img src="https://img.shields.io/pypi/v/py-ticktock" /></a>
  <a href="https://pypi.org/project/py-ticktock/"><img src="https://img.shields.io/pypi/pyversions/py-ticktock" /></a>
  <a href="https://victorbenichoux.github.io/ticktock/index.html"><img src="https://img.shields.io/badge/docs-latest-blue" /></a>
  <a href="https://github.com/victorbenichoux/ticktock/blob/main/LICENSE"><img src="https://img.shields.io/github/license/victorbenichoux/ticktock" /></a>
</p>

---

`ticktock` is a minimalist library to profile Python code: it periodically displays timing of running code.

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

This will print:
```
⏱️ [3-5] 50us count=1
```
Indicating that lines 3-5 took <50us to run.

You can use `ticktock` arbitrarily deep inside you Python code and still get meaningful timing information.

When the timer is called multiple times (for example within a loop), measured times will be aggregated and printed periodically (every 2 seconds by default).

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
⏱️ [4-6] 50us count=1000
```

`ticktock` acts as a context manager to track the timing of a chunk of code:

```python
from ticktock import ticktock

with ticktock():
    time.sleep(1)
```

Or as a decorator:

```python
from ticktock import ticktock

@ticktock
def f():
    time.sleep(1)
```

Checkout the [documentation](https://victorbenichoux.github.io/ticktock/) for a complete manual!

