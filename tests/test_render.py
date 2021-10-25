import os
import tempfile

from tests import TEST_DIR
from ticktock.renderers import StandardRenderer
from ticktock.timer import ClockCollection, tick


def test_file_rendering(incremental_timer):

    with tempfile.NamedTemporaryFile(mode="w") as tmp_f:
        with open(tmp_f.name, "w") as f:
            collection = ClockCollection(
                renderer=StandardRenderer(out=f),
            )
            for _ in range(10):
                t = tick(name="start", collection=collection, timer=incremental_timer)
                t.tock("end")

        with open(tmp_f.name) as f:
            with open(
                os.path.join(TEST_DIR, "testdata", "file_rendering.txt")
            ) as ftruth:
                assert list(f.readlines()) == list(ftruth.readlines())
