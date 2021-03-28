from typing import Optional
import regex as re
import logging

IPV4_REGEX = r'\.'.join(r'\d{1,3}' for _ in range(4))
IPV6_REGEX = r'[0-9a-fA-F:]+'


def ipv4_to_int(ipv4: str) -> Optional[int]:
    if re.match(IPV4_REGEX, ipv4):
        return sum(
            int(part) * (256 ** (3 - i)) for i, part in enumerate(ipv4.split('.'))
        )


def ipv6_to_int(ipv6: str) -> Optional[int]:
    if ipv6 == '::':
        return 0
    elif ipv6 == '::1':
        return 1
    if '::' in ipv6:
        left, right = ipv6.split('::', maxsplit=1)
        colon_cnt = ipv6.count(':')

        new_ipv6 = '{}:{}:{}'.format(left or '0',
                                     ':'.join('0' for _ in range(8 - colon_cnt)),
                                     right or '0')
        logging.debug('Decompressed {} into {}'.format(ipv6, new_ipv6))
        ipv6 = new_ipv6

    if re.match(IPV6_REGEX, ipv6):
        return sum(
            int(part, base=16) * ((16 ** 4) ** (7 - i)) for i, part in enumerate(ipv6.split(':'))
        )
