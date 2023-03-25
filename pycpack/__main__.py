
import argparse
import sys
from pathlib import Path

from . import pycpack


def main(args: argparse.Namespace) -> int:
    try:
        if args.action == "compile":
            file_count = pycpack.compile_directory_tree(args.source, args.destination, args.optimization)
            print(f"{file_count} Python file(s) have been compiled to bytecode.")
        elif args.action == "embed":
            c_file_path, h_file_path = pycpack.embed_bytecode_files(args.source, args.destination)
            print("Source file:", c_file_path)
            print("Header file:", h_file_path)
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
    subparser = parser.add_subparsers(dest="action")
    subparser.required = True

    # Compile
    action_parser = subparser.add_parser("compile")
    action_parser.add_argument(
        "source",
        type=_existing_path, help="Source directory, usually the root of a Python project"
    )
    action_parser.add_argument(
        "destination",
        type=Path, help="Destination directory for bytecode files"
    )
    action_parser.add_argument(
        "-O", "--optimization",
        type=int, choices=[0, 1, 2], default=2, help="Bytecode optimization level (see `builtins.compile`)"
    )

    # Embed
    embed_parser = subparser.add_parser("embed")
    embed_parser.add_argument(
        "source",
        type=_existing_path, help="Source directory where bytecode files are located"
    )
    embed_parser.add_argument(
        "destination",
        type=Path, help="Destination directory for generated files"
    )

    return parser.parse_args()


def _existing_path(path: str) -> Path:
    path = Path(path)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File or directory '{path}' does not exist.")
    return path
