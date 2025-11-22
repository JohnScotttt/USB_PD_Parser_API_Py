from typing import Any, List, Tuple
from tools.vendor_ids_dict import VENDOR_IDS
from usbpdparser.core import metadata

ColorToken = Tuple[str, str]  # (style, text)

__all__ = ["render"]

def _fmt_bit_loc(msg: metadata, indent: str) -> str:
    b0, b1 = msg.bit_loc()
    if b0 == b1:
        return f"{indent}{'[b'+str(msg.bit_loc()[0])+'] ':<12}"
    return f"{indent}{'[b'+str(msg.bit_loc()[0])+'-b'+str(msg.bit_loc()[1])+'] ':<12}"


def render_metadata(msg: metadata, level: int, out: List[ColorToken]):
    indent = '    ' * level
    if not isinstance(msg.value(), list):
        out.append(('red', _fmt_bit_loc(msg, indent)))
        out.append(('bold', f"{msg.field()}: "))
        out.append(('blue', f"{str(msg.value())} "))
        if msg.field() in ("USB Vendor ID", "VID"):
            out.append(('blue', f"[{VENDOR_IDS.get(str(msg.value()), 'Unknown Vendor')}] "))
        if not msg.raw().isdigit():
            out.append(('green', f"({msg.raw()})\n"))
        else:
            if level < 1:
                raw_bin = msg.raw()
                out.append(('green', f"(0x{int(raw_bin, 2):0{int(len(raw_bin)/4)+(1 if len(raw_bin)%4 else 0)}X})\n"))
            else:
                out.append(('green', f"({msg.raw()}b)\n"))
    else:
        out.append(('red', _fmt_bit_loc(msg, indent)))
        out.append(('bold', f"{msg.field()}: "))
        if msg.quick_pdo() != "Not a PDO":
            out.append(('purple', f"{msg.quick_pdo()} "))
        if msg.quick_rdo() != "Not a RDO":
            out.append(('purple', f"{msg.quick_rdo()} "))
        if not msg.raw().isdigit():
            out.append(('green', f"({msg.raw()}\n"))
        else:
            raw_bin = msg.raw()
            out.append(('green', f"(0x{int(raw_bin, 2):0{int(len(raw_bin)/4)+(1 if len(raw_bin)%4 else 0)}X})\n"))
        for sub in msg.value():
            render_metadata(sub, level + 1, out)
    return out


def render(data: Any) -> List[ColorToken]:
    buf: List[ColorToken] = []
    if isinstance(data, list):
        for m in data:
            render_metadata(m, 0, buf)
    else:
        render_metadata(data, 0, buf)
    return buf