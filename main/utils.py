from typing import Optional
import regex as re
import gzip
import requests
import csv


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return local_filename


def ipv4_to_int(ipv4: str) -> int:
    return sum(
        int(part) * (256 ** (3 - i)) for i, part in enumerate(ipv4.split('.'))
    )


def ipv6_to_int(ipv4: str) -> int:
    return sum(
        int(part, base=16) * ((16 ** 4) ** (7 - i)) for i, part in enumerate(ipv4.split(':'))
    )


def update_database():
    download_file("https://iptoasn.com/data/ip2asn-combined.tsv.gz")

def get_info(ip):
    with gzip.open('ip2asn-combined.tsv.gz', 'rt') as file:
        reader = csv.DictReader(file,
                                delimiter='\t',
                                fieldnames='range_start range_end AS_number country_code AS_description'.split())
        for line in reader:
            if line['range_start'] == ip:
                print(line)
                break
        else:
            print('No match for ip: {}'.format(ip))

def parse_trace_route_line(line: str) -> Optional[dict]:
    ipv4_regex = r'\.'.join(r'\d{1,3}' for _ in range(4))
    ipv6_regex = r':'.join(r'[0-9a-fA-F]{4}' for _ in range(8))

    trace_regexp = re.compile(r"""
        ^                                        # begin of line
        (?P<index>\d+)                           # index
        ([ ]?(?P<time>(\*|<?\d+[ ]ms))){1,}[ ]   # times
        ((?P<ipv4>%s)|(?P<ipv6>%s))              # ipv4 or ipv6
        $                                        # end of line
    """ % (ipv4_regex, ipv6_regex), re.VERBOSE)
    match = trace_regexp.match(line)
    if match:
        captures = match.capturesdict()
        captures['index'] = int(captures['index'][0])
        for ip_key in ['ipv4', 'ipv6']:
            if captures[ip_key]:
                captures[ip_key] = captures[ip_key][0]
            else:
                captures.pop(ip_key)
        return captures


if __name__ == '__main__':
    # update_database()
    get_info('8.8.8.0')
