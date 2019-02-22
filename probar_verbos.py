import os
import numpy as np
import json
from collections import defaultdict
from queue import deque
from functools import reduce
import bisect

code_map = {'indicativo':{'conditional perfecto':'icp',
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

class conjugator:
    def __init__(self, verbo):
        self.infinitivo = verbo
        self.classe = verbo[-2:]
        self.gerundio = verbo[:-1]+ (self.classe=="ir" and "iendo" or "ndo") 
        self.participio = verbo[:-1]+"do" if self.classe!="er" else verbo[:-2]+"ido"

    def indicativo(self, tempo):
        if tempo=='presente':
            desinencias = {'ar':['o','as','a','amos','áis','an'],
                           'er':['o','es','e','emos','éis','en'],
                           'ir':['o','es','e','imos','ís','en']}
            return [self.infinitivo[:-2]+d for d in desinencias[self.classe]]
        elif tempo=='preterito imperfecto':
            desinencias = {'ar':['aba','abas','aba','ábamos','abais','aban'],
                           'er':['ía','ías','ía','íamos','íais','ían'],
                           'ir':['ía','ías','ía','íamos','íais','ían']}
            return [self.infinitivo[:-2]+d for d in desinencias[self.classe]]
        elif tempo=='preterito perfecto simple':
            desinencias = {'ar':['é','amaste','ó','amos','asteis','aron'],
                           'er':['í','iste','ió','imos','isteis','ieron'],
                           'ir':['í','iste','ió','imos','isteis','ieron']}
            return [self.infinitivo[:-2]+d for d in desinencias[self.classe]]
        elif tempo=='conditional simple':
            desinencias = ['ía','ías','ía','íamos','íais','ían']
            return [self.infinitivo+d for d in desinencias[self.classe]]
        elif tempo=='preterito perfecto compuesto':
            haber = ['he','has','ha','hemos','habéis','han']
            return ["{} {}".format(h,self.participio) for h in haber]
        elif tempo=='preterito pluscuamperfecto':
            haber = ['había','habías','había','habíamos','habíais','habían']
            return ["{} {}".format(h,self.participio) for h in haber]
        elif tempo=='conditional perfecto':
            haber = ['habría','habrías','habría','habríamos','habríais','habrían']
            return ["{} {}".format(h,self.participio) for h in haber]
        elif tempo=='futuro simple':
            desinencias = ['é','ás','á','emos','éis','án']
            return [self.infinitivo+d for d in desinencias[self.classe]]

    def subjuntivo(self, tempo):
        if tempo=='presente':
            desinencias = {'ar':['e','es','e','emos','éis','en'],
                           'er':['a','as','a','amos','áis','an'],
                           'ir':['a','as','a','amos','áis','an']}
            return [self.infinitivo[-2]+d for d in desinencias[self.classe]]
        elif tempo=='preterito imperfecto':
            desinencias = {'ar':['ara','aras','ara','áramos','arais','aran'],
                           'er':['iera','ieras','iera','iéramos','ierais','ieran'],
                           'ir':['iera','ieras','iera','iéramos','ierais','ieran']}
            return [self.infinitivo[-2]+d for d in desinencias[self.classe]]
        elif tempo=='preterito imperfecto -ese':
            desinencias = {'ar':['ase','ases','ase','ásemos','aseis','asen'],
                           'er':['iese','ieses','iese','iésemos','ieseis','iesen'],
                           'ir':['iese','ieses','iese','iésemos','ieseis','iesen']}
            return [self.infinitivo[-2]+d for d in desinencias[self.classe]]
        elif tempo=='preterito perfecto':
            haber = ['haya','hayas','haya','hayamos','hayáis','haian']
            return ["{} {}".format(h,self.participio) for h in haber]
        elif tempo=='preterito pluscuamperfecto':
            haber = ['hubiera','hubieras','hubiera','hubiéramos','hubierais''hubieran']
            return ["{} {}".format(h,self.participio) for h in haber]
        elif tempo=='preterito pluscuamperfecto -ese':
            haber = ['hubiese','hubieses','hubiese','hubiésemos','hubieseis''hubiesen']
            return ["{} {}".format(h,self.participio) for h in haber]

    def imperativo(self, tempo):
        if tempo='afirmativo':
            desinencias = {'ar':['a','e','emos','ad','en'],
                           'er':['e','as','amos','ed','an'],
                           'ir':['e','as','amos','id','an']}
            return [""]+[self.infinitivo[-2]+d for d in desinencias[self.classe]]


temp = [[(code,modo,tempo) for tempo,code in tempos.items()] for modo,tempos in code_map.items()]
temp = reduce(lambda x,y: x.extend(y) or x, temp, [])
code_map_inverse = {code:(modo,tempo) for code,modo,tempo in temp}
verbs = os.listdir('verbos')
stats = 'stats'

if __name__=='__main__':
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



