# https://en.wikipedia.org/wiki/Functional_programming#Python
print '-' * 22

# Printing first 10 Fibonacci numbers, iterative
def iterative(n, first=0, second=1):
    for _ in range(n):
        print(first), # side-effect
        first, second = second, first + second # assignment
iterative(10)
print


# Printing first 10 Fibonacci numbers, functional expression style
functional = (lambda n, first=0, second=1:
    "" if n == 0 else
    str(first) + " " + functional(n - 1, second, first + second))
#print(functional(10), end="") # python3 syntax
print functional(10)


# Printing a list with first 10 Fibonacci numbers, with generators
def generator(n, first=0, second=1):
    for _ in range(n):
        yield str(first)
        first, second = second, first + second # assignment
print(' '.join(list(generator(10))))


# Printing a list with first 10 Fibonacci numbers, functional expression style
funclist = (lambda n, first=0, second=1:
    [] if n == 0 else
    [first] + funclist(n - 1, second, first + second))
print(' '.join([str(f) for f in funclist(10)]))


# Printing first 10 Fibonacci numbers, recursive style
def recursive(n):
    if n <= 1:
        return n
    else:
        return recursive(n-2) + recursive(n-1)
for n in range(10):
    print(recursive(n)),

