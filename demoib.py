#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:39:31 2019

@author: james
"""



import pandas as pd
import numpy as np

import datadecoder




#sorting filedf get usable df

#sorting priority.
#1. mean 0.6
#2. no.hits 0.8
#3. rate,difference 0.5
filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')

filedf.sort_values('r5mean',inplace = True,ascending=False)
#take highest and lowest 30% return
how_many_to_take = int(len(filedf)*0.3)

temp = pd.concat([filedf.head(how_many_to_take),filedf.tail(how_many_to_take)])

temp['r5difference'] = temp['r5posrate'] - temp['r5negrate']
temp['r5viable'] = temp['r5difference'] * temp['r5mean']
temp = temp[temp['r5viable'] > 0]
temp.sort_values('total_hits',inplace=True,ascending=False)
temp = temp.tail(int(len(temp)*0.8))

temp.sort_values('r5mean',inplace=True,ascending=False)

temp['r5meanabs'] = abs(temp['r5mean'])
temp.sort_values('r5meanabs',inplace=True,ascending=False)
temp = temp[temp['total_hits'] > 10]

genes = temp.index.tolist()


import ast
pool_genes = []
for x in genes:
    pool_genes.append(ast.literal_eval(x))



#DATAFRAME RECEIVED AS data
def makedataDf(df):
    for i in range(20):
        df['r%d'%(i+1)] = df['close'].pct_change(i+1).shift(-(i+1))
    
    for i in range(10):
            #df['%dbHigh'%(i+1)] = df['High'].rolling(i+1).max()
            #df['%dbLow'%(i+1)] = df['Low'].rolling(i+1).min()

            #Calculate i bar spread
            #df['%dSpread'%(i+1)] = df['%dbHigh'%(i+1)] - df['%dbLow'%(i+1)]
        df['Close+%d'%(i+1)] = df['close'].shift(i+1)
        df['%dSpreadWPolarity'%(i+1)] = df['close'] - df['Close+%d'%(i+1)]
    df = df[10:]
    #inverse data
    df = df.iloc[::-1].reset_index(drop=True)
    
    
#inverse genes
inversedGenes = []
for gene in pool_genes:
    newgene = []
    newgene.append(gene[8])
    newgene.append(gene[9])
    newgene.append(gene[6])
    newgene.append(gene[7])
    newgene.append(gene[4])
    newgene.append(gene[5])
    newgene.append(gene[2])
    newgene.append(gene[3])
    newgene.append(gene[0])
    newgene.append(gene[1])
    inversedGenes.append(newgene)
    
