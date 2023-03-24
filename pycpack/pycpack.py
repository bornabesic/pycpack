
import py_compile
from pathlib import Path
from typing import List


def process_root(root: Path, optimization: int) -> int:
    paths: List[Path]
    if root.is_dir():
        paths = [path for path in root.rglob("*.py") if path.is_file()]
    else:
        paths = [root]

    for path in paths:
        input_path = str(path)
        output_path = str(path.with_suffix(".pyc"))
        py_compile.compile(input_path, output_path, optimize=optimization)

    return len(paths)
