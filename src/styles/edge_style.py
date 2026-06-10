from dataclasses import dataclass
from src.enums.color import Color

@dataclass
class EdgeStyle:
    label: str = ''
    color: Color = Color.GRAY
    bold: bool = False
