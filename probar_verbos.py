import os
import numpy as np
import json
from collections import defaultdict
from queue import deque
from functools import reduce
import bisect

code_map = {'indicativo':{'conditional compuesto':'icc',
                          'conditional simple':'ics',
                          'futuro simple':'ifs',
                          'presente':'ip',
                          'preterito imperfecto':'ipi',
                          'preterito perfecto compuesto':'ippc',
                          'preterito perfecto simple':'ipps',
                          'preterito pluscuamperfecto':'ip+'},
            'subjuntivo':{'presente':'sp',
                           'preterito imperfecto':'spi',
                           'preterito imperfecto -ese':'spi2',
                           'preterito perfecto':'spp',
                           'preterito pluscuamperfecto':'sp+',
                           'preterito pluscuamperfecto -ese':'sp+2'},
            'imperativo':{'afirmativo':'ia'}}
temp = [[(code,modo,tempo) for tempo,code in tempos.items()] for modo,tempos in code_map.items()]
temp = reduce(lambda x,y: x.extend(y) or x, temp, [])
code_map_inverse = {code:(modo,tempo) for code,modo,tempo in temp}
verbs = os.listdir('verbos')
stats = 'stats'


# read the stats
s = defaultdict(list) 
if os.path.isfile(stats):
    with open(stats) as s_file:
        s.update(json.load(s_file))
    avg_perc = np.mean([sum(v)/len(v) for v in s.values()])
    if avg_perc>0.5:
        prob_random_choice = 0.8
    else:
        prob_random_choice = 0.1
else:
    prob_random_choice = 1

if np.random.rand()<prob_random_choice:
    # random choice
    verb = np.random.choice(verbs)
    #mood = np.random.choice(['imperativo'])#['indicativo','subjuntivo','imperativo'] 
    mood = np.random.choice(['indicativo','subjuntivo','imperativo'])
    tempo = np.random.choice(os.listdir(os.path.join('verbos',verb,mood)))
    verb_code = '{}_{}'.format(verb,code_map[mood][tempo])
else:
    # choice with a prob proportional to the number of errors
    probs = np.array([(len(v)-sum(v)+0.2/len(v)) for v in s.values()])
    #print(s)
    #print(probs)
    probs= np.cumsum(probs/probs.sum())
    rnd = np.random.rand()
    idx = bisect.bisect_left(probs, rnd)
    verb_code = [k for k in s.keys()][idx]
    verb, code = verb_code.split('_')
    mood, tempo = code_map_inverse[code]




with open(os.path.join('verbos',verb,mood,tempo)) as f:
    # ask for a verb conj
    print(verb)
    print(mood, tempo)
    print()
    err = False
    for p,v in zip(['yo','tu','el/ella','nosotros','vosotros','ell@s'],f):
        if mood=='imperativo':
            if p=='yo': continue
        i = input('{} '.format(p))
        if i!=v.strip():
            print('No! {} {}'.format(p, v))
            err=True

    # change stat
    temp = deque(s[verb_code],5)
    temp.append(1-err)
    s[verb_code] = list(temp)
    #print(sum(temp)/len(temp))
    with open(stats, 'w') as s_file:
        json.dump(s, s_file)



