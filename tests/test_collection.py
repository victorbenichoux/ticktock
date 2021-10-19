import pytest

from ticktock.config import (
    CURRENT_CONFIGURATION,
    get_default_configuration,
    set_configuration,
)


@pytest.fixture(scope="session")
def fresh_configuration():
    set_configuration(get_default_configuration())
    yield
    set_configuration(get_default_configuration())


def test_set_env_period(fresh_configuration, monkeypatch):
    conf = get_default_configuration()
    assert conf["DEFAULT_PERIOD"] == 2

    monkeypatch.setenv("TICKTOCK_DEFAULT_PERIOD", "1")
    conf = get_default_configuration()
    assert conf["DEFAULT_PERIOD"] == 1

    set_configuration({"DEFAULT_PERIOD": 10})
    assert CURRENT_CONFIGURATION["DEFAULT_PERIOD"] == 10
