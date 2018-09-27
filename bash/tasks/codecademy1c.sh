N=10
tmp=/tmp/1
url=https://gist.githubusercontent.com/jcs150/11e2b4c9cbf917f9cec3/raw/1b2e47c9761dbf2a971ec13b10b7a9997c3bd4f0/GistFile3
curl -o $tmp $url
cat $tmp | cut -d, -f3 | sort | uniq -c | sort -nr | head -$N
