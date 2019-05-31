## Meemi

The following repository includes the code and pre-trained cross-lingual word embeddings from the paper *[Improving cross-lingual word embeddings by meeting in the middle](http://aclweb.org/anthology/D18-1027)*  (EMNLP 2018).


### Pre-trained embeddings

We release the 300-dimension word embeddings used in our experiments (English, Spanish, Italian, German and Finnish) as binary *bin* files:

- **Monolingual FastText embeddings**: Available [here](https://drive.google.com/drive/folders/1a4H1qmMWhG5CZQnkNt79wAaJFA6tqZLn?usp=sharing)
- **Baseline cross-lingual embeddings**: Available [here](https://drive.google.com/drive/folders/1Qq5_fC9kqWUA_YwP3SLPpjCB_KMNvxlB?usp=sharing)
- **Cross-lingual embeddings post-processed with Meemi**: Available [here](https://drive.google.com/drive/folders/11rsZf10IJ6Z2WeKJgI7cHy__QBffm5lP?usp=sharing)

*Note 1:* All vocabulary words are lowercased.

*Note 2:* If you would like to convert the binary files to *txt*, you can use [convertvec](https://github.com/marekrei/convertvec).


**Requirements:**

- Python 3
- NumPy
- Gensim
- If you use [VecMap](https://github.com/artetxem/vecmap) or [MUSE](https://github.com/facebookresearch/MUSE), please also check their corresponding GitHub pages. Note that we use a previous version of these tools, of which there is a copy in this repository (WIP).

### Usage

```bash
get_crossembs.sh SOURCE_EMBEDDINGS TARGET_EMBEDDINGS DICTIONARY_FILE [-vecmap | -muse TRAIN_DICT VALID_DICT]
```

#### Apply meemi to your cross-lingual embeddings

```bash
get_crossembs.sh SOURCE_EMBEDDINGS TARGET_EMBEDDINGS DICTIONARY_FILE
```

Example:

```bash
get_crossembs.sh EN-ES.english.vecmap.txt EN-ES.spanish.vecmap.txt en-es.dict.txt
```

#### Use VecMap to align monolingual embeddings and then meemi

```bash
get_crossembs.sh SOURCE_EMBEDDINGS TARGET_EMBEDDINGS DICTIONARY_FILE -vecmap
```

#### Use MUSE to align monolingual embeddings and then meemi

```bash
get_crossembs.sh SOURCE_EMBEDDINGS TARGET_EMBEDDINGS DICTIONARY_FILE -muse TRAIN_SIZE VALID_SIZE
```

### Experiments


#### Bilingual Dictionary Induction

In order to test your embeddings on **bilingual dictionary induction** type the following:

```bash
python test.py SOURCE_EMBEDDINGS TARGET_EMBEDDINGS < DICTIONARY_FILE
```

#### Word similarity

In order to test your embeddings on **monolingual word similarity** type the following:

```bash
python test_similarity_monolingual.py EMBEDDINGS DATASET
```
You can also test various datasets at the same time:

```bash
python test_similarity_monolingual.py EMBEDDINGS DATASET1 [DATASET2] ... [DATASETN]
```
Likewise, to test your cross-lingual embeddings on **cross-lingual word similarity** type the following:

```bash
python test_similarity_crosslingual.py SOURCE_EMBEDDINGS TARGET_EMBEDDINGS DATASET
```
As with monolingual similarity, you can also test various datasets at the same time. Below is an example of how to test your English-Spanish cross-lingual embeddings on all the monolingual and cross-lingual word similarity datasets:

```bash
python test_similarity_monolingual.py EN-ES.english.vecmap.meemi.bin data/SimLex/simlex-999_english.txt data/SemEval2018-subtask1-monolingual/english.txt data/rg65-monolingual/rg65_english.txt data/WS353-monolingual/WS353-english-sim.txt
python test_similarity_monolingual.py EN-ES.english.vecmap.meemi.bin data/SemEval2018-subtask1-monolingual/spanish.txt data/rg65-monolingual/rg65_spanish.txt 
python test_similarity_crosslingual.py EN-ES.english.vecmap.meemi.bin EN-ES.spanish.vecmap.meemi.bin data/SemEval2018-subtask2-crosslingual/en-es.txt data/rg65-crosslingual/rg65_EN-ES.txt
```
*Note:* This code assumes that lowercased word embeddings are provided as input. If you would like to mantain the casing, simply remove the *.lower()* commands in the evaluation scripts.

#### Cross-lingual Hypernym Discovery

[Hypernym Discovery](https://competitions.codalab.org/competitions/17119) is the task to retrieve, for a given term, a ranked list of valid hypernyms. In this experiment, a hypernym discovery system is trained in English data (and possibly in a weakly supervised setting with some target language data), and makes predictions in the target language.

To run the hypernym discovery experiments, launch the following command:

```bash
python3 experiments/hypernym_discovery/taxoembed.py -wvtrain SOURCE_EMBEDDINGS -wvtest TARGET_EMBEDDINGS -vtest TARGET_VOCABULARY -hypotrain SOURCE_HYPONYMS -hypertrain SOURCE_HYPERNYMS -test TARGET_HYPONYMS -newtrain TARGET_LANG_TRAINING_INSTANCES -npairs NUMB_TRAINING_INSTANCES -o OUTPUT_FOLDER 
```

The predictions of the model are saved in `OUTPUT_FOLDER` with the name `[TARGET_EMBEDDINGS]_[NUMB_TRAINING_INSTANCES]_[TARGET_LANG_TRAINING_INSTANCES]_W.txt`.

For example, evaluating a hypernym discovery model for Spanish trained on VecMap English vectors and 500 additional instances in Spanish:

```bash
 python3 experiments/hypernym_discovery/taxoembed.py -wvtrain EN-ES.english.vecmap.bin -wvtest EN-ES.spanish.vecmap.bin -vtest experiments/hypernym_discovery/SemEval2018-Task9/vocabulary/1C.spanish.vocabulary.txt -hypotrain experiments/hypernym_discovery/SemEval2018-Task9/training/data/1A.english.training.data.txt -hypertrain experiments/hypernym_discovery/SemEval2018-Task9/training/gold/1A.english.training.gold.txt -test experiments/hypernym_discovery/SemEval2018-Task9/test/data/1C.spanish.test.data.txt -o experiments/hypernym_discovery/ -newtrain experiments/hypernym_discovery/SemEval2018-Task9/utils/spanish_train.tsv -npairs 500
```

Then, call the official SemEval task scorer passing as arguments the gold file and the predictions file generated in the previous step.

```bash
python experiments/hypernym_discovery/SemEval2018-Task9/task9-scorer.py GOLD_FILE PREDICTIONS_FILE
```

For the previous example, the exact command would be:

```bash
python experiments/hypernym_discovery/SemEval2018-Task9/task9-scorer.py experiments/hypernym_discovery/SemEval2018-Task9/test/gold/1C.spanish.test.gold.txt experiments/hypernym_discovery/EN-ES.spanish.vecmap.bin_500_1C.spanish.output_W.txt 
```

### Reference paper

If you use any of these resources, please cite the following [paper](https://arxiv.org/abs/1808.08780):
```bash
@InProceedings{doval:meemiemnlp2018,
  author = 	"Doval, Yerai and Camacho-Collados, Jose and Espinosa-Anke, Luis and Schockaert, Steven",
  title = 	"Improving cross-lingual word embeddings by meeting in the middle",
  booktitle = 	"Proceedings of EMNLP",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  location = 	"Brussels, Belgium"
}

```

If you use VecMap or MUSE, please also cite their corresponding papers.
