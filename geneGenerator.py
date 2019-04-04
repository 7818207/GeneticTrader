# -*- coding: utf-8 -*-
from random import randint

class geneGenerator:
    
    def __init__(self,maxBlocks,maxLookback,bins):
        self.maxBlocks = maxBlocks
        self.maxLookback = maxLookback
        self.bins = bins
        
    
    #Now only generating fixed length gene
    def generateOne(self):
        gene = []
        for i in range(maxBlocks):
            maxLookback = self.maxLookback
            gene.append(randint(1,maxLookback))
            gene.append(randint(1,self.bins))
        return gene
    
    def generateMany(self, no):
        genes = []
        
        for i in range(no):
            gene = []
            for i in range(self.maxBlocks):
                gene.append(randint(1,self.maxLookback))
                gene.append(randint(1,self.bins))
            genes.append(gene)
                
        return genes