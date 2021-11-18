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

# Installation


`ticktock` is available in the PyPI repository:
```
pip install py-ticktock
```

# Quick start

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