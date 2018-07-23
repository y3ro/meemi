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
crit1 = torch.dot
crit2 = torch.nn.MSELoss()
not_found = 0

for i, line in enumerate(sys.stdin):
    words = line.strip().split(" ")
    if len(words) != len(models):
        sys.stderr.write("Number of models and words not matching at line " + str(i) + "!\n")
        continue
    try:
        crit1_sum += crit1(*[torch.autograd.Variable(torch.Tensor(x)) / torch.autograd.Variable(torch.Tensor(x)).norm() 
            for x in [model[word] for word, model in zip(words, models)]])
        crit2_sum += crit2(*[torch.autograd.Variable(torch.Tensor(x))
            for x in [model[word] for word, model in zip(words, models)]])
        emb = models[0][words[0]]
        nn1 = set([models[-1].similar_by_vector(np.array(emb))[0][0]])
        nn5 = set(x[0] for x in models[-1].similar_by_vector(np.array(emb))[:5])
        nn10 = set(x[0] for x in models[-1].similar_by_vector(np.array(emb)))
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
        not_found += 1
        continue
print("MSE: " + str((crit2_sum/float(n)).data[0]) + " cos: " + str((crit1_sum/float(n)).data[0]) + " induction P@1: " + str(hits1/float(n)) + " induction P@5: " + str(hits5/float(n)) + " induction P@10: " + str(hits10/float(n)) + " OOV%: " + str(not_found/float(n)))
