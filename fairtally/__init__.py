import logging
from .__version__ import __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "FAIR Software"
__email__ = "j.spaaks@esciencecenter.nl"


__all__ = [
    "__version__"
]
