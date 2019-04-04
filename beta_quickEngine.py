# -*- coding: utf-8 -*-


#quick version of dnaEngine, used in multiprocessing

import matplotlib.pyplot as plt
import bisect
from tqdm import tqdm
import numpy as np
import ast
import warnings

import pandas as pd
import re 

#return a list containing bins, helper function for makeDf

def __init__(self):
    self.df = pd.read_csv('df.csv')
    self.column_index_value_dict,self.binDict = makeDf(self.df)
    self.RbinDict = makeRDf(self.df)

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

#result binDict
def makeRBin(data):
    #bin of fixed size of 20
    num_bins = 10
    data = np.sort(data)
        
    data_points_per_bin = len(data) // 10

    bins = [data[_ * data_points_per_bin: (_+1)*data_points_per_bin] for _ in range(num_bins)]

    binLevel = []
        
    for l in bins:
        binLevel.append(min(l))    
        
    binLevel.append(max(bins[-1]))
        
    binLevel = np.array(binLevel)
    binLevel.sort()
    
    return binLevel
    


def makeRDf(df):
    for i in range(20):
        df['r%d'%(i+1)] = df['Close'].pct_change(i+1).shift(-(i+1))

    binDict = {}

    for i in range(1):
        binDict[i+1] = makeRBin(df['r%d'%(i+1)][5:].tolist());
    #Triming step ---Must go hand in hand


    return  binDict
        

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
            
    return df.iloc[list(list_of_index)]




def appendrbin(tempdf,RbinDict):
    tempdf['r20'] = tempdf['r20'] - tempdf['r19']
    tempdf['r19'] = tempdf['r19'] - tempdf['r18']
    tempdf['r18'] = tempdf['r18'] - tempdf['r17']
    tempdf['r17'] = tempdf['r17'] - tempdf['r16']
    tempdf['r16'] = tempdf['r16'] - tempdf['r15']
    tempdf['r15'] = tempdf['r15'] - tempdf['r14']
    tempdf['r14'] = tempdf['r14'] - tempdf['r13']
    tempdf['r13'] = tempdf['r13'] - tempdf['r12']
    tempdf['r12'] = tempdf['r12'] - tempdf['r11']
    tempdf['r11'] = tempdf['r11'] - tempdf['r10']
    tempdf['r10'] = tempdf['r10'] - tempdf['r9']
    tempdf['r9'] = tempdf['r9'] - tempdf['r8']
    tempdf['r8'] = tempdf['r8'] - tempdf['r7']
    tempdf['r7'] = tempdf['r7'] - tempdf['r6']
    tempdf['r6'] = tempdf['r6'] - tempdf['r5']
    tempdf['r5'] = tempdf['r5'] - tempdf['r4']
    tempdf['r4'] = tempdf['r4'] - tempdf['r3']
    tempdf['r3'] = tempdf['r3'] - tempdf['r2']
    tempdf['r2'] = tempdf['r2'] - tempdf['r1']
    return tempdf


def pos_rate(ser):
    return sum(ser > 0) / ser.count()



def get_strategy_bool(index,stop,limit,action,df):
    end = False
    indexer = index
    terminal_index = len(df)
    start_price = df.iloc[indexer].Close
    while((not end) and (indexer < terminal_index-1)):
        high = df.iloc[indexer].High
        low = df.iloc[indexer].Low
        if(action == 1):
            if(high > start_price + limit):
                return 1
            elif(low < start_price - stop):
                return -1
        elif(action == -1):
            if(high > start_price + stop):
                return -1
            elif(low < start_price - limit):
                return 1
        indexer+=1;
    
    
