import os
import gzip
import requests
import csv
from datetime import datetime, timedelta
from main.ip_utils import ipv4_to_int, ipv6_to_int
import logging


class DB:
    def __init__(self, db_path: str, db_url: str, db_expiration_seconds: int):
        self._db_path = db_path
        self._db_url = db_url
        self._db_expiration_seconds = db_expiration_seconds
        self.update_database()

    def _db_file_exists(self):
        return os.path.exists(self._db_path)

    def _db_file_is_too_old(self):
        if self._db_file_exists():
            last_modified = datetime.fromtimestamp(os.path.getmtime(self._db_path))
            return datetime.now() - last_modified >= timedelta(seconds=self._db_expiration_seconds)

    def update_database(self, force_update: bool = False):
        if (force_update
                or not self._db_file_exists()
                or self._db_file_is_too_old()):
            logging.info('Starting updating DB')
            try:
                self._download_file()
                logging.info('DB updated')
            except requests.exceptions.RequestException as e:
                logging.warning('Unable to update DB, error: `{}`, {}'.format(
                    e, 'will continue with older version' if self._db_file_exists() else 'will not show find info'))
        else:
            logging.info('No need to update DB')

    def _download_file(self):
        # NOTE the stream=True parameter below
        with requests.get(self._db_url, stream=True) as r:
            r.raise_for_status()
            with open(self._db_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    @staticmethod
    def _ipv4_to_int(ipv4: str) -> int:
        return sum(
            int(part) * (256 ** (3 - i)) for i, part in enumerate(ipv4.split('.'))
        )

    @staticmethod
    def _ipv6_to_int(ipv4: str) -> int:
        return sum(
            int(part, base=16) * ((16 ** 4) ** (7 - i)) for i, part in enumerate(ipv4.split(':'))
        )

    def get_info(self, ip) -> dict:
        if not self._db_file_exists():
            logging.debug('No DB file found - returning no results')
            return {}

        if ipv4_to_int(ip) is not None:
            ip_int = ipv4_to_int(ip)
            parse_foo = ipv4_to_int
        elif ipv6_to_int(ip) is not None:
            ip_int = ipv6_to_int(ip)
            parse_foo = ipv6_to_int
        else:
            logging.warning('Not supported ip: {}, returning without lookup'.format(ip))
            return {}

        with gzip.open(self._db_path, 'rt', encoding='utf8') as file:
            reader = csv.DictReader(file,
                                    delimiter='\t',
                                    fieldnames='range_start range_end AS_number country_code AS_description'.split())
            for line in reader:
                range_start = line['range_start']
                range_end = line['range_end']
                AS_number = int(line['AS_number'])
                country_code = line['country_code']
                AS_description = line['AS_description']

                if parse_foo(range_start) is None or parse_foo(range_end) is None:
                    continue

                if parse_foo(range_start) <= ip_int <= parse_foo(range_end):
                    #if AS_number != 0:  # non-routable addresses
                        return {
                            'as': AS_number,
                            'country': country_code,
                            'isp': AS_description
                        }

        return {}
