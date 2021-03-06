#    Vertical interval analysis tool for Duos corpora
#    Copyright 2019 Nestor Napoles Lopez
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from vis.models.indexed_piece import Importer
from collections import Counter
from collections import OrderedDict
import copy
import numpy as np
import operator
import json
import sys

vert_setts = {
    'quality': False,
    'simple or compound': 'compound',
    'directed': True,
}

def heldAsRepeated(df):
    return df.fillna(method='ffill')

def ignoreRests(df):
    tmpdf = df[df != "Rest"]
    return tmpdf.dropna(how="any")

def halfNoteSlices(df):
    a = np.arange(df.index[0], df.index[-1] + 2.0, 2.0)
    tmpdf = df.reindex(df.index.union(a))
    tmpdf = tmpdf.fillna(method='ffill')
    return tmpdf.reindex(a)

def removeDuplicates(df):
    tmpdf = df[df != df.shift(1)].dropna(how='all')
    return tmpdf.fillna(method='ffill')

# Half note slices, ignoring rests in one voice + no repeats
def analysisHalfNotesNoRepeats(s):
    hn = copy.deepcopy(s)
    hnnr = hn.get_data('noterest')
    hnnr = halfNoteSlices(hnnr)
    hnnr = ignoreRests(hnnr)
    hnnr = removeDuplicates(hnnr)
    hn._analyses['noterest'] = hnnr
    hnv = hn.get_data('vertical_interval', settings=vert_setts)
    return hn, hnv

# Half note slices, cutting ngrams when finding a rest in one voice
def analysisHalfNotesCutAtRestNoRepeats(s):
    hn = copy.deepcopy(s)
    hnnr = hn.get_data('noterest')
    hnnr = halfNoteSlices(hnnr)
    hnnr = removeDuplicates(hnnr)
    hn._analyses['noterest'] = hnnr
    hnv = hn.get_data('vertical_interval', settings=vert_setts)
    return hn, hnv

# Half note slices, ignoring rests in one voice
def analysisHalfNotes(s):
    hn = copy.deepcopy(s)
    hnnr = hn.get_data('noterest')
    hnnr = halfNoteSlices(hnnr)
    hnnr = ignoreRests(hnnr)
    hn._analyses['noterest'] = hnnr
    hnv = hn.get_data('vertical_interval', settings=vert_setts)
    return hn, hnv

# Attacks only, ignoring rests in one voice
def analysisAttackNotes(s):
    an = copy.deepcopy(s)
    annr = an.get_data('noterest')
    annr = heldAsRepeated(annr)
    annr = ignoreRests(annr)
    an._analyses['noterest'] = annr
    anv = an.get_data('vertical_interval', settings=vert_setts)
    return an, anv

# Half note slices, marking rests in one voice as ngrams
def analysisHalfRests(s):
    hr = copy.deepcopy(s)
    hrnr = hr.get_data('noterest')
    hrnr = halfNoteSlices(hrnr)
    hr._analyses['noterest'] = hrnr
    hrv = hr.get_data('vertical_interval', settings=vert_setts)
    return hr, hrv

# Attacks only, marking rests in one voice as ngrams
def analysisAttackRests(s):
    ar = copy.deepcopy(s)
    arnr = ar.get_data('noterest')
    arnr = heldAsRepeated(arnr)
    ar._analyses['noterest'] = arnr
    arv = ar.get_data('vertical_interval', settings=vert_setts)
    return ar, arv

def runAnalysis(scorelist, output_tsv):
    intervals = OrderedDict()
    total_intervals = OrderedDict()
    with open(scorelist) as f:
        pathnames = f.readlines()
        pathnames = [f.strip() for f in pathnames]
        for filename in pathnames:
            if not filename.endswith('.xml'):
                continue
            print(filename)
            s = Importer(filename)
            _, verts = analysisHalfNotesCutAtRestNoRepeats(s)
            verts_list = list(list(verts.to_dict().values())[0].values())
            composer = filename.split('/')[2]
            composer_intervals = intervals.get(composer, Counter())
            composer_total_intervals = total_intervals.get(composer, 0)
            composer_intervals.update(verts_list)
            composer_total_intervals += len(verts_list)
            intervals[composer] = composer_intervals
            total_intervals[composer] = composer_total_intervals
        with open(output_tsv, 'w') as o:
            header = "interval"
            for composer in intervals:
                header += '\t{0}\t{0} (percent)'.format(composer)
            header += '\n'
            o.write(header)
            all_intervals = []
            [all_intervals.extend(v.keys()) for c, v in intervals.items()]
            all_intervals = [int(n) for n in all_intervals if n != 'Rest']
            min_interval = min(all_intervals)
            max_interval = max(all_intervals)
            for n in range(min_interval, max_interval + 1):
                strn = str(n)
                row = '{}'.format(n)
                for composer in intervals:
                    count = intervals[composer][strn]
                    percent = count / total_intervals[composer]
                    row += '\t{}\t{}'.format(count, percent)
                row += '\n'
                o.write(row)
            # rests = '{}\t{}\t{}\t{}\t{}'.format('Rest', larue_intervals['Rest'], josquin_intervals['Rest'], larue_intervals['Rest'] / larue_total_intervals, josquin_intervals['Rest'] / josquin_total_intervals)
            # o.write(rests)
                
if __name__ == '__main__':
    scorelist = sys.argv[1]
    output_tsv = sys.argv[2]
    runAnalysis(scorelist, output_tsv)