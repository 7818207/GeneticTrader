# -*- coding: utf-8 -*-


#quick version of dnaEngine, used in multiprocessing

import matplotlib.pyplot as plt
import bisect
from tqdm import tqdm
import numpy as np

#return a list containing bins, helper function for makeDf
def makeBin(data):
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



#return a meta dictionary of type dictionary, the key is column name from dataframe, and value is array of corresponding values
#the returned value should be sorted in ascending order and their is a corresponding index list
def makeDf(df):
    for i in range(20):
        df['r%d'%(i+1)] = df['Close'].pct_change(i+1).shift(-(i+1))
    
    for i in range(10):
            #df['%dbHigh'%(i+1)] = df['High'].rolling(i+1).max()
            #df['%dbLow'%(i+1)] = df['Low'].rolling(i+1).min()

            #Calculate i bar spread
            #df['%dSpread'%(i+1)] = df['%dbHigh'%(i+1)] - df['%dbLow'%(i+1)]
        df['Close+%d'%(i+1)] = df['Close'].shift(i+1)
        df['%dSpreadWPolarity'%(i+1)] = df['Close'] - df['Close+%d'%(i+1)]
        
    binDict = {}
        

    for i in range(10):
        binDict[i+1] = makeBin(df['%dSpreadWPolarity'%(i+1)][5:].tolist());
    #Triming step ---Must go hand in hand
    df = df[10:]
    
    
    column_index_value_dict = {}
    
    for i in range(10):
        index_value_list = []
        df = df.sort_values('%dSpreadWPolarity'%(i+1))
        value_list = df['%dSpreadWPolarity'%(i+1)].tolist()
        index_list = df.index.tolist()
        index_value_list.append(index_list)
        index_value_list.append(value_list)
        
        column_index_value_dict['%dSpreadWPolarity'%(i+1)] = index_value_list
    return column_index_value_dict, binDict
        

def draw100dna(genes,binDict):
    fig = plt.figure(figsize=(20,20))
    fig.suptitle('price movement genes')
    for i in range(100):
        plt.subplot(10,10,i+1)
                    ###need to be changed
        gene = genes[i]
        dictTuples = []
        x = []
        y = []
        for i in range(5):
            x.append(gene[2*i])
            y.append(gene[2*i+1])
            
        for i in range(len(x)):
            dictTuples.append((x[i],[binDict[x[i]][y[i]-1],binDict[x[i]][y[i]]]))
        
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
    time.sleep(1)
    
    
def valueMethod1(temporaldf,df):
    factlist = []
    factlist.append(len(temporaldf) / len(df) * 61714.3)
    factlist.append(len(temporaldf))
    for i in range(9):
        try:
            factlist.append(temporaldf['r%d'%(i+2)].mean())
            factlist.append(sum(temporaldf['r%d'%(i+2)] > 0) / len(temporaldf))
            factlist.append(sum(temporaldf['r%d'%(i+2)] < 0) / len(temporaldf))
        except ZeroDivisionError:
            pass
    return factlist
    
def evaluategenes(genes,column_index_value_dict,binDict,df):
    geneDict = {}
    for gene in tqdm(genes):
        geneDict[repr(gene)] = decode(gene,column_index_value_dict,binDict,df)
    return geneDict
        
def decode(gene,column_index_value_dict,binDict,df):
        
    lengthgene = []
    bingene = []
    for i in range(int(len(gene)/2)):
        lengthgene.append(gene[2*i])
        bingene.append(gene[2*i + 1])
        
    interval = 0
    list_of_index = set(column_index_value_dict['1SpreadWPolarity'][0])
    for i in range(len(lengthgene) - 1):
        list_of_index = np.array(list(list_of_index))+interval
        lowBound = bisect.bisect_left(column_index_value_dict['%dSpreadWPolarity'%(lengthgene[i])][1],binDict[lengthgene[i]][bingene[i] - 1])
        upBound = bisect.bisect_right(column_index_value_dict['%dSpreadWPolarity'%(lengthgene[i])][1],binDict[lengthgene[i]][bingene[i]])
        list_of_index = set(column_index_value_dict['%dSpreadWPolarity'%(lengthgene[i])][0][lowBound:upBound]).intersection(list_of_index)
        
        interval = lengthgene[i + 1]
            
    return valueMethod1(df.iloc[list(list_of_index)],df)