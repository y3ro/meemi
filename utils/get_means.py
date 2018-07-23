import sys, gensim
import numpy as np
import re

models = [gensim.models.KeyedVectors.load_word2vec_format(arg, binary=arg.endswith(".bin")) for arg in sys.argv[1:]]

def default_get(x, d):
    try:
        return d[x]
    except KeyError:
        return []

def get_mean(words, models):
    all_vectors = [default_get(word, model) for word, model in zip(words, models) if default_get(word, model) is not None]
    return [np.mean(x) for x in zip(*all_vectors)]

def zip_rep(words, vector):
    rep_vector = [vector for i in range(0, len(words))]
    return zip(words, rep_vector)

for i, line in enumerate(sys.stdin):
    words = line.strip().split(" ")
    if len(words) != len(models):
        sys.stderr.write("Number of models and words not matching at line " + str(i) + "! " + str(len(words)) + " " + str(len(models)) + "\n")
        continue
    s = [" ".join([word] + [str(x) for x in vector]) for word, vector in zip_rep(words, get_mean(words, models))]
    lengths = [x.strip().split() for x in s]
    lengths_condition = [len(x) > 3 for x in lengths]
    if all(lengths_condition):
        print("\t".join(s))
