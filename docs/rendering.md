# Rendering

## Specifying a renderer

The renderer for `ticktock` is defined through the `ClockCollection` object. Create your own `ClockCollection` to modify it, and set it as the default collection, for example:

```python
from ticktock.timer import ClockCollection, set_collection
from ticktock import renderers

collection = ClockCollection(renderer = renderers.StandardRenderer())
set_collection(collection=collection)
```

## Standard renderer

The `StandardRenderer` is used by default and prints to stdout.

Instantiate a `renderer` with `StandardRenderer(format: Optional[str] = None)`

`format` is a regular Python format string describing the desired output. The keys in the format string have to be amongst the available timings aggregates: `"mean"`, `"std"`, `"min"`, `"max"`, `"last"` and `"count"`.

Two special `formats` are accepted too:
    - `"short"` corresponding to  `"{mean} count={count}"`
    - `"long"` corresponding to `"{mean} ({std} std) min={min} max={max} count={count} last={last}"`

    
## Logging renderer

The `LoggingRenderer` is used to render timing information as log messages instead of printing.

Instantiate it with `LoggingRenderer(logger=None, level :str = "INFO", extra_as_kwargs: bool = False)` and set it to the default `ClockCollection`.

This will make `ticktock` render all statistics as log messages of the given log level. Statistics are passed as a dictionary to the `extra` attribute of the `logger` by default. As a result you should make sure that your logging handler and formatter correctly outputs the contents of the `extra` dictionary.

If your logger accepts keyword arguments to the logging functions (for example with `structlog`), provide your own logger and set `extra_as_kwargs` to `True`.