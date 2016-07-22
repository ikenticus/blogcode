import datetime
import tzlocal
import pytz
import sys

def convert_timezone(timestamp, local_tz=tzlocal.get_localzone(), dest_tz=pytz.timezone('Europe/Amsterdam')):
    return local_tz.localize(timestamp).astimezone(dest_tz)

now = datetime.datetime.now()
print '%25s: %s' % ('Current time is', now)
print '%25s: %s' % ('UTC/GMT becomes', convert_timezone(now, dest_tz=pytz.utc))

if len(sys.argv) > 1:
    print '%25s: %s' % (sys.argv[1], convert_timezone(now, dest_tz=pytz.timezone(sys.argv[1])))
