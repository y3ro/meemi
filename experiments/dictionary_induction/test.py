import sys, gensim
import numpy as np
import torch

models = [gensim.models.KeyedVectors.load_word2vec_format(arg, binary=arg.endswith(".bin")) for arg in sys.argv[1:]]

crit1_sum = 0
crit2_sum = 0
hits1 = 0
hits5 = 0
hits10 = 0
n = 0

for i, line in enumerate(sys.stdin):
    words = line.strip().split(" ")
    if len(words) != len(models):
        sys.stderr.write("Number of models and words not matching at line " + str(i) + "!\n")
        continue
    try:
        emb = models[0][words[0]]
        nn10 = [x[0] for x in models[-1].similar_by_vector(np.array(emb))]
        nn5 = nn10[:5]
        nn1 = [nn10[0]]
        if words[-1] in nn1:
            hits1 += 1
            # sys.stderr.write("FOUND: " + words[-1] + " in NN1: " + " ".join(nn1) + "\n")
        # else:
            # sys.stderr.write("NOT FOUND: " + words[-1] + " in NN1: " + " ".join(nn1) + "\n")
        if words[-1] in nn5:
            hits5 += 1
            # sys.stderr.write("FOUND: " + words[-1] + " in NN5: " + " ".join(nn5) + "\n")
        # else:
            # sys.stderr.write("NOT FOUND: " + words[-1] + " in NN5: " + " ".join(nn5) + "\n")
        if words[-1] in nn10:
            hits10 += 1
            # sys.stderr.write("FOUND: " + words[-1] + " in NN10: " + " ".join(nn10) + "\n")
        # else:
            # sys.stderr.write("NOT FOUND: " + words[-1] + " in NN10: " + " ".join(nn10) + "\n")
        n += 1
    except KeyError:
        continue
print("induction P@1: " + str(hits1/float(n)) + " induction P@5: " + str(hits5/float(n)) + " induction P@10: " + str(hits10/float(n)))
