import pandas as pd

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

print(create_matching_sets(stockIndexes, twitterSentiments))