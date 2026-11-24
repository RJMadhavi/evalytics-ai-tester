import socket
import unittest

from common.reachability import can_connect, target_from_url


class Targets(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(target_from_url("https://evalytics.in/pricing"), ("evalytics.in", 443))
        self.assertEqual(target_from_url("http://example.com"), ("example.com", 80))

    def test_explicit_port(self):
        self.assertEqual(target_from_url("http://localhost:8000/login"), ("localhost", 8000))


class Connect(unittest.TestCase):
    def test_open_port_is_reachable(self):
        with socket.socket() as server:
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            port = server.getsockname()[1]
            self.assertTrue(can_connect("127.0.0.1", port, 2.0))

    def test_closed_port_is_not_reachable(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        # the socket is closed now, so nothing listens on this port
        self.assertFalse(can_connect("127.0.0.1", port, 2.0))

    def test_bad_host_is_not_reachable(self):
        self.assertFalse(can_connect("no-such-host.invalid", 443, 2.0))


if __name__ == "__main__":
    unittest.main()
