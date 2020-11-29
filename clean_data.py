import pandas as pd
import datetime
import os
from textblob import TextBlob

stockIndex = pd.read_excel("./BSIFinal.xlsx")
stockIndexDF = pd.DataFrame(stockIndex)
stockIndexDF = stockIndexDF.drop(columns='Id')
dateObj = datetime.datetime.strptime('1/30/2020', '%m/%d/%Y')
dateTruncated = datetime.date(dateObj.year, dateObj.month, dateObj.day)
for eachRow in range(len(stockIndexDF)):
    date = stockIndexDF.iloc[eachRow][2]
    # convert to an actual datetime object
    dateObj = datetime.datetime.strptime(date, '%m/%d/%Y')
    # remove time stamp
    onlyDate = datetime.date(dateObj.year, dateObj.month, dateObj.day)
    # assign the new date obj as the date in dataframe.
    stockIndexDF.at[eachRow, 'Date'] = onlyDate
stockIndexDF = stockIndexDF.sort_values(by='Date')

cleanData = {'Date': {}, 'BSI': {}}
for eachRow in range(len(stockIndexDF)):
    date = stockIndexDF.iloc[eachRow][2].strftime('%m/%d/%Y')
    index = stockIndexDF.iloc[eachRow][0]
    if date in cleanData['Date']:
        cleanData['Date'][date] += 1
        cleanData['BSI'][date] += index
    else:
        cleanData['Date'][date] = 1
        cleanData['BSI'][date] = index
# dictionary for dataframe and pyplot
stockIndex = {'Date': [], 'BSI': []}
for key in cleanData['BSI']:
    stockIndex['Date'].append(key)
    index = cleanData['BSI'][key]
    indexAverage = index / cleanData['Date'][key]
    stockIndex['BSI'].append(indexAverage)
stockIndexDF = pd.DataFrame(stockIndex)
stockIndexDF.to_csv("stockIndexClean.csv")

def calculate_sentiment(text):
    """
    :param text: text to calulate sentiment of
    :return: sentimentScore,sentiment score polarity.
    """
    sentiment = TextBlob(text)
    return sentiment.polarity


def date_truncate(date):
    """
    function to convert a string date to date and to remove time stamp
    :param date: string date
    :return: onlyDate (string date without timestamp)
    """
    try:
        dateObj = datetime.datetime.strptime(date, '%m/%d/%y %H:%M')
    except ValueError:
        dateObj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    onlyDate = datetime.date(dateObj.year, dateObj.month, dateObj.day)
    return onlyDate.strftime('%m/%d/%Y')


def tweet_sort(tweetFile):
    """

    :param tweetFile: the csv file containing the tweets
    :return: sortedTweets, dictionary containing dates and sentiment scores.
    """
    tweetFileData = pd.read_csv(tweetFile, names=["Date", "Tweet", "User", "Tags", "NA", "Location"])
    tweetFileDF = pd.DataFrame(tweetFileData)
    sortedTweets = {'Date': {}, 'Sentiment Score': {}}
    for eachRow in range(len(tweetFileDF)):
        date = str(tweetFileDF.iloc[eachRow][0])
        tweet = str(tweetFileDF.iloc[eachRow][1])
        if tweet != 'nan' and date != 'nan':
            date = date_truncate(date)
            if date not in sortedTweets['Sentiment Score']:
                sortedTweets['Sentiment Score'][date] = calculate_sentiment(tweet)
                sortedTweets['Date'][date] = 1
            else:
                sortedTweets['Sentiment Score'][date] += calculate_sentiment(tweet)
                sortedTweets['Date'][date] += 1
    return sortedTweets

def create_tweet_DF():
    """
    loop through all of the files in twitter_data and analyse sentiments for each tweet.
    :return: pyPlotDF, a DataFrame with date and average sentiment score for that date.
    """
    tweetsDF = {'Date': {}, 'Sentiment Score': {}}
    pyPlotDF = {'Date': [], 'Sentiment Score': []}
#     traverse through all files in twitter_data and analyze them
    directory = os.fsencode("./twitter_data")
    for file in os.listdir(directory):
        fileName = os.fsdecode(file)
        if fileName.endswith(".csv"):
            analysedTweetScores = tweet_sort("./twitter_data/"+str(fileName))
            # add up all the sentiment scores since dates might be scattered all over
            for key in analysedTweetScores['Date']:
                if key not in tweetsDF['Date']:
                    tweetsDF['Date'][key] = analysedTweetScores['Date'][key]
                    tweetsDF['Sentiment Score'][key] = analysedTweetScores['Sentiment Score'][key]
                else:
                    tweetsDF['Date'][key] += analysedTweetScores['Date'][key]
                    tweetsDF['Sentiment Score'][key] += analysedTweetScores['Sentiment Score'][key]
        else:
            continue
    for key in tweetsDF['Date']:
        averageSentimentScore = tweetsDF['Sentiment Score'][key] / tweetsDF['Date'][key]
        pyPlotDF['Date'].append(key)
        pyPlotDF['Sentiment Score'].append(averageSentimentScore)

    pyPlotDF = pd.DataFrame(pyPlotDF)
    return pyPlotDF

tweetSentiments = create_tweet_DF()
tweetSentiments.to_csv("tweetSentiments.csv")
print(tweetSentiments)