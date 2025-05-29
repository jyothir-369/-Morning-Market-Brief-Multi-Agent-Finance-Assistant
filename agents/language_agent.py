import logging
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, List
from dotenv import load_dotenv
import os
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LanguageAgent:
    def __init__(self):
        """
        Initialize LanguageAgent with OpenAI LLM.
        Raises:
            ValueError: If OPENAI_API_KEY is not found.
            Exception: If ChatOpenAI initialization fails.
        """
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in .env file at %s", os.path.abspath(".env"))
            raise ValueError("OPENAI_API_KEY is required in .env file")

        try:
            # Log parameters for debugging
            params = {
                "api_key": "[REDACTED]",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_retries": 2
            }
            logger.debug("Initializing ChatOpenAI with parameters: %s", params)
            self.llm = ChatOpenAI(
                api_key=api_key,
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_retries=2
            )
            logger.info("LanguageAgent initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize ChatOpenAI: %s\n%s", str(e), traceback.format_exc())
            raise

    def generate_narrative(self, query: str, market_data: Dict, retrieved_docs: List, analysis: Dict) -> str:
        """
        Generate a narrative based on query, market data, documents, and analysis.
        Args:
            query (str): User query.
            market_data (Dict): Market data dictionary.
            retrieved_docs (List): List of retrieved documents.
            analysis (Dict): Analysis dictionary.
        Returns:
            str: Generated narrative or error message.
        """
        try:
            prompt = PromptTemplate(
                input_variables=["query", "market_data", "docs", "analysis"],
                template=(
                    "Query: {query}\n"
                    "Market Data: {market_data}\n"
                    "Retrieved Documents: {docs}\n"
                    "Analysis: {analysis}\n"
                    "Provide a concise narrative answering the query, integrating the provided data."
                )
            )
            docs_text = "\n".join([doc.page_content for doc in retrieved_docs if hasattr(doc, 'page_content')])
            response = self.llm.invoke(prompt.format(
                query=query,
                market_data=str(market_data),
                docs=docs_text,
                analysis=str(analysis)
            ))
            narrative = getattr(response, 'content', str(response)).strip()
            logger.info("Generated narrative for query: %s", query)
            return narrative
        except Exception as e:
            logger.error("Language Agent error for query '%s': %s\n%s", query, str(e), traceback.format_exc())
            return f"Error generating narrative: {str(e)}"

if __name__ == "__main__":
    try:
        agent = LanguageAgent()
        test_query = "Test market brief"
        test_data = {"stock": "TSM", "price": 100}
        test_docs = [type('Doc', (), {'page_content': 'Test document'})()]
        test_analysis = {"sentiment": "neutral"}
        result = agent.generate_narrative(test_query, test_data, test_docs, test_analysis)
        print(result)
    except Exception as e:
        print(f"Test failed: {e}")