# IDP-Project


This repository consists of the codebase for *Assessment of User Activity for the Indication of Price Movements in Capital Markets* project. The project is a part of Technical University of Munich's Master of Computer Science program's Interdisciplinary Project which is 16 ECTS credited course. The project has been completed with collaboration of Newgate (https://newgate.de/)

## Code Structure

*data connectors* and *data generators* folders include the python files and jupyter notebook files which used to retrieve data and generate a data model for statistical analysis. First months of the IDP, only correlation analysis studied but later on more well coordinated has been done. First studies of these correlation analysis studies is under *correlation analysis* folder. Under *feature analysis* folder all the statistical analysis were implemented. Lastly, under *trading strategies* simple baseline and machine learning based strategies were implemented.

## Data Visualization

<center><img src="/images/googletrend-btc.png" width="500"></center>



## Statistical Analysis 

- In each analysis different settings of window size yield a better result, it is hard to say something about a window size selection but overall it has observed that in Pearson Correlation Analysis and Granger Causality Test Analysis higher the window sizes better the score. Also, due to the nature of particular analysis, window sizes cannot be selected same for each analysis.
- In terms of lag selection, it can be said that overall best results usually occurred in smaller lags which means that the closer the user metric data to price data better the pattern match. Still, since there were some varieties in Granger Causality Test Analysis and Mutual Information Analysis, higher lags are promising area to study on. The pattern match with higher lags can be interpreted as using the user metric data to predict price data or in another words there is a strong causal effect.
- Data transformation were useful that in each analysis various transformations were more successful than the others; log transformation in Pearson Correlation Analysis, Difference Ratio in Granger Causality Analysis and Simple Moving Average of 21 days in Mutual Information Analysis.
- Best result in each analysis were different; TrendsBinance in Pearson Correlation Analysis, TrendsBitcoin in Granger Causality Test Analysis and TrendsCoinbase in Mutual Information Analysis. This fact can be interpreted as Wikipedia Pageview user metric data was not useful as Google Trends. Also, having a success on different keywords such as currency name and also exchange name, with more varied keywords more experiments could give promising results.

## Discussion

### Challenges

- Literature Review: In the literature, there is a high influence of econometric concepts which made the research more challenging due to unfamiliarity
- Data Collection: Numerous failures happened during data collection from Google Trends API.
- Data Generation: Data generation for various combinations of time series was computationally exhaustive.
- Statistical Analysis: Interpretation of each analysis was challenging.
- Machine Learning: Due to the nature of the ensemble models, debugging the models was challenging.

### Causal Analysis
From the statistical analysis, it is observed that there is a potential causal relationship between user metrics (specifically Google Trends). Considering the bidirectional causality, it is hard to evaluate a true causality and do further analysis on top of causal analysis. But, as Kristoufek says in the following paragraph of the previous quote: "Specifically, we find that while the prices are high (above trend), the increasing interest pushes the prices further atop. From the opposite side, if the prices are below their trend, the growing interest pushes the prices even deeper. This forms an environment suitable for a quite frequent emergence of a bubble behavior which indeed has been observed for the BitCoin currency." [https://www.nature.com/articles/srep03415] - with further research considering the bubble behaviour better causal relationship can be built.

### Trading Strategies with Machine Learning
- After running more simulations it is observed that the models do not success significantly better than simple ’Buy and Hold’ strategy. Possible reasons thought; data model needs to be further analyzed - with better data model better results can be achieved.
- Using advanced models like ensemble models caused overfitting mostly, making the models simpler then resulted low accuracy in both training and test sets.
- Overall,with conducting more research on ’ML in Trading’ better results can be achieved.

