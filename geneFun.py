# -*- coding: utf-8 -*-


from multiprocessing import Process, Manager

import dnaengine
import geneGenerator

engine = dnaengine.Engine()
generator = geneGenerator.geneGenerator(5,5)

genes = generator.generateMany(100)

engine.makeDf(df)



def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


resultdict = {}

for i in range(500):
    genes = generator.generateMany(100)
    diction = engine.evaluategenes(genes)
    resultdict = merge_two_dicts(resultdict,diction)
    
def evaluate(resultdict,genes):
    resultdict = merge_two_dicts(resultdict, engine.evaluategenes(genes))



if __name__ == "__main__":
    with Manager() as manager:
        L = manager.dict()  # <-- can be shared between processes.
        processes = []
        for i in tqdm(range(10)):
            genes = generator.generateMany(100)
            p = Process(target=evaluate, args=(L,genes))  # Passing the list
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        print(L)