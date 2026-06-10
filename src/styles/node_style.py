from dataclasses import dataclass
from src.enums.color import Color

@dataclass
class NodeStyle:
    label: str = ''
    color: Color = Color.GRAY
    bold: bool = False
    fill: bool = False

