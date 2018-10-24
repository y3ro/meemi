*******************************************************************************************************
*                      	       SemEval 2018 task 9: Hypernym Discovery        		              *
* 		Jose Camacho-Collados, Claudio Delli Bovi, Luis Espinosa-Anke, Sergio Oramas,         *
*		Tommaso Pasini, Enrico Santus, Vered Shwartz , Roberto Navigli, Horacio Saggion       *
*												      *
*******************************************************************************************************


This package contains the trial and training data for the SemEval 2018 task 9 on Hypernym Discovery. Given
a term (concept or entity) as input, the hypernym discovery task consists of retrieving a list with the
the most appropriate hypernyms from a text corpus.

In addition to this README file, there is a directory containing the trial data ("trial"), training data
("training"), test data (“test”), another one containing the full space of candidate hypernyms up to 
trigrams ("vocabulary") and a Python evaluation script ("task9-scorer.py"):

-------

	The vocabulary directory contains the files of all potential hypernyms for each subtask. This is an 
exhaustive list which contains all hypernyms in the gold data. All hypernyms are in their lowercased form, as
the final evaluation script is case-insensitive. In this list overgeneric hypernyms such as topic, entity, 
etc., which are not considered in the gold standard have been filtered, as well as those occurring less than 
5 and 3 times on the general-purpose and domain-specific datasets, respectively. Therefore, this list may be 
used by participants to reduce the search space of potential candidates.

-------

	The training and trial directories contain two (or three) folders for the two subtasks:

* data
	
	- contains the list of hyponyms for all five subtasks, each line corresponding to a term and its type
	  (Concept or Entity): 

		hyponym <tab> type


* gold

	- contains gold standard hypernyms for all the datasets, each line corresponding to the same line in 
	the corresponding data file.


* sample_output (only for trial)

	- contains sample system outputs for all the datasets including 15 extracted hypernyms per term. 
	  *This file is included with the only purpose for the participants to understand the proper output format.*
	
-------

	"task9-scorer.py": official evaluation script

The official evaluation script for this task can be run from the terminal as follows:

	$ python task9-scorer.py [gold_keys] [output_keys]

Example of usage:

	$ python task9-scorer.py trial/gold/1A.english.trial.gold.txt trial/sample_output/1A.english.sample.output.txt

Note 1: The evaluation script requires the "numpy" package: http://www.numpy.org/ 

Note 2: Gold and output files should have the same number of lines. If for some occurrence the system is not 
	confident enough to output any answer, just leave that line empty.

-------

For further information please check the CodaLab competition website: https://competitions.codalab.org/competitions/17119
You can also join our Google Group at https://groups.google.com/d/forum/semeval2018-hypernymdiscovery or contact any of 
the organizers for any enquiry.
