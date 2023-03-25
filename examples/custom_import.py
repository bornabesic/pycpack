import sys
from collections.abc import Sequence
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec, SourcelessFileLoader

bytecode = {
    "just_print": b'o\r\r\n\x00\x00\x00\x00\xf0\xe3\x1ed\x18\x00\x00\x00\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                  b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00@\x00\x00\x00s\x0c\x00\x00\x00e\x00d\x00\x83\x01'
                  b'\x01\x00d\x01S\x00)\x02z\rHello, world!N)\x01\xda\x05print\xa9\x00r\x02\x00\x00\x00r\x02\x00'
                  b'\x00\x00\xfa\rjust_print.py\xda\x08<module>\x01\x00\x00\x00s\x02\x00\x00\x00\x0c\x01'
}


class PycpackLoader(SourcelessFileLoader):

    def get_data(self, path) -> bytes:
        return bytecode[self.name]


class PycpackFinder(MetaPathFinder):
    def find_spec(self, fullname, path: Sequence, target=None) -> ModuleSpec | None:
        if fullname not in bytecode:
            print(fullname, path)
            return None

        loader = PycpackLoader(fullname, path)
        is_package = True  # TODO Figure out
        return ModuleSpec(fullname, loader, origin=None, loader_state=None, is_package=is_package)


sys.meta_path.append(PycpackFinder())

# Prints "Hello, world!"
import just_print
