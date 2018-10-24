# -*- coding: utf-8 -*-
# Rank metrics from https://gist.github.com/bwhite/3726239
import sys
import numpy as np

def mean_reciprocal_rank(r):
    """Score is reciprocal of the rank of the first relevant item
    First element is 'rank 1'.  Relevance is binary (nonzero is relevant).
    Example from http://en.wikipedia.org/wiki/Mean_reciprocal_rank
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Mean reciprocal rank
    """
    r = np.asarray(r).nonzero()[0]
    return 1. / (r[0] + 1) if r.size else 0.



def precision_at_k(r, k, n):
    """Score is precision @ k
    Relevance is binary (nonzero is relevant).
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Precision @ k
    Raises:
        ValueError: len(r) must be >= k
    """
    assert k >= 1
    r = np.asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    return (np.mean(r)*k)/min(k,n)
    # Modified from the first version. Now the gold elements are taken into account


def average_precision(r,n):
    """Score is average precision (area under PR curve)
    Relevance is binary (nonzero is relevant).
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Average precision
    """
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1, n) for k in range(r.size)]
    #Modified from the first version (removed "if r[k]"). All elements (zero and nonzero) are taken into account
    if not out:
        return 0.
    return np.mean(out)


def mean_average_precision(r,n):
    """Score is mean average precision
    Relevance is binary (nonzero is relevant).
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Mean average precision
    """
    return average_precision(r,n)


def get_hypernyms(line, is_gold=True):
    if is_gold == True:
        valid_hyps = line.strip().split('\t')
        return valid_hyps
    else:
        linesplit=line.strip().split('\t')
        cand_hyps=[]
        for hyp in linesplit[:limit]:
            hyp_lower=hyp.lower()
            if hyp_lower not in cand_hyps: cand_hyps.append(hyp_lower)
        return cand_hyps

if __name__ == '__main__':

    args = sys.argv[1:]

    if len(args) == 2:

        limit=15
        gold = args[0]
        predictions = args[1]

        fgold = open(gold, 'r')
        fpredictions = open(predictions, 'r')

        goldls = fgold.readlines()
        predls = fpredictions.readlines()

        if len(goldls)!=len(predls): sys.exit('ERROR: Number of lines in gold and output files differ')

        all_scores = []
        scores_names = ['MRR', 'MAP', 'P@1', 'P@3', 'P@5', 'P@15']
        for i in range(len(goldls)):

            goldline = goldls[i]
            predline = predls[i]
            
            avg_pat1 = []
            avg_pat2 = []
            avg_pat3 = []
            avg_pat4 = []


            gold_hyps = get_hypernyms(goldline, is_gold=True)
            pred_hyps = get_hypernyms(predline, is_gold=False)
            gold_hyps_n = len(gold_hyps)
            r = [0 for i in range(limit)]

            for j in range(len(pred_hyps)):
                if j < gold_hyps_n:
                    pred_hyp = pred_hyps[j]
                    if pred_hyp in gold_hyps:
                        r[j] = 1

            avg_pat1.append(precision_at_k(r,1,gold_hyps_n))
            avg_pat2.append(precision_at_k(r,3,gold_hyps_n))
            avg_pat3.append(precision_at_k(r,5,gold_hyps_n))
            avg_pat4.append(precision_at_k(r,15,gold_hyps_n))


            mrr_score_numb = mean_reciprocal_rank(r)
            map_score_numb = mean_average_precision(r,gold_hyps_n)
            avg_pat1_numb = sum(avg_pat1)/len(avg_pat1)
            avg_pat2_numb = sum(avg_pat2)/len(avg_pat2)
            avg_pat3_numb = sum(avg_pat3)/len(avg_pat3)
            avg_pat4_numb = sum(avg_pat4)/len(avg_pat4)
            
            scores_results = [mrr_score_numb, map_score_numb, avg_pat1_numb, avg_pat2_numb, avg_pat3_numb, avg_pat4_numb]        
            all_scores.append(scores_results)


        print('Results for gold file: ',gold,' and predictions: ',predictions)
        for k in range(len(scores_names)):
            print( scores_names[k]+': '+str(sum([score_list[k] for score_list in all_scores]) / len(all_scores)))
    else:
        sys.exit('Argument: (1) Gold file; (2) Predictions file')
