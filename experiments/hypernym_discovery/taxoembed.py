import os
import sys
import gensim
import logging
import numpy as np
from collections import defaultdict
from argparse import ArgumentParser

# Returns list of topn most similar vectors
def msv(self, vectenter, topn=5):
    self.init_sims()
    dists = np.dot(self.wv.syn0norm , vectenter)
    if not topn:
        return dists
    best = np.argsort(dists)[::-1][:topn]
    result = [(self.wv.index2word[sim], float(dists[sim])) for sim in best]
    return result[:topn]

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

if __name__ == '__main__':

	args=sys.argv[1:]

	parser = ArgumentParser()
	# Word vectors for training hypernymy model
	parser.add_argument('-wvtrain','--vectors-train', help='Embeddings train file', required=True)
	# Word vectors for test model
	parser.add_argument('-wvtest','--vectors-test', help='Embeddings test file', required=True)
	# Test vocabulary file, important for filtering out OOV candidate hypernyms
	parser.add_argument('-vtest','--vocabulary-test', help='Semeval test vocabulary', required=True)
	parser.add_argument('-hypotrain','--hyponyms-train', help='Semeval train hyponyms', required=True)
	parser.add_argument('-hypertrain','--hypernyms-train', help='Semeval train hypernyms', required=True)
	parser.add_argument('-test','--test-file', help='Semeval test file', required=True)
	# Output folder where both outputs (linear regression and svd factorized matrix) are saved
	parser.add_argument('-o','--output', help='Output path', required=True)
	###
	# Additional (language-specific) training data files
	parser.add_argument('-newtrain','--newtrain', help='Additional (ES or IT) training hyponym-hypernym pairs (pre extracted)', required=False)
	parser.add_argument('-npairs','--npairs', help='Number of hyponym-hypernym pairs to be used for additional training', required=False)

	args = vars(parser.parse_args())

	embeddings_train=args['vectors_train']
	embeddings_test=args['vectors_test']
	vocabulary_test=args['vocabulary_test']
	hyponyms_train=args['hyponyms_train']
	hypernyms_train=args['hypernyms_train']
	test_file=args['test_file']

	# Train with ENGLISH data
	print('Loading train embeddings')
	model,modelvocab,modeldims=load_embeddings(embeddings_train)
	print('Loading test embeddings')
	modeltest,modeltestvocab,modeltestdims=load_embeddings(embeddings_test)

	print('Loading test vocabulary')
	vocab_test=[]
	for line in open(vocabulary_test,'r'):
		if len(line.strip().split()) == 1:
			vocab_test.append(line.strip())

	print('Reading training data') # check casing
	hypos=[]
	for line in open(hyponyms_train,'r'):
		hypo=line.strip().split('\t')[0].lower()
		hypos.append(hypo)

	print('Loaded ',len(hypos),' hyponyms')

	pairs=[]
	for idx,line in enumerate(open(hypernyms_train,'r').readlines()):
		cols=line.strip().split('\t')
		for h in cols:
			pairs.append((hypos[idx],h))

	print('Loaded ',len(pairs),' hyponym-hypernym pairs')
	orig_pairs=len(pairs)
	### Add extra training data ###
	if args['npairs']:
		npairs=int(args['npairs'])
		for line in open(args['newtrain'],'r').readlines()[:npairs]:
			newpair=(line.strip().split()[0],line.strip().split()[1])
			#print('Adding new training pair: ',newpair)
			pairs.append(newpair)
		print('After language specific augmentation, loaded ',len(pairs),' hyponym-hypernym pairs')

	hypos_matrix=[]
	hypers_matrix=[]

	print('Collecting vector pairs')
	pair_counter=0
	for hypo,hyper in pairs:
		if pair_counter > orig_pairs:
			model=modeltest
		pair_counter+=1
		if model.wv.__contains__(hypo) and model.wv.__contains__(hyper):
			#print('Train pair: ',hypo,hyper)
			hypos_matrix.append(model.wv.__getitem__(hypo))
			hypers_matrix.append(model.wv.__getitem__(hyper))
		else:
			#print(hypo,hyper)
			avg_hypo=[]
			avg_hyper=[]
			for w in hypo.split():
				if model.wv.__contains__(w):
					#print(w,' in model')
					avg_hypo.append(model.wv.__getitem__(w))
			for w in hyper.split():
				if model.wv.__contains__(w):
					#print(w,' in model')
					avg_hyper.append(model.wv.__getitem__(w))
			if avg_hypo and avg_hyper:
				avg_hypo=np.mean(np.array(avg_hypo),axis=0)	
				avg_hyper=np.mean(np.array(avg_hyper),axis=0)
				hypos_matrix.append(avg_hypo)
				hypers_matrix.append(avg_hyper)

	print('From ',len(pairs),' pairs')
	print(len(hypos_matrix),len(hypers_matrix),' training examples collected')

	print('Training matrix and model')
	W = np.linalg.pinv(np.array(hypos_matrix)).dot(np.array(hypers_matrix)).T
	print('Matrix shape: ',W.shape)

	# Check casing of input hyponym
	count=0
	res=[]
	res_lr=[]
	testlines=open(test_file,'r').readlines()
	for idx,line in enumerate(testlines):
		count+=1
		hypo=line.strip().split('\t')[0].lower()
		if count % 100 == 0:
			print('Predicted ',count,' instances of ',len(testlines))
			print('Example - For word ',hypo,' | Found hypernyms: ',cands)
		if modeltest.wv.__contains__(hypo):
			cands=[]
			nearest=msv(modeltest,W.dot(modeltest.wv.__getitem__(hypo)),topn=500)
			#print('nearest: ',nearest[:5])
			for cand,score in nearest:
				if cand in vocab_test and cand != hypo:
					cands.append(cand)
					if len(cands) == 15:
						break
			res.append(cands)
			#print(hypo,' -> ','\t'.join(cands))
		else:
			avg=[]
			for w in hypo.split():
				if modeltest.wv.__contains__(w):
					#print(w,' in model')
					avg.append(modeltest.wv.__getitem__(w))
			if not avg:
				print('HYPO NOT IN MODEL: ',hypo)
				res.append(' ')
				res_lr.append(' ')
				print('---')
				continue
			avg=np.mean(np.array(avg),axis=0)
			cands=[]
			nearest=msv(modeltest,W.dot(avg),topn=500)
			#print('nearest: ',nearest[:5])
			for cand,score in nearest:
				if cand in vocab_test and cand != hypo:
					cands.append(cand)
					if len(cands) == 15:
						break
			res.append(cands)
			#print(hypo,' -> ','\t'.join(cands))
		#input('---')
		#print('Processed line ',idx+1,' of ',len(testlines),' <- ',len(res),len(res_lr) )
		#print('---')

	output_name=embeddings_test.split('/')[-1]+'_'+str(args['npairs'])+'_'
	fname_W=output_name+test_file.split('/')[-1].replace('test.data.txt','output_W.txt')

	print('Output paths')
	path_taxoembed=os.path.join(args['output'],fname_W)
	print(path_taxoembed)

	with open(path_taxoembed,'w') as outf_taxoembed:
		for line in res:
			outf_taxoembed.write('\t'.join(line)+'\n')