""""
Author:     Karol Planadeball
Assignment: Stock Market Data Analysis
Due Date:   2/10/2025
Version:    1.0
AI Usage Disclaimers: Copilot and ChatGPT were heavily used to explore implementations of dictionary methods as well
as give explanations to many of the lines of code provided. Sources such as GeeksForGeeks and W3 schools also helped
with the understanding of how to handle API calls and resulting information. This code was also created with the help
of Grant Bowers. We worked on developing the functions together.
"""
from datetime import date
import json
import requests
import sys

def download_data(ticker: str) -> dict:
    """
    Purpose:
        Downloads data from Stock Market API, specifically NASDAQ.
    Args:
        ticker(str): The stock ticker.
    Returns:
        A dictionary containing the stock data starting from today 5 years ago up until today.
    """
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    try:
        print(base_url + path)
        #We must define the user agent so that the request is able to go through
        response = requests.get(base_url + path, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        historical_data = response.json()
        return historical_data
    except Exception as error:
        print(f"Exception occurred {error}")
        return {}

def data_processing(stocks: dict) -> dict:
    """
    Purpose:
        Processes data from downloaded stocks json. Finds the min, max, avg, and median of the closing prices.
    Args:
        stocks(dict): A dictionary containing the stocks' data.
    Returns:
        dict: A dictionary containing the min, max, avg, and median of the closing prices.
    """
    try:
        #Create a list only containing the rows from the dictionary (i.e. information for each day)
        modified_stocks = list(stocks["data"]["tradesTable"]["rows"])
        #List to store the close values for future operations.
        close_values = []
    except Exception as error:
        print(f"Exception occurred {error}")
        return {}

    for stock in modified_stocks:
        close_price = float(stock["close"].replace('$',''))
        close_values.append(close_price)

    #Create the dictionary to return with the keys being set to the points of interest (min, max, etc.) and the values
    # are the values corresponding to those points
    symbol = stocks["data"]["symbol"]
    max_close = max(close_values)
    min_close = min(close_values)
    avg_close = sum(close_values) / len(close_values)
    median_close = sorted(close_values)[len(close_values) // 2]
    return {"ticker": symbol, "max_close": max_close, "min_close": min_close, "avg_close": avg_close, "median_close": median_close}

if __name__ == "__main__":
    """Data Download Section"""
    tickers = []
    #Read in arguments from user
    for ticker in sys.argv[1:]:
        tickers.append(ticker)
    filtered_tickers = []

    #File Paths
    data_path = "raw_data.json"
    filtered_path = "stocks.json"

    #Run the code using the tickers in the list. Final result is placed in the stocks.json
    for ticker in tickers:
        data = download_data(ticker)
        # Write information to JSON file to verify functionality
        with open(data_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"JSON data written to {data_path}")
        filtered_tickers.append(data_processing(data))
        with open(filtered_path, "w") as file:
            json.dump(filtered_tickers, file, indent=4)