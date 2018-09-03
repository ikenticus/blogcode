# Enter your code here. Read input from STDIN. Print output to STDOUT
T = int(raw_input())
for i in range(T):
    output = ['', '']
    S = raw_input()
    for c in range(len(S)):
        if c % 2 == 0:
            output[0] += S[c]
        else:
            output[1] += S[c]
    print ' '.join(output)


