
import argparse
import sys
from pathlib import Path

from . import pycpack


def main(args: argparse.Namespace) -> int:
    try:
        file_count = pycpack.process_root(args.root, args.optimization)
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
    parser.add_argument("root", type=_exiting_file)
    parser.add_argument("--optimization", type=int, choices=[0, 1, 2], default=2)
    return parser.parse_args()


def _exiting_file(path: str) -> Path:
    path = Path(path)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File or directory '{path}' does not exist.")
    return path