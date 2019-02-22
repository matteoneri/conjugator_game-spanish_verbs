from probar_verbos import *

verbo = input("verbo: ")
c = Conjugator(verbo)

if verbo not in os.listdir("verbos_irregulares"):
    for modo in code_map.keys():
        os.makedirs(os.path.join("verbos_irregulares",verbo,modo))
        print(modo)
        for tempo in code_map[modo].keys():
            print(tempo)
            conj = c.__getattribute__(modo)(tempo)
            print(conj)
            print()
            with open(os.path.join("verbos_irregulares",verbo,modo,tempo), 'w') as f:
                [f.write('{}\n'.format(v)) for v in conj]
