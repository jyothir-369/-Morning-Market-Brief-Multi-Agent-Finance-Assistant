import logging
from typing import List, Dict, Optional
from data_ingestion.api import fetch_stock_data, fetch_historical_data

# Configure logging to match orchestrator/main.py, language_agent.py, scraping_agent.py, and analysis_agent.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIAgent:
    def __init__(self, tickers: Optional[List[str]] = None):
        """
        Initialize API Agent with optional tickers for Asia tech stocks.
        Args:
            tickers (List[str], optional): List of ticker symbols (e.g., ['TSM', '005930.KS']). Defaults to ["TSM", "005930.KS"] if None.
        """
        self.tickers = tickers if tickers is not None else ["TSM", "005930.KS"]
        logger.info("APIAgent initialized with tickers: %s", self.tickers)

    def get_market_data(self, tickers: Optional[List[str]] = None) -> Dict:
        """
        Fetch real-time and historical market data for the specified or default tickers.
        Args:
            tickers (List[str], optional): List of ticker symbols to fetch data for. If None, uses self.tickers.
        Returns:
            Dict: Combined real-time and historical data, or error message.
        """
        try:
            target_tickers = tickers if tickers is not None else self.tickers
            if not target_tickers:
                logger.error("No tickers provided for market data fetch")
                raise ValueError("No tickers provided")

            logger.info("Fetching market data for tickers: %s", target_tickers)
            realtime_data = fetch_stock_data(target_tickers)  # Fixed typo: fetch_realtime_data -> fetch_stock_data
            historical_data = fetch_historical_data(target_tickers, days=30)
            
            result = {
                "realtime": realtime_data or {},
                "historical": historical_data or {}
            }
            logger.info("Successfully fetched market data: %s", result)
            return result
        except Exception as e:
            logger.error("APIAgent error: %s", str(e), exc_info=True)
            return {
                "realtime": {},
                "historical": {},
                "error": f"Failed to fetch market data: {str(e)}"
            }

if __name__ == "__main__":
    try:
        agent = APIAgent()
        data = agent.get_market_data()
        logger.info("API Agent Output: %s", data)
    except Exception as e:
        logger.error("Test failed: %s", str(e), exc_info=True)