""""
Author:     Karol Planadeball
Assignment: Stock Market Data Analysis
Due Date:   2/10/2025
Version:    1.0
"""
import requests
import json
from datetime import date, timedelta

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
        historical_data = response.json()
        return historical_data
    except Exception as error:
        print(f"Exception occurred {error}")
        return {}

"""Data Download Section"""
data = download_data("aapl")
file_path = "stocks.json"

#Write information to JSON file to verify functionality
with open(file_path, "w") as file:
    json.dump(data, file)

print(f"JSON data written to {file_path}")