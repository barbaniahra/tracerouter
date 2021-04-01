# TraceRouter
## Installation
`python3 -m pip install .`

## Examples
To trace route to resource just use `python -m main.tracerouter RESOURCE`, e.g.:
- `python -m main.tracerouter google.com`
- `python -m main.tracerouter 8.8.8.8`

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