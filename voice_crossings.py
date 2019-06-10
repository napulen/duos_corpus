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

import music21
import sys

if __name__ == '__main__':
    scorelist = sys.argv[1]
    with open(scorelist) as f:
        pathnames = f.readlines()
        pathnames = [f.strip() for f in pathnames]
        for filename in pathnames:
            if not filename.endswith('.xml'):
                continue
            print(filename)
            s = music21.converter.parse(filename)
            highest = music21.note.Note('C1')
            lowest = music21.note.Note('C8')
            for p in s.parts:
                print(p)
                for n in p.flat.notes:
                    lowest = n if n < lowest else lowest
                    highest = n if n > highest else highest
            print(highest)
            print(lowest)