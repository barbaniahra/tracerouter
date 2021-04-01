# TraceRouter
## Installation
`python3 -m pip install .`

## Examples
To trace route to resource just use `tracerouter RESOURCE`, e.g.:
- `tracerouter yandex.ru`:
```
index   ip      as      country isp
1       192.168.0.1                     Not routed
2       213.242.203.70  3253    RU      SOVINTEL-EF-AS
3       195.58.0.46     3253    RU      SOVINTEL-EF-AS
4       87.254.133.197  3216    RU      SOVAM-AS
5       79.104.235.213                  Not routed
6       195.239.153.234 3216    RU      SOVAM-AS
7       Request timed out.
8       5.255.255.60    13238   RU      YANDEX
```

- `tracerouter 8.8.8.8`:
```
index   ip      as      country isp
1       192.168.0.1                     Not routed
2       213.242.203.70  3253    RU      SOVINTEL-EF-AS
3       195.58.0.34     3253    RU      SOVINTEL-EF-AS
4       87.254.133.197  3216    RU      SOVAM-AS
5       79.104.225.13                   Not routed
6       81.211.29.103   3216    RU      SOVAM-AS
7       108.170.250.130 15169   US      GOOGLE - Google LLC
8       216.239.50.132  15169   US      GOOGLE - Google LLC
9       172.253.66.108  15169   US      GOOGLE - Google LLC
10      142.250.238.179 15169   US      GOOGLE - Google LLC
11      Request timed out.
12      Request timed out.
13      Request timed out.
14      Request timed out.
15      Request timed out.
16      Request timed out.
17      Request timed out.
18      Request timed out.
19      Request timed out.
20      8.8.8.8 3356    US      LEVEL3 - Level 3 Communications, Inc.
```
## Full usage (`tracerouter --help`):
```
usage: tracerouter [-h] [-c CONFIG] [--db_path DB_PATH] --db_url DB_URL --db_expiration_seconds DB_EXPIRATION_SECONDS --tracert_command TRACERT_COMMAND --logging_level LOGGING_LEVEL resource

positional arguments:
  resource              IP or domain of the resource to traceroute to

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path
  --db_path DB_PATH     Path to database TSV file
  --db_url DB_URL       Url of TSV file
  --db_expiration_seconds DB_EXPIRATION_SECONDS
                        How long before updating the DB
  --tracert_command TRACERT_COMMAND
                        TraceRT command or path
  --logging_level LOGGING_LEVEL
                        Logging level
```