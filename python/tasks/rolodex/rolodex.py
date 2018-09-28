'''
    rolodex: main program to read and organize rolodex data
'''
import os
import sys

def read(args):
    import reader
    output = reader.read(args[0])
    outfile = os.path.splitext(args[0])[0] + '.json'
    reader.write(output, outfile)
    print 'Completed rolodex file: %s' % outfile

def test(args):
    import tester
    tester.test()

def usage(args=[]):
    print '''Usage: %s <action> [file]

    help    this usage screen
    read    read [file] data
    test    run unit tests
''' % os.path.basename(sys.argv[0])
    sys.exit(0)

if __name__ == "__main__":
    actions = {
        "help": usage,
        "read": read,
        "test": test,
    }

    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action in actions:
            actions[action](sys.argv[2:])
        else:
            usage()
    else:
        usage()
