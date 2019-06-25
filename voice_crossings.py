# Copyright 2019 Nestor Napoles Lopez
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

import music21
import sys

if __name__ == '__main__':
    scorelist = sys.argv[1]
    with open(scorelist) as f:
        pathnames = f.readlines()
        pathnames = [f.strip() for f in pathnames]
        print('file\tpart1_lowest_note\tpart1_highest_note\tpart1_range\tpart2_lowest_note\tpart2_highest_note\tpart2_range\tpartcrossing')
        for filename in pathnames:
            if not filename.endswith('.xml'):
                continue
            s = music21.converter.parse(filename)
            outer_notes = []
            for p in s.parts:
                highest = music21.note.Note('C1')
                lowest = music21.note.Note('C8')
                for n in p.flat.notes:
                    if type(n) is music21.chord.Chord:
                        n = min(n)
                    highest = n if n > highest else highest
                    lowest = n if n < lowest else lowest
                outer_notes.append((lowest, highest))
            lower_part, upper_part = outer_notes[1], outer_notes[0]
            range_lower_part = music21.interval.Interval(lower_part[0], lower_part[1])
            range_upper_part = music21.interval.Interval(upper_part[0], upper_part[1])
            if lower_part[1] >= upper_part[0] and upper_part[1] >= lower_part[0]:
                # Crossing
                lower_crossing_note =  max(lower_part[0], upper_part[0])
                higher_crossing_note = min(lower_part[1], upper_part[1])
                voicecrossing = music21.interval.Interval(lower_crossing_note, higher_crossing_note).generic.directed
            else:
                voicecrossing = 'No crossing'
            row = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                filename,
                lower_part[0].nameWithOctave,
                lower_part[1].nameWithOctave,
                range_lower_part.generic.directed,
                upper_part[0].nameWithOctave,
                upper_part[1].nameWithOctave,
                range_upper_part.generic.directed,
                voicecrossing
            )
            print(row)