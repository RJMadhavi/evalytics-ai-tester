"""Safety rules shared by every automated test and, later, every AI agent.

These are plain functions with no browser or network code, so they are unit tested
(see common/tests/test_guardrails.py). The rules come from the test plan, section 2:
  - only visit allow-listed hosts (exact names, no wildcards)
  - never send write requests unless a test says so and the owner has approved it
  - throttle page navigations
  - stop at once when the kill switch is on
  - never submit a sign-up form that could really create an academy by accident
"""
import os
import pathlib
import re
import time
from urllib.parse import urlparse

DEFAULT_ALLOWED_HOSTS = ("evalytics.in",)
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
KILL_FILE = pathlib.Path(".local/KILL")

# Hosts that would contradict the site's "zero third-party trackers" claim.
KNOWN_TRACKERS = (
    "google-analytics.com", "googletagmanager.com", "doubleclick.net",
    "facebook.net", "facebook.com", "connect.facebook.net", "hotjar.com",
    "clarity.ms", "mixpanel.com", "segment.com", "segment.io", "fullstory.com",
    "amplitude.com", "heap.io", "intercom.io", "sentry.io",
)


class GuardrailError(RuntimeError):
    """Raised when a safety rule would be broken."""


def parse_hosts(extra=None):
    """Allowed hosts: evalytics.in plus any exact names in EVA_ALLOWED_HOSTS.

    Subdomains are NOT allowed automatically. Other academies are real customers,
    so list only your own test academies, for example "myqa1.evalytics.in,myqa2.evalytics.in".
    """
    hosts = list(DEFAULT_ALLOWED_HOSTS)
    if extra:
        hosts += [h.strip().lower() for h in extra.split(",") if h.strip()]
    return tuple(dict.fromkeys(hosts))


def host_allowed(url, hosts):
    host = (urlparse(url).hostname or "").lower()
    return host in hosts


def require_host_allowed(url, hosts):
    if not host_allowed(url, hosts):
        raise GuardrailError(f"Host not on the allow-list: {url} (allowed: {', '.join(hosts)})")


def kill_switch_active(environ=None, path=None):
    """True if EVA_KILL=1 is set or the file .local/KILL exists."""
    environ = os.environ if environ is None else environ
    path = KILL_FILE if path is None else pathlib.Path(path)
    return environ.get("EVA_KILL", "") == "1" or path.exists()


def write_allowed(method, allow_writes):
    return method.upper() in SAFE_METHODS or bool(allow_writes)


def tracker_hosts(hosts):
    found = []
    for h in sorted(hosts):
        h = h.lower()
        if any(h == t or h.endswith("." + t) for t in KNOWN_TRACKERS):
            found.append(h)
    return found


class Throttle:
    """Make sure at least min_interval seconds pass between actions."""

    def __init__(self, min_interval=1.0, clock=time.monotonic, sleep=time.sleep):
        self.min_interval = float(min_interval)
        self._clock = clock
        self._sleep = sleep
        self._last = None

    def wait(self):
        now = self._clock()
        if self._last is not None:
            gap = self.min_interval - (now - self._last)
            if gap > 0:
                self._sleep(gap)
                now = self._clock()
        self._last = now


_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_SUBDOMAIN = re.compile(r"^[a-z0-9-]+$")


def academy_form_problems(name, subdomain, your_name, email, password, confirm):
    """Return the reasons this sign-up form would be rejected. An empty list means
    the form looks valid, which means submitting it could create a real academy."""
    problems = []
    if not name.strip():
        problems.append("academy name is empty")
    if not subdomain or not _SUBDOMAIN.match(subdomain):
        problems.append("subdomain is empty or has characters other than a-z, 0-9 and hyphen")
    if not your_name.strip():
        problems.append("your name is empty")
    if not _EMAIL.match(email or ""):
        problems.append("email is not a valid address")
    if not password:
        problems.append("password is empty")
    if password != confirm:
        problems.append("password and confirmation differ")
    return problems


def require_invalid_academy_form(*fields):
    """Call before submitting a negative test. Refuses if the form is fully valid."""
    problems = academy_form_problems(*fields)
    if not problems:
        raise GuardrailError("Refusing to submit: the form looks valid and could create a real academy.")
    return problems
