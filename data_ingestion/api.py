import yfinance as yf
import time
from requests.exceptions import HTTPError

def fetch_stock_data(ticker, retries=3, delay=5):
    # Mock data for real-time data
    mock_data = {
        "TSM": {"price": 150.25, "volume": 12000000, "market_cap": 780000000000},
        "005930.KS": {"price": 58000, "volume": 15000000, "market_cap": 390000000000000}
    }
    
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("regularMarketPrice", 0)
            volume = info.get("regularMarketVolume", 0)
            market_cap = info.get("marketCap", 0)
            return {
                "price": price,
                "volume": volume,
                "market_cap": market_cap
            }
        except HTTPError as e:
            if "429" in str(e):
                print(f"Rate limit hit for {ticker}. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            else:
                print(f"Error fetching data for {ticker}: {e}")
                return mock_data.get(ticker, {"price": 0, "volume": 0, "market_cap": 0})
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return mock_data.get(ticker, {"price": 0, "volume": 0, "market_cap": 0})
    print(f"Failed to fetch data for {ticker} after {retries} attempts. Using mock data.")
    return mock_data.get(ticker, {"price": 0, "volume": 0, "market_cap": 0})

def fetch_historical_data(ticker, period="1mo", retries=3, delay=5):
    # Mock historical data
    mock_historical = {
        "TSM": {
            "Close": {"2025-05-01": 145.0, "2025-05-28": 150.25},
            "Volume": {"2025-05-01": 11000000, "2025-05-28": 12000000}
        },
        "005930.KS": {
            "Close": {"2025-05-01": 57000, "2025-05-28": 58000},
            "Volume": {"2025-05-01": 14000000, "2025-05-28": 15000000}
        }
    }
    
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return {
                "Close": hist["Close"].to_dict(),
                "Volume": hist["Volume"].to_dict()
            }
        except HTTPError as e:
            if "429" in str(e):
                print(f"Rate limit hit for historical data of {ticker}. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            else:
                print(f"Failed to get historical data for {ticker}: {e}")
                return mock_historical.get(ticker, {"Close": {}, "Volume": {}})
        except Exception as e:
            print(f"Failed to get historical data for {ticker}: {e}")
            return mock_historical.get(ticker, {"Close": {}, "Volume": {}})
    print(f"Failed to fetch historical data for {ticker} after {retries} attempts. Using mock data.")
    return mock_historical.get(ticker, {"Close": {}, "Volume": {}})

if __name__ == "__main__":
    tickers = ["TSM", "005930.KS"]
    real_time_data = {ticker: fetch_stock_data(ticker) for ticker in tickers}
    historical_data = {ticker: fetch_historical_data(ticker) for ticker in tickers}
    print("Real-time Data:", real_time_data)
    print("Historical Data:", historical_data)