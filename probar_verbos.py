import os
import numpy as np
import json
from collections import defaultdict
from queue import deque
from functools import reduce
import bisect


class Conjugator: 
    _irregular_verbs_folder = 'verbos_irregulares'
    _irregular_verbs        = os.listdir(_irregular_verbs_folder)

    def __init__(self, verbo):
        self.infinitivo = verbo
        self.classe = verbo[-2:]
        self._regular = verbo not in self._irregular_verbs
        if not self._regular:
            with open(os.path.join(self._irregular_verbs_folder, verbo, 'participio')) as f:
                self.participio = f.readline().strip()
            #with open(os.path.join(self._irregular_verbs_folder, verbo, 'gerundio')) as f:
            #    self.gerundio = f.read_line().strip()
        else:
            self.gerundio = verbo[:-1]+ (self.classe=="ir" and "iendo" or "ndo") 
            self.participio = verbo[:-1]+"do" if self.classe!="er" else verbo[:-2]+"ido"

    def indicativo(self, tempo):
        if self._regular:
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
                return [self.infinitivo+d for d in desinencias]
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
                return [self.infinitivo+d for d in desinencias]
        else:
            with open(os.path.join(self._irregular_verbs_folder,self.infinitivo,'indicativo',tempo)) as f:
                return [l.strip() for l in f.readlines()]

    def subjuntivo(self, tempo): 
        if self._regular:
            if tempo=='presente':
                desinencias = {'ar':['e','es','e','emos','éis','en'],
                               'er':['a','as','a','amos','áis','an'],
                               'ir':['a','as','a','amos','áis','an']}
                return [self.infinitivo[:-2]+d for d in desinencias[self.classe]]
            elif tempo=='preterito imperfecto':
                desinencias = {'ar':['ara','aras','ara','áramos','arais','aran'],
                               'er':['iera','ieras','iera','iéramos','ierais','ieran'],
                               'ir':['iera','ieras','iera','iéramos','ierais','ieran']}
                return [self.infinitivo[:-2]+d for d in desinencias[self.classe]]
            elif tempo=='preterito imperfecto -ese':
                desinencias = {'ar':['ase','ases','ase','ásemos','aseis','asen'],
                               'er':['iese','ieses','iese','iésemos','ieseis','iesen'],
                               'ir':['iese','ieses','iese','iésemos','ieseis','iesen']}
                return [self.infinitivo[:-2]+d for d in desinencias[self.classe]]
            elif tempo=='preterito perfecto':
                haber = ['haya','hayas','haya','hayamos','hayáis','hayan']
                return ["{} {}".format(h,self.participio) for h in haber]
            elif tempo=='preterito pluscuamperfecto':
                haber = ['hubiera','hubieras','hubiera','hubiéramos','hubierais''hubieran']
                return ["{} {}".format(h,self.participio) for h in haber]
            elif tempo=='preterito pluscuamperfecto -ese':
                haber = ['hubiese','hubieses','hubiese','hubiésemos','hubieseis','hubiesen']
                return ["{} {}".format(h,self.participio) for h in haber]
        else:
            with open(os.path.join(self._irregular_verbs_folder,self.infinitivo,'subjuntivo',tempo)) as f:
                return [l.strip() for l in f.readlines()]

    def imperativo(self, tempo):
        if self._regular:
            if tempo=='afirmativo':
                desinencias = {'ar':['a','e','emos','ad','en'],
                               'er':['e','a','amos','ed','an'],
                               'ir':['e','a','amos','id','an']}
                return [""]+[self.infinitivo[:-2]+d for d in desinencias[self.classe]]
        else:
            with open(os.path.join(self._irregular_verbs_folder,self.infinitivo,'imperativo',tempo)) as f:
                return [l.strip() for l in f.readlines()]


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
_temp = [[(code,modo,tempo) for tempo,code in tempos.items()] for modo,tempos in code_map.items()]
_temp = reduce(lambda x,y: x.extend(y) or x, _temp, [])
code_map_inverse = {code:(modo,tempo) for code,modo,tempo in _temp}
del _temp


