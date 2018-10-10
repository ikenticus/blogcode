============
DNS Importer
============

:Info: A Python script to read in a comma-separated (CSV) file and import it into NS1, the Data Driven DNS platform.


About
=====

This script uses the NS1 python SDK to access the NS1 DNS platform and
add records listed in a comma-separated (CSV) file asynchronously
using twisted transport.

Currently version supports python 2.7 due to API limitations.
Future versions will support python3 once the issues are resolved.


Dependencies
============

* Install and activate your favorite "virtualenv" or "pyenv"
* Install dependencies:

  ::

    pip install ns1-python pyOpenSSL service_identity twisted


Usage
=====

By default, to import "dns-importer.csv" just run:

::

  python dns-importer.py

To load other CSV data:

::

  python dns-importer.py [csv-file]

which is the usage message displayed if the `csv-file` does not exist.


Notes
=====

This script will NOT currently handle the following:

* Removing any existing answers for the NS1 zone records previously imported
* Resolving inconsistent TTLs in repeated lines within the CSV (need to define rules)
* Creation of non-existing zones (can be added, but was omitted for security reasons)


Troubleshooting
===============

* If twisted returns certificate failures:

  ::

    [Failure instance: Traceback: <class 'ns1.rest.errors.ResourceException'>: [<twisted.python.failure.Failure OpenSSL.SSL.Error: [('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')]>]

  the following should fix the issue:

  ::

    pip install certifi
    export SSL_CERT_FILE="$(python -m certifi)"
