# Copyright (c) 2025 JohnScotttt
# Version 1.0.2

__version__ = "1.0.2"


class metadata:
    def raw():
        """Return raw binary string representation of the field.""" 
        ...
    def bit_loc():
        """Return tuple of (start_bit, end_bit) for the field."""
        ...
    def field():
        """Return the name of the field."""
        ...
    def value():
        """Return the value of the field."""
        ...
    def quick_pdo(self) -> str:
        """Return a quick description if the field is a PDO."""
        ...
    def quick_rdo(self) -> str:
        """Return a quick description if the field is an RDO."""
        ...
    def pdo(self) -> metadata:
        """Return the PDO metadata form RDO if applicable."""
        ...
    def full_raw(self) -> str:
        """Return full raw binary string of the extended message."""
        ...
    def raw_value(self):
        """Return the raw value of the extended message."""
        ...


class Parser:
    def __init__(self, **kwargs): ...

    def parse(self,
              sop: str = None,  # SOP, SOP', SOP'', SOP'_DEBUG, SOP''_DEBUG
              raw: list | str | int | bytes = None,
              verify_crc: bool = False,
              last_pdo: metadata = None,
              last_ext: metadata = None,
              last_rdo: metadata = None) -> metadata: ...

def is_pdo(msg: metadata) -> bool: ...

def is_rdo(msg: metadata) -> bool: ...

def provide_ext(msg: metadata) -> bool: ...
