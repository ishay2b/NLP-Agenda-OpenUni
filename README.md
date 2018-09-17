**Conservative/Liberal agenda prediction using NLP**

We parsed few political web sites with known Conservative/Liberal articles from the opinions section to see if we can predict the author's agenda by using NLP.

See src/ notebooks for more info.

**Data Preparation**
 
Since we do not own the data, It is up to the user to place text files under the data/liberal/site-name and data/conservative/site-name.

**IPython Notebooks**

See [initial notebook](src/DataAnalysis.ipynb) for words distribution differences between liberal and conservative websites. 

Check this [notebook](src/SVM_vs_NN_vs_regression.ipynb) with naive baseline predictors such as SVM, Nearest-To-Mean-Vector and Linear regression.

See this [lstm notebook](src/lstm_2.ipynb) for running/viewing the LSTM output with accuracy of 74%.

Lastly this [notebook](src/lstm_1.ipynb) explains what happens when you same web sites appear both in test and train results.