def get_monte_carlo_stra(gene,column_index_value_dict,binDict,df,RbinDict):
        tempdf = decode(gene,column_index_value_dict,binDict,df)
        tempdf = appendrbin(tempdf,RbinDict)
        tempdf['l2s1bmean'] = 0
        tempdf['l2s1bposrate'] = 0
        
        tempdf['l2s1smean'] = 0
        tempdf['l2s1sposrate'] = 0
        
        tempdf['l4s2bmean'] = 0
        tempdf['l4s2bposrate'] = 0

        tempdf['l4s2smean'] = 0
        tempdf['l4s2sposrate'] = 0
        
        indexex = tempdf.index.tolist()
        
        l2s1b = []
        l2s1s = []
        l4s2b = []
        l4s2s = []
        l8s3b = []
        l8s3s = []
        l9s3b = []
        l9s3s = []
        for i in indexex:
            l2s1b.append(get_strategy_bool(i,0.0001,0.0002,1,df))
            l2s1s.append(get_strategy_bool(i,0.0001,0.0002,-1,df))
            l4s2b.append(get_strategy_bool(i,0.0002,0.0004,1,df))
            l4s2s.append(get_strategy_bool(i,0.0002,0.0004,-1,df))
            l8s3b.append(get_strategy_bool(i,0.0003,0.0008,1,df))
            l8s3s.append(get_strategy_bool(i,0.0003,0.0008,-1,df))
            l9s3b.append(get_strategy_bool(i,0.0003,0.0009,1,df))
            l9s3s.append(get_strategy_bool(i,0.0003,0.0009,-1,df))
            
            tempdf.loc[i]['l2s1bmean'] = np.mean(l2s1b)
            tempdf.loc[i]['l2s1bposrate'] = sum(np.asarray(l2s1b) > 0) / len(l2s1b)
        
            tempdf.loc[i]['l2s1smean'] = np.mean(l2s1s)
            tempdf.loc[i]['l2s1sposrate'] = sum(np.asarray(l2s1s) > 0) / len(l2s1s)
        
            tempdf.loc[i]['l4s2bmean'] = np.mean(l4s2b)
            tempdf.loc[i]['l4s2bposrate'] = sum(np.asarray(l4s2b) > 0) / len(l4s2b)

            tempdf.loc[i]['l4s2smean'] = np.mean(l4s2s)
            tempdf.loc[i]['l4s2sposrate'] = sum(np.asarray(l4s2s) > 0) / len(l4s2s)
    
            tempdf.loc[i]['l8s3bmean'] = np.mean(l8s3b)
            tempdf.loc[i]['l8s3bposrate'] = sum(np.asarray(l8s3b) > 0) / len(l8s3b)
            
            tempdf.loc[i]['l8s3smean'] = np.mean(l8s3s)
            tempdf.loc[i]['l8s3sposrate'] = sum(np.asarray(l8s3s) > 0) / len(l8s3s)     
            
            tempdf.loc[i]['l9s3bmean'] = np.mean(l9s3b)
            tempdf.loc[i]['l9s3bposrate'] = sum(np.asarray(l9s3b) > 0) / len(l9s3b)
            
            tempdf.loc[i]['l9s3smean'] = np.mean(l9s3s)
            tempdf.loc[i]['l9s3sposrate'] = sum(np.asarray(l9s3s) > 0) / len(l9s3s)     
            
            
        result = {'l2s1bmean':np.mean(l2s1b),'l2s1bposrate':sum(np.asarray(l2s1b) > 0) / len(l2s1b),'l2s1smean':np.mean(l2s1s)
        ,'l2s1sposrate':sum(np.asarray(l2s1s) > 0) / len(l2s1s),'l4s2bmean':np.mean(l4s2b),'l4s2bposrate':sum(np.asarray(l4s2b) > 0) / len(l4s2b),
        'l4s2smean':np.mean(l4s2s),'l4s2sposrate':sum(np.asarray(l4s2s) > 0) / len(l4s2s),'l8s3bmean':np.mean(l8s3b),'l8s3bposrate':sum(np.asarray(l8s3b) > 0) / len(l8s3b),'l8s3smean':np.mean(l8s3s),'l8s3sposrate':sum(np.asarray(l8s3s) > 0) / len(l8s3s),'l9s3bmean':np.mean(l9s3b),'l9s3bposrate':sum(np.asarray(l9s3b) > 0) / len(l9s3b),'l9s3smean':np.mean(l9s3s),'l9s3sposrate':sum(np.asarray(l9s3s) > 0) / len(l9s3s)}
        
        resultdf = pd.DataFrame(data=result,index=[0])
        if(resultdf['l9s3sposrate'][0] > 0.7 and resultdf['l9s3smean'][0] > 0):
            return 0.0009,0.0003,-1
        elif(resultdf['l9s3bposrate'][0] > 0.7 and resultdf['l9s3bmean'][0] > 0):
            return 0.0009,0.0003,1
        elif(resultdf['l8s3bposrate'][0] > 0.7 and resultdf['l8s3bmean'][0] > 0):
            return 0.0008,0.0003,1
        elif(resultdf['l8s3sposrate'][0] > 0.7 and resultdf['l8s3smean'][0] > 0):
            return 0.0008,0.0003,-1
        elif(resultdf['l4s2bposrate'][0] > 0.7 and resultdf['l4s2bmean'][0] > 0):
            return 0.0004,0.0002,1
        elif(resultdf['l4s2sposrate'][0] > 0.7 and resultdf['l4s2smean'][0] > 0):
            return 0.0004,0.0002,-1
        elif(resultdf['l2s1bposrate'][0] > 0.7 and resultdf['l2s1bmean'][0] > 0):
            return 0.0002,0.0001,1
        elif(resultdf['l2s1sposrate'][0] > 0.7 and resultdf['l2s1smean'][0] > 0):
            return 0.0002,0.0001,-1
        return 0,0,0
    
