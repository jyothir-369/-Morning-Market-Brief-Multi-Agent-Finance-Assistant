from fastapi import APIRouter
from pydantic import BaseModel
from agents.api_agent import APIAgent
from agents.scraping_agent import ScrapingAgent
from agents.retriever_agent import RetrieverAgent
from agents.analysis_agent import AnalysisAgent
from agents.language_agent import LanguageAgent
from agents.voice_agent import VoiceAgent

router = APIRouter()

class QueryInput(BaseModel):
    query: str
    audio_file: str = None

@router.post("/process")
async def process_query(input: QueryInput):
    api_agent = APIAgent()
    scraping_agent = ScrapingAgent()
    retriever_agent = RetrieverAgent()
    analysis_agent = AnalysisAgent()
    language_agent = LanguageAgent()
    voice_agent = VoiceAgent()

    query = voice_agent.speech_to_text(input.audio_file) if input.audio_file else input.query
    market_data = api_agent.get_market_data()
    scraped_data = scraping_agent.get_earnings_data(query)
    retriever_agent.index(scraped_data)
    context = retriever_agent.retrieve(query)

    if not context:
        fallback = "Please clarify your query."
        output_audio = voice_agent.text_to_speech(fallback)
        return {"response": fallback, "audio": output_audio}

    exposure = analysis_agent.calculate_exposure(market_data)
    earnings_surprise = analysis_agent.check_earnings_surprise(market_data.get("TSM", {}), "TSM")
    earnings_text = f"TSMC beat estimates by {earnings_surprise:.1f}%." if earnings_surprise else "No earnings data."
    context_text = context[0].page_content if context else "Neutral sentiment."
    narrative = language_agent.generate_narrative(exposure, earnings_text, context_text)
    output_audio = voice_agent.text_to_speech(narrative)

    return {"response": narrative, "audio": output_audio}