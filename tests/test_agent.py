import pytest
from unittest.mock import patch
from agents.api_agent import APIAgent
from agents.scraping_agent import ScrapingAgent
from agents.retriever_agent import RetrieverAgent
from agents.analysis_agent import AnalysisAgent
from agents.language_agent import LanguageAgent
from agents.voice_agent import VoiceAgent
from langchain.docstore.document import Document

# Mock data for tests
mock_market_data = {
    "realtime": {"TSM": {"price": 150, "volume": 1000000, "market_cap": 500000000}},
    "historical": {"TSM": {"Close": {"2025-05-01": 148}}}
}
mock_earnings_data = {"TSM": "beat estimates by 4%"}
mock_documents = [Document(page_content="TSMC beat earnings by 4%", metadata={"source": "earnings"})]

@patch("data_ingestion.api.fetch_stock_data")
@patch("data_ingestion.api.fetch_historical_data")
def test_api_agent(mock_historical, mock_realtime):
    mock_realtime.return_value = mock_market_data["realtime"]
    mock_historical.return_value = mock_market_data["historical"]
    agent = APIAgent(tickers=["TSM"])
    result = agent.get_market_data(tickers=["TSM"])
    assert result["realtime"]["TSM"]["price"] == 150
    assert result["historical"]["TSM"]["Close"]["2025-05-01"] == 148

@patch("data_ingestion.api.fetch_stock_data")
@patch("data_ingestion.api.fetch_historical_data")
def test_api_agent_error(mock_historical, mock_realtime):
    mock_realtime.side_effect = Exception("API error")
    agent = APIAgent(tickers=["TSM"])
    result = agent.get_market_data(tickers=["TSM"])
    assert result["realtime"] == {}
    assert result["historical"] == {}
    assert "error" in result

@patch("data_ingestion.scraper.scrape_earnings_data")
@patch("data_ingestion.scraper.clean_earnings_data")
def test_scraping_agent(mock_clean, mock_scrape):
    mock_scrape.return_value = {"TSM": "raw data: beat estimates"}
    mock_clean.return_value = mock_earnings_data
    agent = ScrapingAgent(tickers=["TSM"])
    result = agent.get_earnings_data(tickers=["TSM"])
    assert result["TSM"] == "beat estimates by 4%"

@patch("data_ingestion.scraper.scrape_earnings_data")
@patch("data_ingestion.scraper.clean_earnings_data")
def test_scraping_agent_error(mock_clean, mock_scrape):
    mock_scrape.side_effect = Exception("Scraping error")
    agent = ScrapingAgent(tickers=["TSM"])
    result = agent.get_earnings_data(tickers=["TSM"])
    assert result["TSM"].startswith("No earnings data available")

@patch("data_ingestion.document_loader.load_documents")
@patch("agents.retriever_agent.process_documents")
@patch("langchain.vectorstores.FAISS.from_documents")
def test_retriever_agent(mock_faiss, mock_process, mock_load):
    mock_load.return_value = mock_documents
    mock_process.return_value = mock_documents
    mock_faiss.return_value.similarity_search_with_score.return_value = [(mock_documents[0], 0.9)]
    agent = RetrieverAgent()
    result = agent.retrieve("earnings surprises", k=1)
    assert len(result) == 1
    assert result[0][0].page_content == "TSMC beat earnings by 4%"
    assert result[0][1] == 0.9

@patch("data_ingestion.document_loader.load_documents")
@patch("agents.retriever_agent.process_documents")
@patch("langchain.vectorstores.FAISS.from_documents")
def test_retriever_agent_empty(mock_faiss, mock_process, mock_load):
    mock_load.return_value = []
    mock_process.return_value = []
    mock_faiss.return_value.similarity_search_with_score.return_value = []
    agent = RetrieverAgent()
    result = agent.retrieve("earnings surprises", k=1)
    assert len(result) == 0

def test_analysis_agent():
    agent = AnalysisAgent(portfolio={"TSM": 0.12})
    result = agent.analyze_risk_exposure(mock_market_data, mock_earnings_data)
    assert result["current_allocation"] == "12%"
    assert result["yesterday_allocation"] == "18%"
    assert result["earnings_summary"]["TSM"] == "beat estimates by 4%"
    assert "price_changes" in result

def test_analysis_agent_error():
    agent = AnalysisAgent(portfolio={"TSM": 0.12})
    result = agent.analyze_risk_exposure("invalid_data", mock_earnings_data)
    assert result["current_allocation"] == "0%"
    assert result["yesterday_allocation"] == "0%"
    assert result["earnings_summary"] == {}
    assert result["price_changes"] == {}

@patch("langchain_openai.ChatOpenAI")
def test_language_agent(mock_llm):
    mock_response = type("Response", (), {"content": "Mocked narrative: allocation 12%, earnings beat."})()
    mock_llm.return_value.invoke.return_value = mock_response
    agent = LanguageAgent()
    query = "What's our risk exposure?"
    market_data = mock_market_data
    retrieved_docs = mock_documents
    analysis = {
        "current_allocation": "12%",
        "yesterday_allocation": "18%",
        "earnings_summary": mock_earnings_data
    }
    result = agent.generate_narrative(query, market_data, retrieved_docs, analysis)
    assert "Mocked narrative" in result

@patch("langchain_openai.ChatOpenAI")
def test_language_agent_error(mock_llm):
    mock_llm.return_value.invoke.side_effect = Exception("LLM error")
    agent = LanguageAgent()
    query = "What's our risk exposure?"
    result = agent.generate_narrative(query, mock_market_data, mock_documents, {})
    assert result.startswith("Error generating narrative")

@patch("speech_recognition.Recognizer.recognize_google")
@patch("gtts.gTTS")
def test_voice_agent(mock_gtts, mock_recognize):
    mock_recognize.return_value = "Test query"
    mock_gtts.return_value.save.return_value = None
    agent = VoiceAgent()
    text = agent.speech_to_text("mock_audio.wav")
    assert text == "Test query"
    audio_file = agent.text_to_speech("Test response", "test.mp3")
    assert audio_file == "test.mp3"
    agent.cleanup("test.mp3")  # Ensure no crash

@patch("speech_recognition.Recognizer.recognize_google")
def test_voice_agent_speech_error(mock_recognize):
    mock_recognize.side_effect = Exception("Speech recognition error")
    agent = VoiceAgent()
    text = agent.speech_to_text("mock_audio.wav")
    assert text == ""