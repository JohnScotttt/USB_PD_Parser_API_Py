from usbpdparser.core import metadata

ColorToken = tuple[str, str]

def renderer(data: list | metadata, level_thr: int) -> list[ColorToken]: ...