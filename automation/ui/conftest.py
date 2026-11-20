"""Shared setup for the browser tests: guardrails on every test, plus a run summary.

Safe by default:
  - every request to a host outside the allow-list is blocked when it is a page navigation
  - POST, PUT, PATCH and DELETE are blocked unless the test has @pytest.mark.writes_ok
  - page navigations are throttled (EVA_MIN_INTERVAL seconds, default 1.0)
  - the kill switch (EVA_KILL=1 or the file .local/KILL) stops the run before the next test
Environment variables:
  EVA_BASE_URL       default https://evalytics.in
  EVA_ALLOWED_HOSTS  your own test academy hosts, exact names, comma separated
  EVA_MIN_INTERVAL   seconds between page navigations
"""
import datetime
import json
import os
import pathlib
import warnings
from urllib.parse import urlparse

import pytest

from common.guardrails import (
    Throttle, host_allowed, kill_switch_active, parse_hosts,
    require_host_allowed, tracker_hosts, write_allowed,
)

ROOT = pathlib.Path(__file__).resolve().parents[2]
ALLOWED = parse_hosts(os.environ.get("EVA_ALLOWED_HOSTS"))
THROTTLE = Throttle(float(os.environ.get("EVA_MIN_INTERVAL", "1.0")))
RUN = {"versions": set(), "seen_hosts": set(), "blocked": []}


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("EVA_BASE_URL", "https://evalytics.in")


@pytest.fixture
def run_notes():
    return RUN


@pytest.fixture
def seen_hosts():
    return set()


@pytest.fixture
def console_errors(page):
    errors = []
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.on("console", lambda m: errors.append(f"console: {m.text}") if m.type == "error" else None)
    return errors


@pytest.fixture(autouse=True)
def guardrails(request, context, base_url, seen_hosts):
    if kill_switch_active():
        pytest.exit("Kill switch is on (EVA_KILL=1 or .local/KILL). Stopping.", returncode=2)
    require_host_allowed(base_url, ALLOWED)
    allow_writes = request.node.get_closest_marker("writes_ok") is not None
    blocked_writes, blocked_navigations = [], []

    def handler(route):
        req = route.request
        host = urlparse(req.url).hostname or ""
        seen_hosts.add(host)
        if not write_allowed(req.method, allow_writes):
            blocked_writes.append(f"{req.method} {req.url}")
            route.abort()
            return
        if req.resource_type == "document" and not host_allowed(req.url, ALLOWED):
            blocked_navigations.append(req.url)
            route.abort()
            return
        if req.resource_type == "document":
            THROTTLE.wait()
        route.continue_()

    context.route("**/*", handler)
    yield
    RUN["seen_hosts"] |= seen_hosts
    RUN["blocked"] += blocked_writes + [f"NAVIGATION {u}" for u in blocked_navigations]
    if blocked_writes:
        warnings.warn(f"Blocked {len(blocked_writes)} write request(s): {blocked_writes[:3]}")
    if blocked_navigations:
        pytest.fail(f"Navigation outside the allow-list was blocked: {blocked_navigations}")


def pytest_sessionfinish(session, exitstatus):
    if not RUN["versions"] and not RUN["seen_hosts"]:
        return
    try:
        out_dir = ROOT / "reports" / "runs" / datetime.date.today().isoformat()
        out_dir.mkdir(parents=True, exist_ok=True)
        summary = {
            "date": datetime.date.today().isoformat(),
            "sut_versions_seen": sorted(RUN["versions"]),
            "hosts_contacted": sorted(RUN["seen_hosts"]),
            "known_tracker_hosts": tracker_hosts(RUN["seen_hosts"]),
            "blocked_requests": RUN["blocked"],
            "exit_status": int(exitstatus),
        }
        (out_dir / "ui-summary.json").write_text(json.dumps(summary, indent=2))
    except OSError:
        pass
