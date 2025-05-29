import logging
from typing import Dict, Optional

# Configure logging to match orchestrator/main.py, language_agent.py, and scraping_agent.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnalysisAgent:
    def __init__(self, portfolio: Optional[Dict[str, float]] = None):
        """
        Initialize Analysis Agent with portfolio data.
        Args:
            portfolio (Dict[str, float], optional): Portfolio allocations (e.g., {"TSM": 0.12, "005930.KS": 0.10}).
        """
        self.portfolio = portfolio or {"TSM": 0.12, "005930.KS": 0.10}  # Mock data: 22% of AUM
        self.yesterday_portfolio = {"TSM": 0.10, "005930.KS": 0.08}  # Mock data: 18% of AUM
        logger.info("AnalysisAgent initialized with portfolio: %s", self.portfolio)

    def analyze_risk_exposure(self, market_data: Dict, earnings_data: Dict) -> Dict:
        """
        Analyze risk exposure and earnings surprises.
        Args:
            market_data (Dict): Real-time and historical market data.
            earnings_data (Dict): Scraped earnings data.
        Returns:
            Dict: Analysis results including allocation and earnings summary.
        """
        try:
            # Validate inputs
            if not isinstance(market_data, dict):
                logger.error("Invalid market_data: expected dict, got %s", type(market_data))
                raise ValueError("market_data must be a dictionary")
            if not isinstance(earnings_data, dict):
                logger.error("Invalid earnings_data: expected dict, got %s", type(earnings_data))
                raise ValueError("earnings_data must be a dictionary")

            # Calculate portfolio allocations
            current_allocation = sum(self.portfolio.values()) * 100
            yesterday_allocation = sum(self.yesterday_portfolio.values()) * 100

            # Summarize earnings data
            earnings_summary = {
                ticker: earnings_data.get(ticker, "No earnings data")
                for ticker in self.portfolio.keys()
            }

            # Example: Incorporate market_data (e.g., price changes)
            price_changes = {}
            for ticker in self.portfolio.keys():
                if ticker in market_data.get("realtime", {}):
                    current_price = market_data["realtime"].get(ticker, {}).get("price", 0)
                    price_changes[ticker] = f"Current price: {current_price}"

            analysis = {
                "current_allocation": f"{current_allocation:.0f}%",
                "yesterday_allocation": f"{yesterday_allocation:.0f}%",
                "earnings_summary": earnings_summary,
                "price_changes": price_changes
            }
            logger.info("Risk exposure analysis completed: %s", analysis)
            return analysis
        except Exception as e:
            logger.error("AnalysisAgent error: %s", str(e), exc_info=True)
            return {
                "current_allocation": "0%",
                "yesterday_allocation": "0%",
                "earnings_summary": {},
                "price_changes": {}
            }

if __name__ == "__main__":
    try:
        agent = AnalysisAgent()
        mock_market_data = {"realtime": {"TSM": {"price": 150}, "005930.KS": {"price": 60000}}}
        mock_earnings_data = {"TSM": "beat estimates by 4%", "005930.KS": "missed estimates by 2%"}
        analysis = agent.analyze_risk_exposure(mock_market_data, mock_earnings_data)
        logger.info("Analysis Agent Output: %s", analysis)
    except Exception as e:
        logger.error("Test failed: %s", str(e), exc_info=True)