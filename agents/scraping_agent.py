from data_ingestion.scraper import scrape_earnings_data, clean_earnings_data

class ScrapingAgent:
    def __init__(self, tickers=["TSM", "005930.KS"]):
        """
        Initialize Scraping Agent with default tickers.
        Args:
            tickers (list): List of ticker symbols.
        """
        self.tickers = tickers

    def get_earnings_data(self):
        """
        Scrape and clean earnings data for tickers.
        Returns:
            dict: Cleaned earnings data.
        """
        try:
            raw_data = scrape_earnings_data(self.tickers)
            cleaned_data = clean_earnings_data(raw_data)
            return cleaned_data
        except Exception as e:
            print(f"Scraping Agent error: {e}")
            return {ticker: "No earnings data available" for ticker in self.tickers}

if __name__ == "__main__":
    agent = ScrapingAgent()
    data = agent.get_earnings_data()
    print("Scraping Agent Output:", data)