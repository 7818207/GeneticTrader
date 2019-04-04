# GeneticTrader
genetic algorithm for forex high frequency trading

# HowItWorks - General Ideas
Random hypothetical price movement is generated in the format [duration,pricechange(bin)] egg. [5,10,3,2] means for the past 5 days the price change falls in bin 10, and for 3 days ahead of the past 5 days, the price change falls in bin 2


Below is an example of what 100 randomly generated genes looks like:

============================Codes for drawing the below example===========
```python
import geneGenerator

import dnaengine

#Here 5 means totaly number of [duration, price_change] pairs, we give it 5 pairs
#10 means maximum lookback period for each block
#20 means bins for each lookback period
generator = geneGenerator.geneGenerator(5,10,20)

genes = generator.generateMany(100)

engine = dnaengine.Engine()

df = pd.read_csv('df.csv')

engine.makeDf(df)

engine.draw100Dna(genes)
```
![alt text](https://github.com/7818207/GeneticTrader/blob/master/gene_example.png?raw=true)


# Monte-Carlo
Every hypothetical price movement is then tested for best stop-limit strategy using monte-carlo.
