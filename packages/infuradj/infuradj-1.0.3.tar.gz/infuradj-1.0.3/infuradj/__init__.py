"""Django infura
    >>> from infuradj import send_tx
    >>> send_tx()
"""
from .lib import NETWORK_IDS, __setup, get_tx_details, send_tx

__version__ = "1.0.0"
