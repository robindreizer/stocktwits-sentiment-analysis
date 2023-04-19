# sentiment-analysis

Utilities that mine Stocktwits.com for a list of stocks twits and label twits into Bearish or Bullish. 

Stocktwits api provides a class that allows for listening to individual tickers. 

The classification files take in labeled twits, and classify unlabeled ones into bullish or bearish. Two distinct models are compared and the best one used (i.e. Naive Bayes vs. Logistic Reg. Classifier). 


## Output

A dataframe indexed on date which contains list of tickers and number of bullish and bearish twits for each day. 
See plotted example of ADSK below. 

![image](https://user-images.githubusercontent.com/60831947/232955738-d5e1fcbb-2308-4196-9bbf-e0605693355c.png)
