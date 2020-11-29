# bhutan-stock-index

Just trying to see if there is any relation between the stock index of Bhutan(Bhutan Stock Index or BSI) and sentiment scores of tweets from Bhutan.
Used `TextBlob` to analyse the sentiment of the tweets and `Matplotlib` and `pandas` for data visualization.

## Installation
first install all the packages required.
```bash
  pip install -r requirements.txt
```

## Usage
first run `clean_data.py` then run `run.py`. It will output the plot of Bhutan Stock Index and twitter sentiments on the same plot.

## Contributing
Feel free to make pull requests and play around. The data is in the root directory with the BSI data as: `BSI.xlsx` and the twitter data in the `twitter_data` directory.

## License
[MIT](https://github.com/Kzoeps/bhutan-stock-index/blob/main/LICENSE)
