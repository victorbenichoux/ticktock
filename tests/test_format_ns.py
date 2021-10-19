import pytest

from ticktock.utils import format_ns_interval


@pytest.mark.parametrize(
    "v_ns, max_terms, out_str",
    [
        (1, 1, "1ns"),
        (1e3, 1, "1us"),
        (1e6, 1, "1ms"),
        (1e9, 1, "1s"),
        (60 * 1e9, 1, "1m"),
        (60 * 60 * 1e9, 1, "1h"),
        (24 * 60 * 60 * 1e9, 1, "1d"),
        (24 * 60 * 60 * 1e9, 2, "1d"),
        (24 * 60 * 60 * 1e9 + 60 * 60 * 1e9, 2, "1d1h"),
    ],
)
def test_format_ns(v_ns, max_terms, out_str):
    assert format_ns_interval(v_ns, max_terms=max_terms) == out_str
