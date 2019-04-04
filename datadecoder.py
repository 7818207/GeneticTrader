#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:13:59 2019

@author: james
"""
import pandas as pd
import quickEngine as qe
import ast
import numpy as np

class DataDecoder:
    
    def __init__(self):
        self.evaluation_method_4()
        
        
        
        
        
        
        
    def evaluation_method_4(self):
        #First step is to get lowest 30% for all r1
        
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
        temp = temp.head(int(len(temp) * 0.3))
        
        
        self.usabledf = temp
        genes = temp.index.tolist()
        pool_genes = []
        for x in genes:
            pool_genes.append(ast.literal_eval(x))
        self.genes = pool_genes
        df = pd.read_csv('df.csv')
        _, self.binDict = qe.makeDf(df)
        self.inverseGenes()
        
        
        
    #Only aim for those strategy that has success rate of more than 80%, take r6 instead of r5
    def evaluation_method_3(self):
        
        self.filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        
        self.filedf.sort_values('r6posrate',inplace = True,ascending=False)
        
        #take by posrate and negrate
        upper = self.filedf[self.filedf['r6posrate'] >= 0.8]
        upper = upper[upper['total_hits'] >= 10]
        lower = self.filedf[self.filedf['r6negrate'] >= 0.8]
        lower = lower[lower['total_hits'] >= 10]
        
        temp = pd.concat([upper,lower])

        #70% by viability
        temp['r6difference'] = temp['r6posrate'] - temp['r6negrate']
        temp['r6viable'] = temp['r6difference'] * temp['r6mean']
        
        temp = temp[temp['r6viable'] > 0]
        
        
        self.usabledf = temp
        
        genes = temp.index.tolist()
        pool_genes = []
        for x in genes:
            pool_genes.append(ast.literal_eval(x))
        self.genes = pool_genes
        df = pd.read_csv('df.csv')
        _, self.binDict = qe.makeDf(df)
        self.inverseGenes()
        
    #1. rank by frequency, take 50%
    def evaluation_method_2(self):
        self.filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        
        self.filedf.sort_values('total_hits',inplace = True,ascending=False)
        
        #take the upper 50%
        temp = self.filedf.head(int(len(self.filedf)*0.5))
        
        #take 50% by mean
        temp.sort_values('r5mean',inplace = True,ascending=False)
        how_many_to_take = int(len(self.filedf) * 0.25)
        temp = pd.concat([temp.head(how_many_to_take),temp.tail(how_many_to_take)])

        #70% by viability
        temp['r5difference'] = temp['r5posrate'] - temp['r5negrate']
        temp['r5viable'] = temp['r5difference'] * temp['r5mean']
        
        temp.sort_values('r5viable',inplace = True,ascending=False)
        
        temp = temp.head(int(len(temp) * 0.3))
        
        self.usabledf = temp
        
        genes = temp.index.tolist()
        pool_genes = []
        for x in genes:
            pool_genes.append(ast.literal_eval(x))
        self.genes = pool_genes
        df = pd.read_csv('df.csv')
        _, self.binDict = qe.makeDf(df)
        self.inverseGenes()
        
        
    #This is a expectation bound method
    def evaluation_method_1(self):
        self.filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
        
        self.filedf.sort_values('r5mean',inplace = True,ascending=False)
        #take highest and lowest 30% return
        
        how_many_to_take = int(len(self.filedf)*0.3)
        
        temp = pd.concat([self.filedf.head(how_many_to_take),self.filedf.tail(how_many_to_take)])
        
        temp['r5difference'] = temp['r5posrate'] - temp['r5negrate']
        temp['r5viable'] = temp['r5difference'] * temp['r5mean']
        temp = temp[temp['r5viable'] > 0]
        temp.sort_values('total_hits',inplace=True,ascending=False)
        temp = temp.tail(int(len(temp)*0.8))
        
        temp.sort_values('r5mean',inplace=True,ascending=False)
        
        temp['r5meanabs'] = abs(temp['r5mean'])
        temp.sort_values('r5meanabs',inplace=True,ascending=False)
        temp = temp[temp['total_hits'] > 10]
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
    

            
'''
#Pass in realtime data, genes, and binDict, return genes that are matched.
def findMatch(df,genes,binDict):
    for i in range(20):
        df['r%d'%(i+1)] = df['close'].pct_change(i+1).shift(-(i+1))
    
    for i in range(10):
            #df['%dbHigh'%(i+1)] = df['High'].rolling(i+1).max()
            #df['%dbLow'%(i+1)] = df['Low'].rolling(i+1).min()

            #Calculate i bar spread
            #df['%dSpread'%(i+1)] = df['%dbHigh'%(i+1)] - df['%dbLow'%(i+1)]
        df['Close+%d'%(i+1)] = df['close'].shift(i+1)
        df['%dSpreadWPolarity'%(i+1)] = df['close'] - df['Close+%d'%(i+1)]
        df['%dBin'%(i+1)] = np.digitize(df['%dSpreadWPolarity'%(i+1)],binDict[i+1])
    df = df[10:]
    '''

'''
geneLocators = []
for gene in dd.inversedGenes:
    locators = []
    locators.append(0)
    locators.append(gene[0]+locators[0])
    locators.append(locators[1]+gene[2])
    locators.append(locators[2]+gene[4])
    locators.append(locators[3]+gene[6])
    geneLocators.append(locators)
    
binLocators = []
for gene in dd.inversedGenes:
    locators = []
    locators.append(gene[0])
    locators.append(gene[2])
    locators.append(gene[4])
    locators.append(gene[6])
    locators.append(gene[8])
    binLocators.append(locators)
    
    
bins = []
for (gene,bind) in zip(geneLocators,binLocators):
    bin = []
    for (index, binl) in zip(gene, bind):
        bin.append(data.iloc[index]['%dBin'%binl])
        
    bins.append(bin)
        


search = []
global globalflag
globalflag = True

def match_search(li,pool_genes):
    global globalflag
    if globalflag == True:  
        if(len(li) == 10):
            search.append(li)
            print('10')
            return
        if(len(pool_genes) == 0):
            search.append('x')
            print('zero')
            return
        print('not 10 not zero')
        gene = li
        latest = li[-1]
        if(len(li)%2 != 0):
            print('old search')
            index = 0
            for i in range(len(li) - 1):
                if(i %2 == 0):
                    index += li[i]
            print('gene before %s'%gene)
            gene.append(data.iloc[index]['%dBin'%(latest)])
            print('gene after %s'%gene)
            pool = []
            for ge in pool_genes:
                flag = True
                for i in range(len(gene)):
                    if(ge[i] != gene[i]):
                        flag = False
                if flag:
                    pool.append(ge)
            print('pool length %d'%len(pool))
            if(len(pool) == 0):
                globalflag = False;
            match_search(gene,pool)
        print('even search %s'%gene)
        pool = pool_genes
        geneappendix = []
        for ge in pool:
            geneappendix.append(ge[len(gene)])
        geneappendix = list(set(geneappendix))
        for dix in geneappendix:
            gene.append(dix)
            print('new gene even search %s'%(gene))
            match_search(gene,pool)
        
        
def match_search(li,pool_genes):
    gene = li
    latest = li[-1]
    if(len(pool_genes) == 0):
        return 
    if(len(gene) % 2 != 0):
        index = 0
        for i in range(len(li) - 1):
            if(i %2 == 0):
                index += li[i]
        print('gene before %s'%gene)
        gene.append(data.iloc[index]['%dBin'%(latest)])
        print('gene after %s'%gene)
        pool = []
        for ge in pool_genes:
            flag = True
            for i in range(len(gene)):
                if(ge[i] != gene[i]):
                    flag = False
            if flag:
                pool.append(ge)
        match_search(gene,pool)
    if(len(gene) == 10):
        return li[-2:]
    if(len(pool_genes) == 0):
        return 
    pool = pool_genes
    geneappendix = []
    for ge in pool:
        geneappendix.append(ge[len(gene)])
    geneappendix = list(set(geneappendix))
    for dix in geneappendix:
        gene.append(dix)
        print('new gene even search %s'%(gene))
        match_search(gene,pool)
        

gene.append(gene)
    if(len(gene) % 2 != 0):
        index = 0
        for i in range(len(gene) - 1):
            if(i %2 == 0):
                index += gene[i]
        gene.append(data.iloc[index]['%dBin'%(latest)])
        bucket.append(gene)
    
    

#Take gene, return next gene or list of next genes
bucket = []
def get_bucket_depth():
    lengthlist = []
    for b in bucket:
        lengthlist.append(len(b))
    return max(lengthlist)

def append_to_bucket(gene):
    latest = gene[-1]
    tempgene = gene
    if(len(tempgene) % 2 != 0):
        index = 0
        for i in range(len(tempgene) - 1):
            if(i %2 == 0):
                index += tempgene[i]
        tempgene.append(data.iloc[index]['%dBin'%(latest)])
        bucket.append(tempgene)
        return
    if(len(tempgene) %2 == 0):
        for ge in pool_genes:
            flag = True
            for i in range(len(tempgene)):
                if(ge[i] != tempgene[i]):
                    flag = False
            if flag:
                bucket.append(ge[0:len(tempgene)+1])
            
def bucket_search():
    global bucket
    maxlength = get_bucket_depth()
    list_of_max_length = []
    for b in bucket:
        if(len(b) == maxlength):
            list_of_max_length.append(b)
    
    for l in list_of_max_length:
        append_to_bucket(l)
    b_set = set(tuple(x) for x in bucket)
    bucket = [ list(x) for x in b_set ]
    return


bucket = []
for i in range(10):
    bucket.append([i+1])
depth = 0
bucketdepth = get_bucket_depth()
while(depth != bucketdepth):
    depth = get_bucket_depth()
    bucket_search()
    bucketdepth = get_bucket_depth()
    




for b in bucket:
    if(len(b) == maxlength):
        list_of_max_length.append(b)
'''

'''

bucketcopy = bucket
genepoolcopy = genepool
bucket = []
genepool = []
for g,p in zip(bucketcopy,genepoolcopy):
    evaluate(g,p)

def evaluate(g,p):
    if(len(g) %2 != 0):
        evaluate_odd(g,p)
    else:
        evaluate_even(g,p)
        
def evaluate_odd(genecopy,poolcopy):
    tempgene = genecopy
    index = 0
    latest = tempgene[-1]
    for i in range(len(tempgene) - 1):
        if(i %2 == 0):
            index += tempgene[i]
    tempgene.append(data.iloc[index]['%dBin'%(latest)])
    bucket.append(tempgene)
    genepool.append(poolcopy)

def evaluate_even(genecopy,poolcopy):
    tempgene = genecopy
    pool = []
    for ge in poolcopy:
        flag = True
        for i in range(len(tempgene)):
            if(ge[i] != tempgene[i]):
                flag = False
        if flag:
            pool.append(ge)
            if ge[0:len(tempgene)+1] in bucket:
                pass
            else:
                newgene = ge[0:len(tempgene)+1]
                bucket.append(newgene)
                genepool.append(pool)

    
for i in range(10):
    bucket.append([i+1])
    genepool.append(pool_genes)
'''