
'''
    Splice one file into many
    - match line on cfg_pre
    - split line by cfg_sep
    - use index cfg_idx for output filename
    
'''

import os
import sys

from pprint import pprint

cfg_idx = 1
cfg_sep = '"'
cfg_pre = 'job('
cfg_out = 'output'

def splice(data, outdir, ext):
    name = None
    for d in data:
        #print(d, end='')
        if d.startswith(cfg_pre):
            name = d.split(cfg_sep)[cfg_idx]
        if name:
            file = open('%s/%s.%s' % (outdir, name, ext), 'a')
            file.write(d)
            file.close()
    
def main():
    """
    Entry point of the program when called as a script.
    """
    if len(sys.argv) > 1:
        input = sys.argv[1]
    else:
        print('Usage: %s <large-file>' % os.path.basename(sys.argv[0]))
        exit()

    file = open(input)
    data = file.readlines()
    file.close()

    outdir = '%s/%s' % (os.path.dirname(input), cfg_out)
    #print(outdir)
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    #pprint(data)
    ext = input.split('.')[-1]
    splice(data, outdir, ext)

if __name__ == '__main__':
    main()
