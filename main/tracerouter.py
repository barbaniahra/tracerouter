import sys
import os
import configargparse
from main.db import DB
from main.tracert import TraceRT
from main.writer import Writer
import logging

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, '..', 'resources'))

def set_logging_level(level):
    root = logging.getLogger()
    root.setLevel(logging.getLevelName(level))

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.getLevelName(level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

def parse_args(argv):
    p = configargparse.ArgParser(default_config_files=[os.path.join(RESOURCE_DIRECTORY, 'config.ini')])
    p.add_argument('-c', '--config', required=False, is_config_file=True, help='Config file path')
    p.add_argument('--db_path', required=False, help='Path to database TSV file',
                   default=os.path.join(os.path.join(RESOURCE_DIRECTORY, 'db.tcv.gz')))
    p.add_argument('--db_url', required=True, help='Url of TSV file')
    p.add_argument('--db_expiration_seconds', type=int, required=True, help='How long before updating the DB')
    p.add_argument('--tracert_command', required=True, help='TraceRT command or path')
    p.add_argument('--logging_level', required=True, help='Logging level')
    p.add_argument('resource', help='IP or domain of the resource to traceroute to')
    return p.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    set_logging_level(args.logging_level)
    db = DB(db_path=args.db_path, db_url=args.db_url, db_expiration_seconds=args.db_expiration_seconds)
    tracert = TraceRT(tracert_command=args.tracert_command)
    writer = Writer()
    logging.info('Starting tracing to {}'.format(args.resource))
    for trace_info in tracert.trace(args.resource):
        if trace_info:
            lookup_info = {}

            ip = (trace_info.get('ipv4') or trace_info.get('ipv6'))
            if ip is not None:
                lookup_info = db.get_info(ip)

            writer.write_line(trace_info, lookup_info)
    logging.info('Tracing finished')
