import xxhash

word = 'teamstats_mlb_2017_2973'
seed = 0

print(xxhash.xxh64(word).hexdigest())
print(xxhash.xxh64(word, seed=seed).hexdigest())
print(xxhash.xxh64(word, seed=seed).intdigest())
print(xxhash.xxh64(word).intdigest())
