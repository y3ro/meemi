## Meemi
#### Yerai Doval...

The following repository includes the code and pre-trained cross-lingual embeddings from the paper *[]()*  ().

### Apply meemi to your cross-lingual embeddings


```bash
python get...
```


### Experiments



#### Bilingual Dictionary Induction





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

#### Hypernym Discovery
