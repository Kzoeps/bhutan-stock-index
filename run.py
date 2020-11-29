import pandas as pd
import matplotlib.pyplot as plt
stockIndexes = pd.read_csv("./stockIndexClean.csv")
twitterSentiments = pd.read_csv("./tweetSentiments.csv")


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
def create_plot(dataFrame):
    """

    :param dataFrame: dataFrame to extract the X and Y from.
    :return: void, just draws a plot using matplotlib
    """
    X = dataFrame[0:]['Date']
    Y1 = dataFrame[0:]['BSI']
    Y2 = dataFrame[0:]['Sentiment']
    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(X,Y1)
    ax1.set_title('BSI')
    ax2.plot(X, Y2)
    ax2.set_title('Sentiment Scores')
    fig.show()
# stocksSentimentsDF = pd.DataFrame(create_matching_sets(stockIndexes, twitterSentiments))
stocksSentimentsDF = pd.read_csv("./stocks&sentiments.csv")
for eachRow in range(len(stocksSentimentsDF)):
    stocksSentimentsDF.at[eachRow, 'Sentiment'] = scale_sentiment(stocksSentimentsDF.iloc[eachRow]['Sentiment'])
create_plot(stocksSentimentsDF)