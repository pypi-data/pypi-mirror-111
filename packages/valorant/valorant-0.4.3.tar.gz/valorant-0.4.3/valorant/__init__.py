import urllib3

urllib3.disable_warnings()

del urllib3

from .client import Client
from .local import LocalClient
from .threads import AsyncClient

__all__ = ["Client", "AsyncClient", "LocalClient"]
__author__ = "frissyn"
__version__ = "0.4.3"
