"""
Global config containing things like the stylesheet.
"""

from pathlib import Path

import attr


@attr.s(auto_attribs=True)
class Config:
    data: list[Path]
