import unittest

from main.utils import parse_trace_route_line, ipv4_to_int, ipv6_to_int


class TestUtils(unittest.TestCase):
    def test_parse_trace_route_line(self):
        log = """
Tracing route to any-fp.wa1.b.yahoo.com [209.191.122.70]
over a maximum of 30 hops:
1 <1 ms <1 ms <1 ms 10.1.0.1
2 29 ms 23 ms 20 ms 98.245.140.1
3 9 ms 16 ms 14 ms 68.85.105.201
4 *** 68.85.125.201
...
13 98 ms 77 ms 79 ms 209.191.78.131
14 80 ms 88 ms 89 ms 68.142.193.11
15 77 ms 79 ms 78 ms 209.191.122.70
16 77 ms 79 ms 78 ms 2001:0db8:85a3:0000:0000:8a2e:0370:7334
Trace complete.
"""
        actual = list(map(parse_trace_route_line, log.split('\n')))
        expected = [
            None,
            None,
            None,
            {'index': 1, 'time': ['<1 ms', '<1 ms', '<1 ms'], 'ipv4': '10.1.0.1'},
            {'index': 2, 'time': ['29 ms', '23 ms', '20 ms'], 'ipv4': '98.245.140.1'},
            {'index': 3, 'time': ['9 ms', '16 ms', '14 ms'], 'ipv4': '68.85.105.201'},
            {'index': 4, 'time': ['*', '*', '*'], 'ipv4': '68.85.125.201'},
            None,
            {'index': 13, 'time': ['98 ms', '77 ms', '79 ms'], 'ipv4': '209.191.78.131'},
            {'index': 14, 'time': ['80 ms', '88 ms', '89 ms'], 'ipv4': '68.142.193.11'},
            {'index': 15, 'time': ['77 ms', '79 ms', '78 ms'], 'ipv4': '209.191.122.70'},
            {'index': 16, 'time': ['77 ms', '79 ms', '78 ms'], 'ipv6': '2001:0db8:85a3:0000:0000:8a2e:0370:7334'},
            None,
            None,
        ]

        self.assertEqual(actual, expected)

    def test_ipv4_to_int(self):
        ip = '185.204.1.185'
        expected = 3117154745
        self.assertEqual(ipv4_to_int(ip), expected)

    def test_ipv6_to_int(self):
        ip = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        expected = 42540766452641154071740215577757643572
        self.assertEqual(ipv6_to_int(ip), expected)
