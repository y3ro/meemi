# -*- coding: utf-8 -*-
import math
from math import sqrt
import sys
import fileinput
import gensim
from scipy import stats



def load_embeddings(embeddings_path):
    print('Loading embeddings:',embeddings_path)
    try:
        model=gensim.models.Word2Vec.load(embeddings_path)
    except:
        try:
            model=gensim.models.KeyedVectors.load_word2vec_format(embeddings_path)
        except:
            try:
                model=gensim.models.KeyedVectors.load_word2vec_format(embeddings_path,binary=True)
            except:
                sys.exit('Couldnt load embeddings')
    vocab=model.wv.index2word
    dims=model.__getitem__(vocab[0]).shape[0]
    vocab=set(vocab)
    return model,vocab,dims    


def module(vector):
    suma=0
    for dimension in vector:
        suma+=dimension*dimension
    return sqrt(suma)

def scalar_prod(vector1,vector2):
    prod=0
    for i in range(len(vector1)):
        dimension_1=vector1[i]
        dimension_2=vector2[i]
        prod+=dimension_1*dimension_2
    return prod

def cosine(vector1,vector2):
    return scalar_prod(vector1,vector2)/(module(vector1)*module(vector2))

if __name__ == '__main__':

    args=sys.argv[1:]

    if len(args)<3: sys.exit("Error: less than three arguments provided")
    embeddings_1=args[0]
    embeddings_2=args[1]
    print('Loading test embeddings 1')
    model_1,modelvocab_1,modeldims_1=load_embeddings(embeddings_1)
    print('Dimensions embeddings 1: '+str(modeldims_1))
    print('Loading test embeddings 2')
    model_2,modelvocab_2,modeldims_2=load_embeddings(embeddings_2)
    print('Dimensions embeddings 2: '+str(modeldims_2))
    print ("\n Done loading embeddings \n")

    for path_dataset in args[2:]:
        print ("\n ----------- \n Dataset "+path_dataset+"\n")
        dataset_file=open(path_dataset, encoding='utf-8').readlines()
        gold_list=[]
        output_list=[]
        for line in dataset_file:
            linesplit=line.strip().split("\t")
            word1=linesplit[0].lower()
            word2=linesplit[1].lower()
            gold=float(linesplit[2])
            gold_list.append(gold)
            if not model_1.wv.__contains__(word1) or not model_2.wv.__contains__(word2):
                output_list.append(0.5)
                continue
            vector_1=model_1.wv.__getitem__(word1)
            vector_2=model_2.wv.__getitem__(word2)
            sim=cosine(vector_1, vector_2)
            output_list.append(sim)

	
        scorr = stats.spearmanr(output_list, gold_list)
        pcorr = stats.pearsonr(output_list, gold_list)

        print ("Pearson correlation: "+str(round(pcorr[0]*100,1))+"%")
        print ("Spearman correlation: "+str(round(scorr[0]*100,1))+"%")

print ("\n Finished")



