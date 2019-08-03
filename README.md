# duos_corpus
This repository contains all the necessary code to replicate the results from *Contrapuntal Style: Josquin des Prez vs. Pierre de la Rue*. It has been written by Nestor Napoles Lopez.

## Requirements
We assume that the [vis-framework](https://github.com/ELVIS-Project/vis-framework) package is available in python, as well as `music21`, `pandas`, and `seaborn` (for plotting).

We also assume that the repository has been cloned including its submodules:
```
git clone https://github.com/napulen/duos_corpus_code.git --recursive
```

## Running
The analysis is divided in several steps:

### `analyze.py`

This script is in charge of computing all the n-grams of the collections. It should be always run first as other scripts usually depend on the output obtained here.
```
python analyze.py <input_collection> <path_to_ngrams_json> <path_to_ngram_types>
```

The script receives as its first argument, a plain-text file containing all the scores to be computed. A typical input file looks like this:
```
./mass-duos-corpus-josquin-larue/Josquin (secure)/XML/Josquin Credo De tous biens playne - Et in spiritum.xml
./mass-duos-corpus-josquin-larue/Josquin (secure)/XML/Josquin Missa Ave maris stella - Agnus II.xml
./mass-duos-corpus-josquin-larue/Josquin (secure)/XML/Josquin Missa Ave maris stella - Benedictus.xml
./mass-duos-corpus-josquin-larue/Josquin (secure)/XML/Josquin Missa Ave maris stella - Qui venit.xml
...
```

The script then outputs two files: A `json` file containing all the n-gram analysis of each score in the input file and a `tsv` file containing all the n-gram types and their occurrences through the corpus.
