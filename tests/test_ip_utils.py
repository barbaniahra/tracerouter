import unittest

from main.tracerouter import set_logging_level
from main.ip_utils import ipv4_to_int, ipv6_to_int


class TestIPUtils(unittest.TestCase):
    def setUpClass() -> None:
        set_logging_level('DEBUG')

    def test_ipv4_to_int(self):
        ip = '185.204.1.185'
        expected = 3117154745
        self.assertEqual(ipv4_to_int(ip), expected)

    def test_ipv6_to_int(self):
        ip = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        expected = 42540766452641154071740215577757643572
        self.assertEqual(ipv6_to_int(ip), expected)

    def test_ipv6_compressions(self):
        self.assertEqual(ipv6_to_int('::'), 0)
        self.assertEqual(ipv6_to_int('::1'), 1)
        self.assertEqual(ipv6_to_int('1:1::1'), ipv6_to_int('1:1:0:0:0:0:0:1'))
        self.assertEqual(ipv6_to_int('1::1:1:1:1:1:1'), ipv6_to_int('1:0:1:1:1:1:1:1'))
