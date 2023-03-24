
import argparse
import sys
from pathlib import Path

from . import pycpack


def main(args: argparse.Namespace) -> int:
    try:
        file_count = pycpack.compile_directory_tree(args.source, args.destination, args.optimization)
        print(f"{file_count} Python file(s) have been compiled to bytecode.")
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    return 0


def _start() -> None:
    args = _parse_args()
    status = main(args)
    sys.exit(status)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        type=_existing_path, help="Source directory, usually the root of a Python project"
    )
    parser.add_argument(
        "destination",
        type=Path, help="Destination directory for bytecode files"
    )
    parser.add_argument(
        "-O", "--optimization",
        type=int, choices=[0, 1, 2], default=2, help="Bytecode optimization level (see `builtins.compile`)"
    )
    return parser.parse_args()


def _existing_path(path: str) -> Path:
    path = Path(path)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File or directory '{path}' does not exist.")
    return path
