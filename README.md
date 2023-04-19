# sentiment-analysis

Utilities that mine Stocktwits.com for a list of stocks twits and label twits into Bearish or Bullish. 

Stocktwits api provides a class that allows for listening to individual tickers. 

The classification files take in labeled twits, and classify unlabeled ones into bullish or bearish. Two distinct models are compared and the best one used (i.e. Naive Bayes vs. Logistic Reg. Classifier). 

## Output


dates	ticker	Bearish	Bullish
12/29/2021	ADSK	2	1
12/30/2021	ADSK	3	1
12/31/2021	ADSK	1	0
1/1/2022	ADSK	1	1
1/3/2022	ADSK	6	3
1/4/2022	ADSK	1	0
1/5/2022	ADSK	0	1
1/6/2022	ADSK	7	2
1/7/2022	ADSK	1	1
1/8/2022	ADSK	1	1
1/9/2022	ADSK	2	1

