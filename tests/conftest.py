import pytest

from ticktock.timer import ClockCollection


@pytest.fixture(scope="function")
def fresh_clock_collection():
    return ClockCollection()


@pytest.fixture(scope="function")
def incremental_timer():
    class IncrementalTimer:
        def __init__(self) -> None:
            self.count = 0

        def __call__(self) -> int:
            self.count += 1
            return self.count

    return IncrementalTimer()


@pytest.fixture(scope="function")
def constant_timer():
    class ConstantTimer:
        def __init__(self, v: int = 1) -> None:
            self.v = v

        def __call__(self) -> int:
            return self.v

    return ConstantTimer()