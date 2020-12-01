import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

def create_matching_sets(stockIndex, twitterSentiments):
    """
    Function to be able to create a DataFrame having the BSI and twitterSentiments
    :param stockIndex: DataFrame containing BSI and the dates
    :param twitterSentiments: DataFrame containing sentiment average for the days tweets
    :return: matchingSet; dictionary with stock index and sentiment average for the day if applicable
    """
    matchingSet = {'Date': [], 'BSI': [], 'Sentiment': []}
    for eachRow in range(len(stockIndex)):
        stockIndexDate = stockIndex.iloc[eachRow]['Date']
        for differentRow in range(len(twitterSentiments)):
            twitterSentimentDate = twitterSentiments.iloc[differentRow]['Date']
            if stockIndexDate == twitterSentimentDate:
               matchingSet['Date'].append(stockIndexDate)
               matchingSet['BSI'].append(stockIndex.iloc[eachRow]['BSI'])
               matchingSet['Sentiment'].append(twitterSentiments.iloc[differentRow]['Sentiment Score'])
    return matchingSet

def scale_sentiment(sentiment):
    """

    :param sentiment: sentiment score
    :return: scaledScore, sentiment score multiplied by 1000 so that it fits better on the graph
    """
    sentiment = float(sentiment)
    scaledScore = sentiment*100
    return scaledScore
def create_subplot(dataFrame):
    """
    Function to create subplots of sentiment and stock index with dates
    :param dataFrame: dataFrame to extract the x and y from
    :return: void, subplot with sentiment and stock index plot side by side
    """
    x = dataFrame[0:]['Date']
    y1 = dataFrame[0:]['BSI']
    y2 = dataFrame[0:]['Sentiment']
    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.scatter(x, y1)
    ax1.set_title('Bhutan Stock Index')
    ax2.scatter(x, y2)
    ax2.set_title('Twitter Sentiment Scores')
    fig.show()
def create_plot(dataFrame):
    """

    :param dataFrame: dataFrame to extract the x and y from.
    :return: void, just draws a plot using matplotlib
    """
    y = np.array(dataFrame[0:]['BSI'])
    x = np.array(dataFrame[0:]['Sentiment']).reshape((-1, 1))
    x1 = np.array(dataFrame[0:]['Sentiment'])

    mymodel = np.poly1d(np.polyfit(x1, y, 3))
    myline = np.linspace(0,37,100)
    rSq1 = r2_score(y, mymodel(x))
    print(rSq1)

    # change x to contain additional column with values = x^2
    transformer = PolynomialFeatures(degree=2, include_bias=False)
    x_ = transformer.fit_transform(x)
    model = LinearRegression().fit(x_,y)
    rSq = model.score(x_,y)
    intercept = model.intercept_
    slope = model.coef_
    print('intercept :', intercept,'\nRSquared:',rSq,'\nSlope:', slope)
    plt.scatter(x, y)
    plt.plot(myline, mymodel(myline))
    # plt.plot(x,slope[0]*x+intercept)
    plt.show()

stockIndexes = pd.read_csv("./stockIndexClean.csv")
twitterSentiments = pd.read_csv("./tweetSentiments.csv")
# stocksSentimentsDF = pd.DataFrame(create_matching_sets(stockIndexes, twitterSentiments))
stocksSentimentsDF = pd.read_csv("./stocks&sentiments.csv")
for eachRow in range(len(stocksSentimentsDF)):
    stocksSentimentsDF.at[eachRow, 'Sentiment'] = scale_sentiment(stocksSentimentsDF.iloc[eachRow]['Sentiment'])
create_plot(stocksSentimentsDF)
