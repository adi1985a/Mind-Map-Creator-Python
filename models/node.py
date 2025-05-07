from typing import Optional, List, Dict
import uuid
from PyQt5.QtGui import QColor

class Node:
    # Add shape constants
    SHAPES = {
        "rectangle": "rectangle",
        "ellipse": "ellipse",
        "diamond": "diamond",
        "hexagon": "hexagon",
        "rounded": "rounded"
    }

    def __init__(self, title: str, content: str = "", parent: Optional['Node'] = None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.parent = parent
        self.children: List[Node] = []
        self.style: Dict = {
            "color": "#000000",
            "background": "#FFFFFF",
            "border_color": "#000000",
            "border_width": 2,
            "shape": self.SHAPES["rectangle"],
            "size": (100, 50)
        }
        self.position = (0, 0)
        self.attachments = []

    def add_child(self, child: 'Node') -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: 'Node') -> None:
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def set_color(self, color: str) -> None:
        """Set the background color of the node"""
        self.style["background"] = color

    def set_border_color(self, color: str) -> None:
        """Set the border color of the node"""
        self.style["border_color"] = color

    def set_text_color(self, color: str) -> None:
        """Set the text color of the node"""
        self.style["color"] = color

    def set_shape(self, shape: str) -> None:
        """Set the shape of the node"""
        if shape in self.SHAPES.values():
            self.style["shape"] = shape
