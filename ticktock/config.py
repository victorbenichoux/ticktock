import copy
import os
from typing import Dict, TypeVar

T = TypeVar("T")


def value_from_env(env_var: str, default):
    if env_var in os.environ:
        return type(default)(os.environ[env_var])
    return default


def get_default_configuration():
    return {
        "DEFAULT_PERIOD": value_from_env("TICKTOCK_DEFAULT_PERIOD", 2.0),
        "DEFAULT_FORMAT": value_from_env(
            "TICKTOCK_DEFAULT_FORMAT",
            "{mean} ({std} std) min={min} max={max} count={count} last={last}",
        ),
    }


_TICKTOCK_DEFAULT_CONFIGURATION = get_default_configuration()

CURRENT_CONFIGURATION = copy.deepcopy(_TICKTOCK_DEFAULT_CONFIGURATION)


def set_configuration(config_dict: Dict):
    global CURRENT_CONFIGURATION
    CURRENT_CONFIGURATION.update(config_dict)


def set_period(v: float):
    global CURRENT_CONFIGURATION

    CURRENT_CONFIGURATION.update({"DEFAULT_PERIOD": v})


def set_format(v: str):
    global CURRENT_CONFIGURATION

    CURRENT_CONFIGURATION.update({"DEFAULT_FORMAT": v})
