from usbpdparser.core import metadata

ColorToken = tuple[str, str]

def renderer(data: list | metadata) -> list[ColorToken]: ...