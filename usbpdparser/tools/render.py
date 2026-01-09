from usbpdparser.tools.vendor_ids_dict import VENDOR_IDS
from usbpdparser.core import metadata

ColorToken = tuple[str, str]  # (style, text)

def _fmt_bit_loc(msg: metadata, indent: str) -> str:
    b0, b1 = msg.bit_loc()
    if b0 == b1:
        return f"{indent}{'[b'+str(msg.bit_loc()[0])+'] ':<12}"
    return f"{indent}{'[b'+str(msg.bit_loc()[0])+'-b'+str(msg.bit_loc()[1])+'] ':<12}"


def render_metadata(msg: metadata, level: int, out: list[ColorToken], level_thr: int = 1) -> list[ColorToken]:
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
            if level < level_thr:
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
            render_metadata(sub, level + 1, out, level_thr)
    return out


def renderer(data: list | metadata, level_thr: int) -> list[ColorToken]:
    buf: list[ColorToken] = []
    if isinstance(data, list):
        for m in data:
            render_metadata(m, 0, buf, level_thr)
    else:
        render_metadata(data, 0, buf, level_thr)
    return buf