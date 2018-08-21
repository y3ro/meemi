## Meemi

The following repository includes the code and pre-trained cross-lingual embeddings from the paper *[Improving cross-lingual embeddings by meeting in the middle]()*  (EMNLP 2018).


### Pre-trained embeddings

We release the 300-dimension word embeddings used in our experiments as binary *bin* files. If you would like to convert the binary files to *txt*, you can use [convertvec](https://github.com/marekrei/convertvec):

- **Monolingual FastText embeddings**: Available [here]()
- **Baseline cross-lingual embeddings**: Available [here]()
- **Cross-lingual embeddings post-processed with Meemi**: Available [here]()

*Note:* All embeddings are uncased.

**Requirements:**

- Python 3
- NumPy
- Gensim
- If you use [VecMap](https://github.com/artetxem/vecmap) or [MUSE](https://github.com/facebookresearch/MUSE), please check their corresponding github pages.

### Usage

```bash
get_crossembs.sh EMBEDDING_FILE1 EMBEDDING_FILE2 DICTIONARY_FILE [-vecmap | -muse TRAIN_SIZE VALID_SIZE]
```

#### Apply meemi to your cross-lingual embeddings

```bash
get_crossembs.sh EMBEDDING_FILE1 EMBEDDING_FILE2 DICTIONARY_FILE
```

#### Use VecMap to align monolingual embeddings and then meemi

```bash
get_crossembs.sh EMBEDDING_FILE1 EMBEDDING_FILE2 DICTIONARY_FILE -vecmap
```

#### Use MUSE to align monolingual embeddings and then meemi

```bash
get_crossembs.sh EMBEDDING_FILE1 EMBEDDING_FILE2 DICTIONARY_FILE -muse TRAIN_SIZE VALID_SIZE
```

### Experiments



#### Bilingual Dictionary Induction

In order to test your embeddings on **bilingual dictionary induction** type the following:

```bash
python test.py EMBEDDING_FILE1 EMBEDDING_FILE2 < DICTIONARY_FILE
```

#### Word similarity

In order to test your embeddings on **monolingual word similarity** type the following:

```bash
python test_similarity_monolingual.py EMBEDDINGS DATASET
```
You can also test various datasets at the same time

```bash
python test_similarity_monolingual.py EMBEDDINGS DATASET1 DATASET2 ... DATASETN
```
Likewise, to test your cross-lingual embeddings on **cross-lingual word similarity** type the following:

```bash
python test_similarity_crosslingual.py SOURCE_EMBEDDINGS TARGET_EMBEDDINGS DATASET
```
As with monolingual similarity, you can similarly also test various datasets at the same time. Below an example on how to test your English-Spanish cross-lingual embeddings on all the monolingual and cross-lingual word similarity datasets:

```bash
python test_similarity_monolingual.py XXXXXXXXX XXXXXXXXX data/SimLex/simlex-999_english.txt data/SemEval2018-subtask1-monolingual/english.txt data/rg65-monolingual/rg65_english.txt data/WS353-monolingual/WS353-english-sim.txt
python test_similarity_monolingual.py XXXXXXXXX XXXXXXXXX data/SemEval2018-subtask1-monolingual/spanish.txt data/rg65-monolingual/rg65_spanish.txt 
python test_similarity_crosslingual.py XXXXXXXXX XXXXXXXXX data/SemEval2018-subtask2-crosslingual/en-es.txt data/rg65-crosslingual/rg65_EN-ES.txt
```
*Note:* This code assumes you are given uncased (lowercased) embeddings as input. If you would like to mantain the casing, simply remove the *.lower()* commands in the evaluation scripts.

#### Hypernym Discovery

Coming soon!

### Reference paper

If you use any of these resources, please cite the following [paper]():
```bash
@InProceedings{camacho:preprocessing2018,
  author = 	"Doval, Yerai and Camacho-Collados, Jose and Espinosa-Anke, Luis and Schockaert, Steven",
  title = 	"Improving cross-lingual embeddings by meeting in the middle",
  booktitle = 	"Proceedings of EMNLP",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  location = 	"Brussels, Belgium"
}

```

If you use VecMap or MUSE, please also cite their corresponding papers.
