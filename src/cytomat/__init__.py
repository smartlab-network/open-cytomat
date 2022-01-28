import sys

if sys.version_info[:2] < (3, 8):
    import importlib_metadata as metadata
else:
    from importlib import metadata

from .cytomat import Cytomat

__version__ = metadata.version("open-cytomat")

__all__ = ["__version__", "Cytomat"]
