import difflib
import logging
import os
import shutil
import tempfile

import pytest

from tests import TEST_DIR
from ticktock.renderers import LoggingRenderer, StandardRenderer
from ticktock.timer import ClockCollection, set_collection, set_format, tick


def compare_text(truth_fn, result_fn):
    with open(result_fn, encoding="utf-8") as result_f:
        with open(
            os.path.join(TEST_DIR, "testdata", truth_fn),
            encoding="utf-8",
        ) as truth_f:
            rewrite = False
            diff_lines = list(
                difflib.unified_diff(
                    "\n".join(result_f.readlines()), "\n".join(truth_f.readlines())
                )
            )
            if len(diff_lines):
                if os.environ.get("UPDATE_TESTS"):
                    rewrite = True
                else:
                    raise AssertionError(
                        "File content mismatch.\n" + "\n".join(diff_lines)
                    )
            else:
                return
        if rewrite:
            shutil.copy2(result_fn, os.path.join(TEST_DIR, "testdata", truth_fn))


def test_file_rendering(incremental_timer):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_fn = os.path.join(tmp_dir, "file_rendering.txt")
        with open(tmp_fn, mode="w", encoding="utf-8") as f:
            collection = ClockCollection(
                renderer=StandardRenderer(out=f),
            )
            for _ in range(10):
                t = tick(name="start", collection=collection, timer=incremental_timer)
                t.tock("end")
        compare_text("file_rendering.txt", os.path.join(tmp_dir, "file_rendering.txt"))


def test_file_rendering_long(incremental_timer):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_fn = os.path.join(tmp_dir, "file_rendering_long.txt")
        with open(tmp_fn, mode="w", encoding="utf-8") as f:
            collection = ClockCollection(
                renderer=StandardRenderer(out=f),
            )
            collection.renderer.set_format("long")
            for _ in range(10):
                t = tick(name="start", collection=collection, timer=incremental_timer)
                t.tock("end")
        compare_text(
            "file_rendering_long.txt", os.path.join(tmp_dir, "file_rendering_long.txt")
        )


def test_set_format(caplog):
    renderer = StandardRenderer()
    collection = ClockCollection(renderer=renderer)
    set_collection(collection)
    set_format("a format")
    assert renderer._format == "a format"


def test_set_format_invalid_renderer(caplog):
    renderer = LoggingRenderer()
    collection = ClockCollection(renderer=renderer)
    set_collection(collection)
    with caplog.at_level(logging.WARNING):
        set_format("a format")
    assert len(caplog.records) == 1


def test_log_rendering(caplog):
    collection = ClockCollection(renderer=LoggingRenderer(level="DEBUG"))
    with caplog.at_level(logging.INFO):
        t = tick(collection=collection)
        t.tock()
    assert len(caplog.records) == 0

    collection = ClockCollection(renderer=LoggingRenderer(level="DEBUG"))
    with caplog.at_level(logging.DEBUG):
        t = tick(collection=collection)
        t.tock()
    assert len(caplog.records) == 1
    for record in caplog.records:
        assert hasattr(record, "tick_name")
        assert hasattr(record, "tock_name")
        assert hasattr(record, "mean")
        assert hasattr(record, "std")
        assert hasattr(record, "min")
        assert hasattr(record, "max")
        assert hasattr(record, "count")

    collection = ClockCollection(
        renderer=LoggingRenderer(level="DEBUG", extra_as_kwargs=True)
    )
    with caplog.at_level(logging.DEBUG):
        t = tick(collection=collection)
        with pytest.raises(TypeError):
            # this will fail because standard loggers do not accept
            # extra as keyword arguments
            t.tock()
