import csv
import sys
import logging


class Writer:
    def __init__(self):
        self._writer = csv.DictWriter(sys.stdout, ['index', 'ip', 'as', 'country', 'isp'],
                                      delimiter='\t')
        self._writer.writeheader()

    def write_line(self, trace_info, db_info):
        logging.debug('Writing line: trace_info=`{}`, db_info={}'.format(trace_info, db_info))
        row = {
            'index': trace_info['index'],
            'ip': (trace_info.get('ipv4') or trace_info.get('ipv6') or trace_info.get('error')),
            'as': (db_info.get('as') or ''),
            'country': db_info.get('country') if str(db_info.get('country')) != 'None' else '',
            'isp': (db_info.get('isp') or '')
        }

        self._writer.writerow(row)
