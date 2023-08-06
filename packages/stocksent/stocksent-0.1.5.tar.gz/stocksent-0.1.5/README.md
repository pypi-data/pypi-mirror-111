
# Stocksent

<a href="https://github.com/Aryagm/Stocksent" target="blank"><img align="center" src="https://img.shields.io/badge/Stocksent-100000?style=for-the-badge&logo=github&logoColor=white" /></a>

<p align="center">
<img src="https://raw.githubusercontent.com/Aryagm/Stocksent/main/logo.png" alt="logo" width="100"/>
</p>

Stocksent is a Python library for sentiment analysis of various tickers from the latest news from trusted sources. It also has options for plotting results.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install stocksent.

```bash
pip install stocksent
```
<br />
<br />

## Usage

<br />

### Get Sentiment of single stock

```python 
from stocksent import StockSent
stock = StockSent('AAPL')
sentiment_score = stock.get_sentiment()
print(sentiment_score)  # Returns a float with the sentiment score.
```

```python
0.189
```
<br />

### Get Sentiment of multiple stocks

```python
from stocksent import StockSent
stocks = StockSent(['AAPL','TSLA','GOOG'])
sentiment_score = stocks.get_sentiment(days=4) # Get the sentiment for the past 4 days.
print(sentiment_score)  # Returns a float with the sentiment score.
```

```python
0.237
```

<br />

### Get plot of sentiment scores

```python
from stocksent import StockSent
stocks = StockSent(['AAPL','TSLA','GOOG'])
sentiment_score = stocks.plot()
```
<img src="https://raw.githubusercontent.com/Aryagm/Stocksent/main/plot.png" alt="plot" width=450/>

<br />
<br />

### Get word cloud of headlines

```python
from stocksent import StockSent
stocks = StockSent(['AAPL','AMZN','GOOG','TSLA'])
sentiment_score = stocks.word_cloud(days=5) #Create a word cloud from news from the past 5 days.
```
<img src="https://raw.githubusercontent.com/Aryagm/Stocksent/main/word_cloud.png" alt="word cloud" width=450/>

<br />
<br />

## Contributing
Pull requests are welcome on [GitHub](https://github.com/Aryagm/Stocksent) !

<br />

## License
[Mozilla Public License
Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/)

<br />

## Author
**Arya Manjaramkar**

<a href="https://www.linkedin.com/in/arya-manjaramkar" target="blank"><img align="center" src="https://img.shields.io/badge/Arya Manjaramkar-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>  &nbsp;&nbsp;&nbsp;       <a href="https://www.github.com/Aryagm" target="blank"><img align="center" src="https://img.shields.io/badge/Aryagm-100000?style=for-the-badge&logo=github&logoColor=white" /></a>