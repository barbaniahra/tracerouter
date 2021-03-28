from typing import Optional
import regex as re
import io
from main.ip_utils import IPV4_REGEX, IPV6_REGEX
import subprocess
import logging


class TraceRT:
    def __init__(self, tracert_command: str):
        self._tracert_command = tracert_command

    def trace(self, resource: str):
        process = subprocess.Popen([self._tracert_command, '-d', resource],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        stdout = []
        for line in io.TextIOWrapper(process.stdout, encoding="utf8"):
            stdout.append(line)
            logging.debug('Attempting to parse line: `{}`'.format(line))
            parsed = self._parse_trace_route_line(line)
            logging.debug('Line parsed as: `{}`'.format(parsed))
            if parsed:
                yield parsed

        return_code = process.poll()
        if return_code is None:
            return_code = process.returncode
        logging.debug('Return code: {}'.format(return_code))
        if return_code != 0:
            raise Exception('tracert finished with non-zero code: {}, stderr: `{}`, stdout: `{}`'.format(
                return_code, process.stderr.read().decode('utf8'), ''.join(stdout)))

    @staticmethod
    def _parse_trace_route_line(line: str) -> Optional[dict]:
        trace_regexp = re.compile(r"""
            ^                                           # begin of line
            \s*                                         # maybe some whitespaces
            (?P<index>\d+)                              # index
            (\s*(?P<time>(\*|<?\d+\s+ms))){1,}          # times
            \s*                                         # maybe some whitespaces
            ((?P<ipv4>%s)|(?P<ipv6>%s)|(?P<error>.*))   # ipv4 or ipv6
            \s*                                         # maybe some whitespaces
            $                                           # end of line
        """ % (IPV4_REGEX, IPV6_REGEX), re.VERBOSE)

        match = trace_regexp.match(line)
        if match:
            captures = match.capturesdict()
            captures['index'] = int(captures['index'][0])
            for ip_key in ['ipv4', 'ipv6', 'error']:
                if captures[ip_key]:
                    captures[ip_key] = captures[ip_key][0]
                else:
                    captures.pop(ip_key)
            return captures
