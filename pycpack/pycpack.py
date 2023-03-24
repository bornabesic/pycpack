
import py_compile
from pathlib import Path
from typing import List


def compile_directory_tree(source: Path, destination: Path, optimization: int = -1) -> int:
    """
    Compiles all Python files in `source` directory tree to bytecode (.pyc).
    Outputs the same directory hierarchy but rooted at `destination`.
    :param source: Source directory, usually the root of a Python project
    :param destination: Destination directory for bytecode files
    :param optimization: Bytecode optimization level (see `builtins.compile`)
    :return: Number of compiled files
    """
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
