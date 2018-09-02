def print_rangoli(size):
    # your code goes here
    import string
    alpha = string.ascii_lowercase

    pattern = []
    w = 4 * size - 3
    for i in range(size):
        p = '-'.join(alpha[i:size])
        pattern.append((p[::-1]+p[1:]).center(w, '-'))
    print '\n'.join(pattern[::-1] + pattern[1:])

if __name__ == '__main__':
    n = int(raw_input())
    print_rangoli(n)
