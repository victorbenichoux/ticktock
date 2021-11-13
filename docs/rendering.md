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

The `StandardRenderer` is used by default and prints to stdout: 

```python
StandardRenderer(format: Optional[str] = None, out: TextIO = sys.stderr, max_terms: int = 2)
```

- `format` is a regular Python format string describing the desired output. See [format strings](#format-string)
- `out` is a text IO stream to write to
- `max_terms` controls the number of units to display. `1.3` seconds will be written as `1s` with max_terms = 1 or `1s300ms` with `max_terms = 2`

### Format string

The keys in the format string have to be amongst the available timings aggregates: `"mean"`, `"std"`, `"min"`, `"max"`, `"last"` and `"count"`.
Two special `formats` are accepted too:

- `"short"` corresponding to  `"{mean} count={count}"`
- `"long"` corresponding to `"{mean} ({std} std) min={min} max={max} count={count} last={last}"`

    
## Logging renderer

The `LoggingRenderer` is used to render timing information as log messages instead of printing:

```python
LoggingRenderer(logger=None, level :str = "INFO", extra_as_kwargs: bool = False)
```

This will make `ticktock` render all statistics as log messages of the given log level. 
Statistics are passed as a dictionary to the `extra` attribute of the `logger` by default. As a result you should make sure that your logging handler and formatter correctly outputs the contents of the `extra` dictionary.

If your logger accepts keyword arguments to the logging functions (for example with `structlog`), provide your own logger and set `extra_as_kwargs` to `True`.