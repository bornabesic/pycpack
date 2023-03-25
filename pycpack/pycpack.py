
import py_compile
import sys
from pathlib import Path
from typing import List, Tuple


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


def embed_bytecode_files(source: Path, destination: Path) -> Tuple[Path, Path]:
    paths = [path for path in source.rglob("*.pyc") if path.is_file()]
    destination.mkdir(exist_ok=True, parents=True)

    c_file_path = destination / "embed.c"
    h_file_path = destination / "embed.h"
    with c_file_path.open("w") as cf:
        print("static const char *bytecode[] = {", file=cf)
        for path in paths:
            with path.open("rb") as pycf:
                file_bytecode = pycf.read()
            file_bytecode_str = "\""
            for b in file_bytecode:
                file_bytecode_str += f"\\x{b.to_bytes(1, sys.byteorder).hex()}"
            file_bytecode_str += "\""
            print(file_bytecode_str + ",", file=cf)
        print("};", file=cf)

    # TODO Generate name to array index mapping
    # TODO Generate the header file

    return c_file_path, h_file_path
