import yaml

settings = yaml.safe_load('''
    alpha: this is a string
    beta:
        - this
        - is
        - a
        - list
    gamma:
        one: 1
        two: 2
        tre: 3
        six: 6
        sep: 7
        oct: 8
    delta:
        - one: 1
          two: 2
          tre: 3
        - six: 6
          sep: 7
          oct: 8
''')


# https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
'''
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

cfg = Struct(**settings)
'''

class dict2obj(dict):
    def __init__(self, dict_):
        super(dict2obj, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    if isinstance(it, dict):
                        item[idx] = dict2obj(it)
            elif isinstance(item, dict):
                self[key] = dict2obj(item)

    def __getattr__(self, key):
        return self[key]

cfg = dict2obj(settings)


print(settings)
print(settings.keys())
print(cfg)
print(cfg.keys())

for k in settings.keys():
    print(k, getattr(cfg, k))

print('alpha:', cfg.alpha)
print('beta.-1:', cfg.beta[-1])
print('gamma.one:', cfg.gamma.one)
print('delta.1.six:', cfg.delta[1].six)
