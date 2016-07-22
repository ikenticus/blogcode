'''
    Really useful getattr/setattr for use with dot-notation
    especially since pure dot-notation does not allow numbers
'''

output = {
    'page': {
        '20120727': [ 1, 2, 3, 4 ]
    }
}

def dot_object(obj, dot, value=False):
    '''
    dot_object(obj, '1.2.3', [value]): deep get/set object using dot-notation
    '''
    if isinstance(dot, basestring):
        return dot_object(obj, dot.split('.'), value)
    elif len(dot) == 1 and value is not False:
        if isinstance(obj, list):
            key = int(dot[0])
            if key >= len(obj):
                for i in range(len(obj), key):
                    obj.insert(i, None)
                obj.insert(key, value)
            else:
                obj[key] = value
        else:
            obj[dot[0]] = value
        return obj
    elif len(dot) == 0:
        return obj
    else:
        if isinstance(obj, list):
            key = int(dot[0])
            if key >= len(obj):
                return None
        else:
            key = dot[0]
            if key not in obj.keys():
                return None
        return dot_object(obj[key], dot[1:], value)

print output
print 'output -> page.20120727.1 =', dot_object(output, 'page.20120727.1')
print 'output -> page.20120727.7 =', dot_object(output, 'page.20120727.7')
print 'output -> page.20120728 =', dot_object(output, 'page.20120728')

dot_object(output, 'page.20120727.6', 6);
print 'setting output -> page.20120727.6 to 6:\n', output

dot_object(output, 'page.20120727.2', 9)
print 'setting output -> page.20120727.2 to 9\n', output

dot_object(output, 'page.20120727.3', [])
print 'setting output -> page.20120727.3 to []:\n', output

dot_object(output, 'page.20120727.4', {})
print 'setting output -> page.20120727.4 to {}:\n', output

dot_object(output, 'page.20120728', [4, 5, 6])
print 'setting output -> page.20120728 to [list]:\n', output

output['test'] = {};
dot_object(output, 'test.a', 1);
dot_object(output, 'test.b', 1);
print 'setting output.test -> {a, b}:\n', output
