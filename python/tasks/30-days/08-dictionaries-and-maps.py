# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(raw_input())
entry = {}
for i in range(n):
    e = raw_input().split(' ')
    entry[e[0]] = e[1]
    
while True:
    q = raw_input()
    # Using entry.keys() times out for Testcase(s) 1-3
    #print '%s=%s' % (q, entry[q]) if q in entry.keys() else 'Not found'
    print '%s=%s' % (q, entry[q]) if q in entry else 'Not found'

