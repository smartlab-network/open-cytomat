from .cytomat import Cytomat
from .scripts.setup_cytomat import post_install
post_install()
__all__ = ["Cytomat", "post_install"]