import os
import tempfile

from tests import TEST_DIR
from ticktock.renderers import StandardRenderer
from ticktock.timer import ClockCollection, tick


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

        with open(tmp_fn, encoding="utf-8") as f:
            with open(
                os.path.join(TEST_DIR, "testdata", "file_rendering.txt"),
                encoding="utf-8",
            ) as ftruth:
                assert list(f.readlines()) == list(ftruth.readlines())
