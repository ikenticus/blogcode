import datetime
import tzlocal
import pytz
import sys

from pprint import pprint

def convert_timezone(timestamp, local_tz=tzlocal.get_localzone(), dest_tz=pytz.timezone('Europe/Amsterdam')):
    return local_tz.localize(timestamp).astimezone(dest_tz)

now = datetime.datetime.now()
print '\n%25s: %s' % ('Current time is', now)
print '%25s: %s' % ('UTC/GMT becomes', convert_timezone(now, dest_tz=pytz.utc))

if len(sys.argv) > 1:
    ask = sys.argv[1]
    if ask == 'common':
        print '\nCommon timezones:\n'
        pprint(pytz.common_timezones)
    elif ask == 'all':
        print '\nAll available timezones:\n'
        pprint(pytz.all_timezones)
    else:
        print '%25s: %s' % (sys.argv[1], convert_timezone(now, dest_tz=pytz.timezone(ask)))
else:
    print '\nYou can specify another timezone to convert of pass "all" or "common" to see examples\n'
