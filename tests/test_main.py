
import tempfile
import unittest
from pathlib import Path

import pycpack

TESTS_DIR = Path(__file__).parent


class TestMain(unittest.TestCase):

    def test_compile(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            file_count = pycpack.compile_directory_tree(TESTS_DIR.parent / "pycpack", tmp_dir)
            tmp_dir_files = list(tmp_dir.iterdir())
            self.assertEqual(file_count, 3)
            self.assertEqual(len(tmp_dir_files), 3)
            self.assertTrue(all(file.suffix == ".pyc" for file in tmp_dir_files))
