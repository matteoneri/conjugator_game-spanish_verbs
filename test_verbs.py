import os
import numpy as np

verbs = os.listdir('verbos')
verb = np.random.choice(verbs)
mood = np.random.choice(['indicativo','subjuntivo'])
tempo = np.random.choice(os.listdir(os.path.join('verbos',verb,mood)))

with open(os.path.join('verbos',verb,mood,tempo)) as f:
    print(verb)
    print(mood, tempo)
    print()
    for p,v in zip(['yo','tu','el/ella','nosotros','vosotros','ell@s'],f):
        i = input('{} '.format(p))
        i==v.strip() or print('No! {} {}'.format(p, v))
