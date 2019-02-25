import json
import pandas as pd
from functools import reduce

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
temp = [[(code,modo,tempo) for tempo,code in tempos.items()] for modo,tempos in code_map.items()]
temp = reduce(lambda x,y: x.extend(y) or x, temp, [])
code_map_inverse = {code:(modo,tempo) for code,modo,tempo in temp}

with open('/home/matteo/Spanish/conjugator/stats') as f:
    stats = json.load(f)
    
data = []
for k,v in stats.items():
    verb, code  = k.split("_")
    modo, tempo = code_map_inverse[code]
    data.append((verb, modo, tempo, sum(v)/len(v)*100, v))

df = pd.DataFrame(data, columns=['verb','modo','tempo','precision','streak'])
print(df.sort_values(['precision','verb','modo','tempo']))
