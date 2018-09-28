# Rolodex

Script to read in a comma-separated file (CSV) with patterns defined by a config file in order to generate an alphabetical rolodex of entries (as well as a list of line indices representing errors in the origin CSV)

## Usage

For help, just run: `python rolodex.py`

For unit testing, run: `python rolodex.py test`

Using the included sample, generating a rolodex: `python rolodex.py read data.in` would output a corresponding `data.json`