verbs = os.listdir('verbos_irregulares')+['reg.ar','reg.er','reg.ir']*2
stats = 'stats'


if __name__=='__main__':
    # read the stats
    s = defaultdict(list) 
    if os.path.isfile(stats):
        with open(stats) as s_file:
            s.update(json.load(s_file))
        avg_perc = np.mean([sum([i>0 for i in v])/len(v) for v in s.values()])
        if avg_perc>0.5:
            prob_random_choice = 0.8
        else:
            prob_random_choice = 0.1
    else:
        prob_random_choice = 1

    # tie a verb, mood, tempo
    if np.random.rand()<prob_random_choice:
        # random choice
        verb = np.random.choice(verbs)
        #mood = np.random.choice(['imperativo'])#['indicativo','subjuntivo','imperativo'] 
        mood = np.random.choice(['indicativo','subjuntivo','imperativo'],p=np.array([6,4,1])/sum([6,4,1]))
        tempo = np.random.choice(os.listdir(os.path.join('verbos_irregulares','ir',mood)))
        code = code_map[mood][tempo]
        verb_code = '{}_{}'.format(verb,code)
    else:
        # choice with a prob proportional to the number of errors
        probs = np.array([(len(v)-sum([i>0 for i in v])+0.2/len(v)) for v in s.values()])
        #print(s)
        #print(probs)
        probs= np.cumsum(probs/probs.sum())
        rnd = np.random.rand()
        idx = bisect.bisect_left(probs, rnd)
        verb_code = [k for k in s.keys()][idx]
        verb, code = verb_code.split('_')
        mood, tempo = code_map_inverse[code]


    if np.random.rand()<0.4:
        # ask for a verb conj
        if verb in ['reg.ar','reg.er','reg.ir']:
            with open('verbos_regulares/{}'.format(verb)) as reg_f:
                verbs_meanings = [l for l in reg_f]
                verb_meaning = np.random.choice(verbs_meanings)
                verb, meaning = verb_meaning.strip().split(':')
                print('{} - {}'.format(verb, meaning))
        else:
            print(verb)

        c = Conjugator(verb)
        conj = c.__getattribute__(mood)(tempo)

        print(mood, tempo)
        print()
        err = False

        for p,v in zip(['yo','tu','el/ella','nosotros','vosotros','ell@s'],conj):
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

    else:
        # ask for a verb conj
        tempos = [k for k in code_map[mood].keys()]
        person = np.random.choice(range(6))
        if mood=='imperativo':
            if person==0:
                person = 1
        if verb in ['reg.ar','reg.er','reg.ir']:
            with open('verbos_regulares/{}'.format(verb)) as reg_f:
                verbs_meanings = [l for l in reg_f]
                verb_meaning = np.random.choice(verbs_meanings)
                verbo, meaning = verb_meaning.strip().split(':')
                print('{} - {}'.format(verbo, meaning))
        else:
            verbo = verb
            print(verbo)
        print(mood)
        print()

        for tempo in tempos:
            code = code_map[mood][tempo]
            verb_code = '{}_{}'.format(verb,code)

            c = Conjugator(verbo)
            conj = c.__getattribute__(mood)(tempo)

            err = False
            p,v = list(zip(['yo','tu','el/ella','nosotros','vosotros','ell@s'],conj))[person]
            i = input('({:31}) {} '.format(tempo, p))
            if i!=v.strip():
                print('No! {} {}'.format(p, v))
                err=True

            # change stat
            temp_var = deque(s[verb_code],5)
            temp_var.append((1-err)*0.2)
            s[verb_code] = list(temp_var)
            #print(sum(temp)/len(temp))
            with open(stats, 'w') as s_file:
                json.dump(s, s_file)
