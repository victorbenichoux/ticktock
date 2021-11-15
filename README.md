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

This will print the timing of the lines 3 to 5 in your code as so:
```
⏱️ [3-5] 50us count=1
```

# How is `ticktock` different?

`ticktock` becomes really useful when you are trying to time code that is called multiple times. 

Rather than printing a new line each time the code is visited, `ticktock` computes tracks the times and *only prints them every couple of seconds*. 

`ticktock`'s output is **compact and readable**, regardless of how many times you run through the code you are timing, or where this code is.

As an example, the following code:

```python
from ticktock import tick

for _ in range(1000):
    clock = tick()
    # do some work
    clock.tock()
```

Will result in a *single, continuously updated line of output* showing you the average time and how many times it was called so far:
```
⏱️ [4-6] 50us count=1000
```

# Documentation

Checkout the [documentation](https://victorbenichoux.github.io/ticktock/) for a complete manual.

`ticktock` is actively being developed, be sure to submit [issues](https://github.com/victorbenichoux/ticktock/issues) or [pull requests](https://github.com/victorbenichoux/ticktock/pulls) with ideas!

