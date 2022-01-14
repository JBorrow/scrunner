"""
``scrunner`` is a library to automatically run a series
of scripts that all conform to the same API, on various data
sources.
"""

from scrunner.version import __version__

from scrunner.arguments import ScriptArgumentParser
from scrunner.html import WebpageCreator
from scrunner.runner import ScriptRunner
