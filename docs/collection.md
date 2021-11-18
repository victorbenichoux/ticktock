## Collection

ticks and tocks are recorded in a globally defined `ClockCollection` defined in `ticktock.collection._DEFAULT_COLLECTION`.

It is possible to create a different `ClockCollection` and use it for your ticks and tocks as so:

```python
from ticktock.collection import ClockCollection

collection = ClockCollection()
tick(collection=collection)
tock(collection=collection)
```

The clock collection keeps track of all the clocks with their unique ids in `collection.clocks`, as well as deals with the rendering. 

### Rendering period

`ticktock` renders timing information on a fixed schedule with a given `period`. Update the `period` (in seconds) of the default collection to make it render more or less often:

```python
from ticktock.collection import ClockCollection, set_collection
from ticktock import renderers

collection = ClockCollection(period = 10)
set_collection(collection=collection)
```