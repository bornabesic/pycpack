
import py_compile
from pathlib import Path
from typing import List


def compile_directory_tree(source: Path, destination: Path, optimization: int = -1) -> int:
    paths: List[Path]
    if source.is_dir():
        paths = [path for path in source.rglob("*.py") if path.is_file()]
    else:
        paths = [source]

    for path in paths:
        input_path = str(path)
        output_path = str(destination / path.relative_to(source).with_suffix(".pyc"))
        py_compile.compile(input_path, output_path, optimize=optimization)

    return len(paths)
