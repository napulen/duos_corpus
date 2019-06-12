# Copyright 2019 Nestor Napoles Lopez

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import csv
import sys
from collections import Counter
from collections import OrderedDict
import pprint


def print_counts(occurrence, occurrence_by_composer):
    composers = list(sorted(occurrence_by_composer.keys()))
    composers_d = [occurrence_by_composer[c] for c in composers]
    # Header
    print('Occurrences,{},Total'.format(','.join(composers)))
    # Rows
    for ocs, all_ngrams in occurrence.items():
        print(ocs, end='')
        for idx, comp in enumerate(composers_d):
            if ocs in comp:
                print(',{}'.format(len(comp[ocs])), end='')
            else:
                print(',0', end='')
        print(',{}'.format(len(all_ngrams)))


if __name__ == '__main__':
    tsv_input = sys.argv[1]
    ngrams_by_occurrence = OrderedDict()
    ngrams_by_composer = {}
    with open(tsv_input, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader, None)
        total_ngrams = 0
        distinct_ngrams = 0
        current_ngram_composer = []
        for row in csv_reader:
            # Starting a new distinct n-gram
            if row[0] and row[1]:
                if current_ngram_composer:
                    composer = '_'.join(sorted(current_ngram_composer))
                    d = ngrams_by_composer.get(composer, OrderedDict())
                    l = d.get(occurrences, [])
                    d[occurrences] = l + [ngram]
                    ngrams_by_composer[composer] = d
                occurrences, ngram = row[0], row[1]
                current_ngram_composer = []
                total_ngrams += int(occurrences)
                distinct_ngrams += 1
                l = ngrams_by_occurrence.get(occurrences, [])
                ngrams_by_occurrence[occurrences] = l + [ngram]
            # Reading a specific occurrence of an n-gram
            else:
                composer = row[2]
                if not composer in current_ngram_composer:
                    current_ngram_composer.append(composer)

    print('Total n-grams: {}'.format(total_ngrams))
    print('Distinct n-grams: {}'.format(distinct_ngrams))
    print('Number of distinct n-grams by occurrence')
    print_counts(ngrams_by_occurrence, ngrams_by_composer)