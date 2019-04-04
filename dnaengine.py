# -*- coding: utf-8 -*-
import numpy as np
import collections
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

class Engine:
    def __init__(self):
        pass
    
    def makeDf(self,df):
        #first run the return from 1-20
        for i in range(20):
            df['r%d'%(i+1)] = df['Close'].pct_change(i+1).shift(-(i+1))
            
        #Make 5 spread of different bar-size
        for i in range(10):
            df['%dbHigh'%(i+1)] = df['High'].rolling(i+1).max()
            df['%dbLow'%(i+1)] = df['Low'].rolling(i+1).min()

            #Calculate i bar spread
            df['%dSpread'%(i+1)] = df['%dbHigh'%(i+1)] - df['%dbLow'%(i+1)]
            df['Close+%d'%(i+1)] = df['Close'].shift(i+1)
            
            df['%dSpreadWPolarity'%(i+1)] = df['Close'] - df['Close+%d'%(i+1)]
        
        
        self.df = df[10:]

        #Make bin for those spreads
        self.binDict = {}
        
        #replace 0.1% extreme value with their 0.5% extreme value percentile.
        
        
        for i in range(10):
            self.binDict[i+1] = self.makeBin(df['%dSpreadWPolarity'%(i+1)][5:].tolist());


    def makeBin(self,data):
        #bin of fixed size of 20
        num_bins = 20
        data = np.sort(data)
        
        data_points_per_bin = len(data) // 20

        bins = [data[_ * data_points_per_bin: (_+1)*data_points_per_bin] for _ in range(num_bins)]

        binLevel = []
        
        for l in bins:
            binLevel.append(min(l))    
        
        binLevel.append(max(bins[-1]))
        
        binLevel = np.array(binLevel)
        binLevel.sort()
        return binLevel
        
    
    def drawDna(self, gene):
        ###need to be changed
        dictTuples = []
        x = []
        y = []
        for i in range(5):
            x.append(gene[2*i])
            y.append(gene[2*i+1])
            
        for i in range(len(x)):
            dictTuples.append((x[i],[self.binDict[x[i]][y[i]-1],self.binDict[x[i]][y[i]]]))
        
        currentLine = ([0,0],[0,0])
        
        for i in range(len(dictTuples)):
            x1 = currentLine[0][1]
            x2 = dictTuples[i][0] + currentLine[0][1]
            y1 = currentLine[1][1]
            y2 = dictTuples[i][1][1] + currentLine[1][1]
    
            plt.plot([x1,x2],[y1,y2],'--', color='g', lw= 0.8)
            currentLine[0][0] = x1
            currentLine[0][1] = x2
            currentLine[1][0] = y1
            currentLine[1][1] = y2
            
        currentLine = ([0,0],[0,0])
        
        
        for i in range(len(dictTuples)):
            x1 = currentLine[0][1]
            x2 = dictTuples[i][0] + currentLine[0][1]
            y1 = currentLine[1][1]
            y2 = dictTuples[i][1][0] + currentLine[1][1]
    
            plt.plot([x1,x2],[y1,y2],'--', color='r', lw= 0.8)
            currentLine[0][0] = x1
            currentLine[0][1] = x2
            currentLine[1][0] = y1
            currentLine[1][1] = y2
            
            
    def draw100Dna(self, genes):
        fig = plt.figure(figsize=(20,20))
        fig.suptitle('price movement genes')
        for i in range(100):
            plt.subplot(10,10,i+1)
                    ###need to be changed
            gene = genes[i]
            dictTuples = []
            x = []
            y = []
            #needed attention
            for i in range(5):
                x.append(gene[2*i])
                y.append(gene[2*i+1])
            
            for i in range(len(x)):
                dictTuples.append((x[i],[self.binDict[x[i]][y[i]-1],self.binDict[x[i]][y[i]]]))
        
            currentLine = ([0,0],[0,0])
        
            for i in range(len(dictTuples)):
                x1 = currentLine[0][1]
                x2 = dictTuples[i][0] + currentLine[0][1]
                y1 = currentLine[1][1]
                y2 = dictTuples[i][1][1] + currentLine[1][1]
    
                plt.plot([x1,x2],[y1,y2],'--', color='g', lw= 0.8)
                
                currentLine[0][0] = x1
                currentLine[0][1] = x2
                currentLine[1][0] = y1
                currentLine[1][1] = y2
            
            currentLine = ([0,0],[0,0])
        
        
            for i in range(len(dictTuples)):
                x1 = currentLine[0][1]
                x2 = dictTuples[i][0] + currentLine[0][1]
                y1 = currentLine[1][1]
                y2 = dictTuples[i][1][0] + currentLine[1][1]
    
                plt.plot([x1,x2],[y1,y2],'--', color='r', lw= 0.8)
                currentLine[0][0] = x1
                currentLine[0][1] = x2
                currentLine[1][0] = y1
                currentLine[1][1] = y2
        plt.tight_layout()
            
            
    def decode(self,gene):
        
        tempdf = self.df
        lengthgene = []
        bingene = []
        for i in range(int(len(gene)/2)):
            lengthgene.append(gene[2*i])
            bingene.append(gene[2*i + 1])
        
        interval = 0
        temporaldf = tempdf
        for i in range(len(lengthgene) - 1):
            tempindex = temporaldf.index + interval
            temporaldf = tempdf.loc[tempindex]
            temporaldf = temporaldf[temporaldf['%dSpreadWPolarity'%(lengthgene[i])] < self.binDict[lengthgene[i]][bingene[i]]]
            temporaldf = temporaldf[temporaldf['%dSpreadWPolarity'%(lengthgene[i])] >= self.binDict[lengthgene[i]][bingene[i] - 1]]
            
            interval = lengthgene[i + 1]
            
        return self.valueMethod1(temporaldf)


    #Pure expected value method.
    #meta 0 : mean
    #meta 1: polarity
    #meta 2: size
    
    def valueMethod1(self, temporaldf):
        meta = []
        meta.append(temporaldf['r2'].mean())
        meta.append(len(temporaldf['r2']) / len(self.df) * 86400.0)
        meta.append(sum(temporaldf['r2'] > 0) / len(temporaldf))
        meta.append(len(temporaldf))
        return meta
    
    def evaluategenes(self, genes):
        geneDict = {}
        for gene in tqdm(genes):
            geneDict[repr(gene)] = self.decode(gene)
        sorted(geneDict.values())
        return geneDict

###Things to improve###
#1. Dynamic bin size, more bins around data points with more density#
