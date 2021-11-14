
## Advanced rendering

This section describes how to specify the exact renderer objects used by `ticktock`: 

- A [StandardRenderer](#standard-renderer) to print to a file, or even more control on the output
- A [LoggingRenderer](#logging-renderer) to send log messages

### Specifying a renderer

In `ticktock`, each ticktock `ClockCollection` object has a renderer attribute that controls how the clocks are rendered.

Create your own `ClockCollection` with a custom renderer to customiwe the way `ticktock` renders your clocks. 

Then, set it as the default collection so all your `tick`s and `tock`s are attached to it:

```python
from ticktock.timer import ClockCollection, set_collection
from ticktock import renderers

collection = ClockCollection(renderer = renderers.StandardRenderer())
set_collection(collection=collection)
```

### Standard renderer

The `StandardRenderer` is used by default and prints to stdout: 

```python
StandardRenderer(format: Optional[str] = None, out: TextIO = sys.stderr, max_terms: int = 2)
```

- `format` is a regular Python format string describing the desired output. See [format strings](#changing-format)
- `out` is a text IO stream to write to
- `max_terms` controls the number of units to display. `1.3` seconds will be written as `1s` with max_terms = 1 or `1s300ms` with `max_terms = 2`

    
## Logging renderer

The `LoggingRenderer` is used to render timing information as log messages instead of printing:

```python
LoggingRenderer(logger=None, level :str = "INFO", extra_as_kwargs: bool = False)
```

This will make `ticktock` render all statistics as log messages of the given log level. 
Statistics are passed as a dictionary to the `extra` attribute of the `logger` by default. As a result you should make sure that your logging handler and formatter correctly outputs the contents of the `extra` dictionary.

If your logger accepts keyword arguments to the logging functions (for example with `structlog`), provide your own logger and set `extra_as_kwargs` to `True`.