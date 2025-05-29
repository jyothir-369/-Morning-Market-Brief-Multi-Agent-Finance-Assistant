import pytest
from fastapi.testclient import TestClient
from orchestrator.main import app
from unittest.mock import patch
from langchain.docstore.document import Document

# Mock data for pipeline tests
mock_market_data = {
    "realtime": {"TSM": {"price": 150}},
    "historical": {"TSM": {"Close": {"2025-05-01": 148}}}
}
mock_earnings_data = {"TSM": "beat estimates by 4%"}
mock_retrieved_docs = [(Document(page_content="TSMC beat earnings by 4%", metadata={"source": "earnings"}), 0.9)]
mock_analysis = {
    "current_allocation": "22%",
    "yesterday_allocation": "18%",
    "earnings_summary": {"TSM": "beat estimates by 4%"},
    "price_changes": {"TSM": "Current price: 150"}
}
mock_response = "Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%."

client = TestClient(app)

@patch("os.getenv")
@patch("agents.api_agent.APIAgent.get_market_data")
@patch("agents.scraping_agent.ScrapingAgent.get_earnings_data")
@patch("agents.retriever_agent.RetrieverAgent.retrieve")
@patch("agents.analysis_agent.AnalysisAgent.analyze_risk_exposure")
@patch("agents.language_agent.LanguageAgent.generate_narrative")
@patch("agents.voice_agent.VoiceAgent.text_to_speech")
@patch("data_ingestion.document_loader.load_documents")
def test_pipeline(
    mock_load_docs,
    mock_tts,
    mock_language,
    mock_analysis,
    mock_retrieve,
    mock_scrape,
    mock_api,
    mock_getenv
):
    mock_getenv.return_value = "mock_openai_api_key"
    mock_load_docs.return_value = [Document(page_content="Mock earnings document")]
    mock_api.return_value = mock_market_data
    mock_scrape.return_value = mock_earnings_data
    mock_retrieve.return_value = mock_retrieved_docs
    mock_analysis.return_value = mock_analysis
    mock_language.return_value = mock_response
    mock_tts.return_value = "response.mp3"

    response = client.post(
        "/process_query",
        json={"query": "What's our risk exposure in Asia tech stocks today?"}
    )
    assert response.status_code == 200
    assert response.json()["response"] == mock_response
    assert response.json()["audio_output"] == "response.mp3"

@patch("os.getenv")
@patch("agents.retriever_agent.RetrieverAgent.retrieve")
@patch("data_ingestion.document_loader.load_documents")
def test_pipeline_error(mock_load_docs, mock_retrieve, mock_getenv):
    mock_getenv.return_value = "mock_openai_api_key"
    mock_load_docs.return_value = [Document(page_content="Mock earnings document")]
    mock_retrieve.side_effect = Exception("Retrieval error")
    response = client.post(
        "/process_query",
        json={"query": "What's our risk exposure in Asia tech stocks today?"}
    )
    assert response.status_code == 200
    assert response.json()["response"].startswith("Error:")
    assert response.json()["audio_output"] is None