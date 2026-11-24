"""Quick check that a site can be reached from this machine, before any browser test starts.

Browser tests wait 30 seconds per page when the network drops their traffic, which hides the
real cause. This check takes a few seconds and says what is wrong.
"""
import socket
from urllib.parse import urlparse


def target_from_url(url):
    """Return (host, port) for a URL, using 443 for https and 80 for http by default."""
    parts = urlparse(url)
    host = parts.hostname or ""
    port = parts.port or (443 if parts.scheme == "https" else 80)
    return host, port


def can_connect(host, port=443, timeout=5.0):
    """True if a TCP connection opens within the timeout."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False
