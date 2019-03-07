import re
import requests

res = requests.get('http://myexternalip.com')
print(re.sub(r'^.+<title>(.+)</title>.+$', r'\1', str(res.content)))
