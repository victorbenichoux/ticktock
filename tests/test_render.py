import difflib
import os
import shutil
import tempfile

from tests import TEST_DIR
from ticktock.renderers import StandardRenderer
from ticktock.timer import ClockCollection, tick


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
