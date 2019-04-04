# -*- coding: utf-8 -*-

import pandas as pd
import quickEngine
import numpy as np
import geneGenerator
from multiprocessing import Process, Manager, Pool
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import time
import multiprocessing
import multiprocessing.pool

df = pd.read_csv('df.csv')

column_index_value_dict, binDict = quickEngine.makeDf(df)
generator = geneGenerator.geneGenerator(5,10,20)



'''
genes = generator.generateMany(100)
factsheetdict = evaluategenes(genes,column_index_value_dict)


factsheetdf = pd.DataFrame.from_dict(factsheetdict,orient='index',columns=['hits_per_day','total_hits','r2mean','r2posrate','r2negrate','r3mean','r3posrate','r3negrate','r4mean','r4posrate','r4negrate','r5mean','r5posrate','r5negrate','r6mean','r6posrate','r6negrate','r7mean','r7posrate','r7negrate','r8mean','r8posrate','r8negrate','r9mean','r9posrate','r9negrate','r10mean','r10posrate','r10negrate'])


genes = generator.generateMany(1000)
factsheetdict = evaluategenes(genes,column_index_value_dict)
factsheetdf = pd.DataFrame.from_dict(factsheetdict,orient='index',columns=['hits_per_day','total_hits','r2mean','r2posrate','r2negrate','r3mean','r3posrate','r3negrate','r4mean','r4posrate','r4negrate','r5mean','r5posrate','r5negrate','r6mean','r6posrate','r6negrate','r7mean','r7posrate','r7negrate','r8mean','r8posrate','r8negrate','r9mean','r9posrate','r9negrate','r10mean','r10posrate','r10negrate'])
factsheetdf.drop_duplicates(inplace = True)
'''


def evaluate200(i):
    genes = generator.generateMany(200)
    factsheetdict = quickEngine.evaluategenes(genes,column_index_value_dict,binDict,df)
    mdict.update(factsheetdict)
    
    
    '''if(i % 200 == 0):
        factsheetdict = dict(mdict)
        factsheetdf = pd.DataFrame.from_dict(factsheetdict,orient='index',columns=['hits_per_day','total_hits','r2mean','r2posrate','r2negrate','r3mean','r3posrate','r3negrate','r4mean','r4posrate','r4negrate','r5mean','r5posrate','r5negrate','r6mean','r6posrate','r6negrate','r7mean','r7posrate','r7negrate','r8mean','r8posrate','r8negrate','r9mean','r9posrate','r9negrate','r10mean','r10posrate','r10negrate'])
        filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        finaldf = pd.concat([filedf,factsheetdf])
        finaldf.drop_duplicates(inplace = True)
        finaldf.to_csv('factsheetdf.csv')
        m = Manager()
        mdict = m.dict()'''
'''
for i in range(200):
    evaluate200()
    
    
if __name__ == '__main__':
    jobs = []
    while(1):
        for i in range(8):
            p = Process(target=evaluate200)
            jobs.append(p)
            p.start()
            time.sleep(500)'''
        
        
class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)
    
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

     


while(1):
    m = Manager()
    mdict = m.dict()
    pool = MyPool(processes=6)
    pool.map(evaluate200,[i for i in range(6)])
    print('finished')
    
    factsheetdict = dict(mdict)
    factsheetdf = pd.DataFrame.from_dict(factsheetdict,orient='index',columns=['hits_per_day','total_hits','r2mean','r2posrate','r2negrate','r3mean','r3posrate','r3negrate','r4mean','r4posrate','r4negrate','r5mean','r5posrate','r5negrate','r6mean','r6posrate','r6negrate','r7mean','r7posrate','r7negrate','r8mean','r8posrate','r8negrate','r9mean','r9posrate','r9negrate','r10mean','r10posrate','r10negrate'])
    filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
    finaldf = pd.concat([filedf,factsheetdf])
    finaldf.drop_duplicates(inplace = True)
    finaldf.to_csv('factsheetdf.csv')
    print('1')
    pool.close()
    pool.join()
    print('2')
    del factsheetdict
    del factsheetdf
    del finaldf
    print('3')
    time.sleep(30)