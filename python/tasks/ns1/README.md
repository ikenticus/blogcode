# DNS Importer

Script to read in a comma-separated file (CSV) and import it into NS1. With twisted transport, all of the NS1 methods return Deferred.
Yield them to gather the results, then add callbacks/errrorbacks to retrieve results/failures when available.

## Configure

By default, the tool will load configuration from `~/.nsone`, use the `nsone.sample` for guidance.

The `config.loadFromFile(Config.DEFAULT_CONFIG_FILE)` will allow loading a configuration file from an alternative location or a configuration file can be generate using just the API key `config.createFromAPIKey('YourAPIKey')`

## Usage

By default, to import `dns-importer.csv`, just run: `python dns-importer.py`

To load other CSV data: `python dns-importer.py [csv-file]`, which is the usage message displayed if the `csv-file` does not exist.
