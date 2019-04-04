#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 23:18:21 2019

@author: james
"""

import pandas as pd
import quickEngine as qe
import ast
import numpy as np
from operator import itemgetter

class BetaDecoder:
    
    def __init__(self):
        self.evaluation_method_5()
        
        
        
        
        
    def evaluation_method_6(self):
        self.filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        self.filedf['r7-r2'] = self.filedf['r7mean'] - self.filedf['r2mean']
        self.filedf['r7-r2samesign'] = self.filedf['r2mean'] * self.filedf['r7-r2'] > 0
        #for those that are of the same sign, take the highest
        self.filedf.sort_values('r7-r2',inplace = True,ascending=False)
        upper = self.filedf.head(int(len(self.filedf)*0.4))
        upperdiffsign = upper[upper['r7-r2samesign'] == False]
        uppersamesign = upper[upper['r7-r2samesign'] == True]
        lower = self.filedf.tail(int(len(self.filedf)*0.4))
        lowersamesign =  lower[lower['r7-r2samesign'] == True]
        lowerdiffsign = lower[lower['r7-r2samesign'] == False]
        
        diffsigntemp = pd.concat([upperdiffsign,lowerdiffsign])
        samesigntemp = pd.concat([uppersamesign,lowersamesign])
        diffsigntemp['r7divr2'] = (diffsigntemp['r7-r2'])/ abs(diffsigntemp['r2mean'])
        
        samesigntemp['r7divr2'] = (samesigntemp['r7-r2']) / samesigntemp['r2mean']
        
        samesigntemp.sort_values('r7divr2',inplace = True,ascending=False)
        diffsigntemp.sort_values('r7divr2',inplace = True,ascending=False)
        #take 20% from them
        samesigntemp = samesigntemp.head(int(len(samesigntemp)*0.2))
        diffsigntemp = diffsigntemp.head(int(len(diffsigntemp)*0.2))
        
        temp = pd.concat([samesigntemp,diffsigntemp])
        
        temp['r7-r2viable'] = temp['r7-r2']*(temp['r7posrate']-temp['r7negrate'])
        temp.sort_values('r7-r2viable',inplace = True,ascending=False)
        temp = temp.head(int(len(temp) * 0.8))
        
        
        self.usabledf = temp
        genes = temp.index.tolist()
        pool_genes = []
        for x in genes:
            pool_genes.append(ast.literal_eval(x))
        self.genes = pool_genes
        df = pd.read_csv('df.csv')
        _, self.binDict = qe.makeDf(df)
        self.inverseGenes()
        
        
    def evaluation_method_5(self):
        self.filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        self.filedf.dropna(inplace=True)
        self.filedf = self.filedf[self.filedf['total_hits'] >= 20]
        temp = self.filedf
        
        
        self.usabledf = temp
        genes = temp.index.tolist()
        pool_genes = []
        for x in genes:
            pool_genes.append(ast.literal_eval(x))
        self.genes = pool_genes
        df = pd.read_csv('df.csv')
        _, self.binDict = qe.makeDf(df)
        self.inverseGenes()
        
    
    def evaluation_method_4(self):
        #First step is to get lowest 30% for all r1
        
        self.filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        self.filedf.dropna(inplace=True)
        #Calculate deal price, 
        self.filedf['r0mean'] = (self.filedf['r2mean'] - 0) * 0.3
        self.filedf['r1mean'] = self.filedf['r0mean'] + (self.filedf['r2mean'] - self.filedf['r0mean'])/2
        self.filedf['deal2'] = self.filedf['r2mean'] + (self.filedf['r3mean'] - self.filedf['r2mean']) * 0.3
        self.filedf['deal3'] = self.filedf['r3mean'] + (self.filedf['r4mean'] - self.filedf['r3mean']) * 0.3
        self.filedf['deal4'] = self.filedf['r4mean'] + (self.filedf['r5mean'] - self.filedf['r4mean']) * 0.3
        self.filedf['deal5'] = self.filedf['r5mean'] + (self.filedf['r6mean'] - self.filedf['r5mean']) * 0.3
        self.filedf['deal6'] = self.filedf['r6mean'] + (self.filedf['r7mean'] - self.filedf['r6mean']) * 0.3
        self.filedf['deal7'] = self.filedf['r7mean'] + (self.filedf['r8mean'] - self.filedf['r7mean']) * 0.3
        self.filedf['deal8'] = self.filedf['r8mean'] + (self.filedf['r9mean'] - self.filedf['r8mean']) * 0.3
        self.filedf['deal9'] = self.filedf['r9mean'] + (self.filedf['r10mean'] - self.filedf['r9mean']) * 0.3
        self.filedf['highest'] = self.filedf[['r0mean','r1mean','r2mean','r3mean','r4mean','r5mean','r6mean','r7mean','r8mean','r9mean']].max(axis=1)
        self.filedf['lowest'] = self.filedf[['r0mean','r1mean','r2mean','r3mean','r4mean','r5mean','r6mean','r7mean','r8mean','r9mean']].min(axis=1)
        self.filedf['profit'] = self.filedf['highest'] - self.filedf['lowest']
        self.filedf['risk'] = self.filedf['profit'] / 2
        
        self.filedf['maxname'] = self.filedf[['r0mean','r1mean','r2mean','r3mean','r4mean','r5mean','r6mean','r7mean','r8mean','r9mean']].idxmax(axis=1)
        self.filedf['minname'] = self.filedf[['r0mean','r1mean','r2mean','r3mean','r4mean','r5mean','r6mean','r7mean','r8mean','r9mean']].idxmin(axis=1)
        maxlist = list(map(itemgetter(1), self.filedf['maxname'].values))
        self.filedf['maxtime'] = maxlist
        self.filedf["maxtime"] = pd.to_numeric(self.filedf["maxtime"])
        minlist = list(map(itemgetter(1), self.filedf['minname'].values))
        self.filedf['mintime'] = minlist
        self.filedf["mintime"] = pd.to_numeric(self.filedf["mintime"])
        self.filedf['order_type'] = self.filedf['maxtime'] > self.filedf['mintime']
        
        self.filedf['placetimebuy'] = self.filedf['mintime']*60
        self.filedf['endtimebuy'] = self.filedf['maxtime']*60
        
        self.filedf['placetimesell'] = self.filedf['maxtime']*60
        self.filedf['endtimesell'] = self.filedf['mintime']*60
        
        
        self.filedf.sort_values('profit',inplace = True,ascending=False)
        self.filedf = self.filedf[self.filedf['total_hits'] >= 20]
        self.filedf.sort_values('profit',inplace = True,ascending=False)
        self.filedf = self.filedf.head(int(len(self.filedf)*0.5))
        temp = self.filedf
        
        
        self.usabledf = temp
        genes = temp.index.tolist()
        pool_genes = []
        for x in genes:
            pool_genes.append(ast.literal_eval(x))
        self.genes = pool_genes
        df = pd.read_csv('df.csv')
        _, self.binDict = qe.makeDf(df)
        self.inverseGenes()
        
    
    
    def inverseGenes(self):
        poolgenes = self.genes
        inversedGenes = []
        for gene in poolgenes:
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
        self.inversedGenes = inversedGenes
        self.genes = []


    #Get raw data downloaded from ibkr,return 1 for buy order, 0 for sell order
    def findMatch(self,df):
        for i in range(20):
            df['r%d'%(i+1)] = df['close'].pct_change(i+1).shift(-(i+1))
    
        for i in range(10):
            #df['%dbHigh'%(i+1)] = df['High'].rolling(i+1).max()
            #df['%dbLow'%(i+1)] = df['Low'].rolling(i+1).min()

            #Calculate i bar spread
            #df['%dSpread'%(i+1)] = df['%dbHigh'%(i+1)] - df['%dbLow'%(i+1)]
            df['Close+%d'%(i+1)] = df['close'].shift(i+1)
            df['%dSpreadWPolarity'%(i+1)] = df['close'] - df['Close+%d'%(i+1)]
            df['%dBin'%(i+1)] = np.digitize(df['%dSpreadWPolarity'%(i+1)],self.binDict[i+1])
        df = df[10:]
        df = df.iloc[::-1].reset_index(drop=True)
        self.data = df
        
        
        #finding match
        self.bucket = []
        self.genepool = []
        for i in range(10):
            self.bucket.append([i+1])
            self.genepool.append(self.inversedGenes)
        for i in range(9):
            self.bucketcopy = self.bucket
            self.genepoolcopy = self.genepool
            self.bucket = []
            self.genepool = []
            for g,p in zip(self.bucketcopy,self.genepoolcopy):
                self.evaluate(g,p)
        self.reverseBucket()
        return self.reversedBucket
            
    def evaluate(self,g,p):
        if(len(g) %2 != 0):
            self.evaluate_odd(g,p)
        else:
            self.evaluate_even(g,p)
        
    def evaluate_odd(self,genecopy,poolcopy):
        tempgene = genecopy
        index = 0
        latest = tempgene[-1]
        for i in range(len(tempgene) - 1):
            if(i %2 == 0):
                index += tempgene[i]
        tempgene.append(self.data.iloc[index]['%dBin'%(latest)])
        self.bucket.append(tempgene)
        self.genepool.append(poolcopy)

    def evaluate_even(self,genecopy,poolcopy):
        tempgene = genecopy
        pool = []
        for ge in poolcopy:
            flag = True
            for i in range(len(tempgene)):
                if(ge[i] != tempgene[i]):
                    flag = False
            if flag:
                pool.append(ge)
                if ge[0:len(tempgene)+1] in self.bucket:
                    pass
                else:
                    newgene = ge[0:len(tempgene)+1]
                    self.bucket.append(newgene)
                    self.genepool.append(pool)
                    
    def reverseBucket(self):
        reversedBucket = []
        for b in self.bucket:
            buc = []
            buc.append(b[8])
            buc.append(b[9])
            buc.append(b[6])
            buc.append(b[7])
            buc.append(b[4])
            buc.append(b[5])
            buc.append(b[2])
            buc.append(b[3])
            buc.append(b[0])
            buc.append(b[1])
            reversedBucket.append(repr(buc))
        self.reversedBucket = reversedBucket