def get_sharpe_stra(gene,column_index_value_dict,binDict,df,RbinDict):
        tempdf = decode(gene,column_index_value_dict,binDict,df)
        tempdf = appendrbin(tempdf,RbinDict)
    
        binLists = []
        for i in range(20):
            dig = np.digitize(tempdf['r%d'%(i+1)], RbinDict[1])
            binLists.append(dig)
        binArray = np.array(binLists) - 5.5
        arraydf = pd.DataFrame(binArray)
        for i in range(14):
            arraydf['mean%dposrate'%(i+6)] = arraydf.rolling(i+6).mean().apply(pos_rate,axis=1)
            arraydf['mean%dposrate'%(i+6)] = arraydf['mean%dposrate'%(i+6)].shift(-(i+6))
            arraydf['mean%d'%(i+6)] = arraydf.rolling(i+6).mean().mean(axis=1)
            arraydf['mean%d'%(i+6)] = arraydf['mean%d'%(i+6)].shift(-(i+6))
            arraydf['sharpe%d'%(i+6)] = (arraydf.rolling(i+6).mean() / arraydf.rolling(i+6).std()).mean(axis=1)
            arraydf['sharpe%d'%(i+6)] = arraydf['sharpe%d'%(i+6)].shift(-(i+6))
            
        arraydf['max'] = arraydf[['sharpe6','sharpe7','sharpe8','sharpe9','sharpe10','sharpe11','sharpe12','sharpe13','sharpe14','sharpe15','sharpe16','sharpe17','sharpe18','sharpe19']].idxmax(axis=1)
        arraydf['min'] = arraydf[['sharpe6','sharpe7','sharpe8','sharpe9','sharpe10','sharpe11','sharpe12','sharpe13','sharpe14','sharpe15','sharpe16','sharpe17','sharpe18','sharpe19']].idxmin(axis=1)
        maxname = arraydf.iloc[0]['max']
        minname = arraydf.iloc[0]['min']
        maxn = re.findall('\d+',arraydf.iloc[0]['max'])
        minn = re.findall('\d+',arraydf.iloc[0]['min'])
        maxint = int(maxn[0])
        minint = int(minn[0])
        if(arraydf.iloc[0][maxname] > 2.0):
            return maxint
        elif(arraydf.iloc[0][minname] < -2.0):
            return -minint
        else:
            return 0
        
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    pd.options.mode.chained_assignment = None
    filedf = pd.read_csv('factsheetdf.csv',index_col='Unnamed: 0')
    filedf.dropna(inplace=True)
    
    genes = filedf.index.values.tolist()
    new_genes = []
    for x in genes:
        new_genes.append(ast.literal_eval(x))
    
    df = pd.read_csv('df.csv')
    
    RbinDict = makeRDf(df)
    bins = RbinDict[1]
    column_index_value_dict,binDict = makeDf(df)
    sharpedf = pd.DataFrame()
    for gene in tqdm(new_genes):
        tempdf = decode(gene,column_index_value_dict,binDict,df)
        tempdf = appendrbin(tempdf,RbinDict)
    
        binLists = []
        for i in range(20):
            dig = np.digitize(tempdf['r%d'%(i+1)], bins)
            binLists.append(dig)
        binArray = np.array(binLists) - 5.5
        arraydf = pd.DataFrame(binArray)
        for i in range(14):
            arraydf['mean%dposrate'%(i+6)] = arraydf.rolling(i+6).mean().apply(pos_rate,axis=1)
            arraydf['mean%dposrate'%(i+6)] = arraydf['mean%dposrate'%(i+6)].shift(-(i+6))
            arraydf['mean%d'%(i+6)] = arraydf.rolling(i+6).mean().mean(axis=1)
            arraydf['mean%d'%(i+6)] = arraydf['mean%d'%(i+6)].shift(-(i+6))
            arraydf['sharpe%d'%(i+6)] = (arraydf.rolling(i+6).mean() / arraydf.rolling(i+6).std()).mean(axis=1)
            arraydf['sharpe%d'%(i+6)] = arraydf['sharpe%d'%(i+6)].shift(-(i+6))
            
        filedf.ix[gene.__repr__(),['sharpe6','sharpe7','sharpe8','sharpe9','sharpe10','sharpe11','sharpe12','sharpe13','sharpe14','sharpe15','sharpe16','sharpe17','sharpe18','sharpe19']]  = arraydf[['sharpe6','sharpe7','sharpe8','sharpe9','sharpe10','sharpe11','sharpe12','sharpe13','sharpe14','sharpe15','sharpe16','sharpe17','sharpe18','sharpe19']].iloc[0]    
    