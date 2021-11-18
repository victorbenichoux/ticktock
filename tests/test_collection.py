from ticktock import timer
from ticktock.std import FORMATS, StandardRenderer
from ticktock.timer import ClockCollection, disable, enable, set_collection, tick


def test_env_set_period(fresh_configuration, monkeypatch):
    collection = ClockCollection()
    assert collection._period == 2

    monkeypatch.setenv("TICKTOCK_DEFAULT_PERIOD", "1")
    collection = ClockCollection()
    assert collection._period == 1

    set_collection(collection)
    assert timer._DEFAULT_COLLECTION._period == 1

    clock = tick()
    assert clock.collection._period == 1


def test_env_set_renderer_format(fresh_configuration, monkeypatch):
    renderer = StandardRenderer()
    assert renderer._format == FORMATS["short"]

    renderer = StandardRenderer(format="long")
    assert renderer._format == FORMATS["long"]


def test_set_enable_disable(fresh_configuration, monkeypatch):
    collection = ClockCollection()
    assert collection._enabled

    monkeypatch.setenv("TICKTOCK_DISABLE", "True")
    collection = ClockCollection()
    assert not collection._enabled

    monkeypatch.delenv("TICKTOCK_DISABLE")
    collection = ClockCollection()
    assert collection._enabled

    disable()
    assert not timer._DEFAULT_COLLECTION._enabled

    enable()
    assert timer._DEFAULT_COLLECTION._enabled
