import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_earnings_data(tickers, base_url="https://finance.yahoo.com/quote"):
    """
    Scrape earnings data for given tickers from a financial news site.
    Args:
        tickers (list): List of ticker symbols (e.g., ['TSM', '005930.KS']).
        base_url (str): Base URL for scraping (e.g., Yahoo Finance).
    Returns:
        dict: Earnings data with ticker as key and summary as value.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    earnings_data = {}
    
    for ticker in tickers:
        try:
            # Construct URL (mock example, adjust for actual source)
            url = f"{base_url}/{ticker}/news"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mock parsing: Look for headlines with "earnings"
            headlines = soup.find_all('h3', class_=re.compile('.*news.*'))
            for headline in headlines:
                text = headline.get_text().lower()
                if "earnings" in text:
                    earnings_data[ticker] = text
                    break
            else:
                earnings_data[ticker] = f"No recent earnings news for {ticker}"
        except Exception as e:
            print(f"Error scraping data for {ticker}: {e}")
            earnings_data[ticker] = f"Failed to scrape earnings for {ticker}"
    
    return earnings_data

def clean_earnings_data(raw_data):
    """
    Clean scraped earnings data for RAG.
    Args:
        raw_data (dict): Raw earnings data from scraper.
    Returns:
        dict: Cleaned earnings data.
    """
    cleaned = {}
    for ticker, text in raw_data.items():
        # Remove unwanted characters and normalize
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        cleaned[ticker] = cleaned_text
    return cleaned

if __name__ == "__main__":
    # Example usage
    tickers = ["TSM", "005930.KS"]
    raw_data = scrape_earnings_data(tickers)
    cleaned_data = clean_earnings_data(raw_data)
    print("Scraped Earnings Data:", cleaned_data)