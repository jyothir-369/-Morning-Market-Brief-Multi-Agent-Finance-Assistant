from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
import uuid
from contextlib import asynccontextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env safely
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
    logger.info(f"Loaded environment variables from {dotenv_path}")
else:
    logger.warning(f".env file not found at {dotenv_path}")

# Import agents and other modules
try:
    from agents.scraping_agent import ScrapingAgent
    from agents.api_agent import APIAgent
    from agents.retriever_agent import RetrieverAgent
    from agents.analysis_agent import AnalysisAgent
    from agents.language_agent import LanguageAgent
    from agents.voice_agent import VoiceAgent
    from data_ingestion.document_loader import load_documents
    from orchestrator.router import process_query
except ImportError as e:
    logger.error(f"Failed to import modules: {str(e)}")
    raise

app = FastAPI(title="Finance Assistant Orchestrator")

# Initialize agents
try:
    api_agent = APIAgent()
    scraping_agent = ScrapingAgent()
    retriever_agent = RetrieverAgent()
    analysis_agent = AnalysisAgent()
    language_agent = LanguageAgent()
    voice_agent = VoiceAgent()
except Exception as e:
    logger.error(f"Error initializing agents: {str(e)}")
    raise

# Load and index documents
def initialize_vector_store():
    try:
        document_path = os.getenv("DOCUMENT_PATH", "sample_earnings.pdf")
        documents = load_documents(document_path)
        if documents:
            retriever_agent.index_documents(documents)
            logger.info("Initialized vector store with documents")
        else:
            logger.error("No documents loaded for vector store")
            raise RuntimeError("Failed to initialize vector store: No documents loaded")
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}")
        raise

# Lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_vector_store()
    yield

app = FastAPI(title="Finance Assistant Orchestrator", lifespan=lifespan)

# Request and response models
class QueryRequest(BaseModel):
    query: str
    audio_file: Optional[UploadFile] = File(None)

class QueryResponse(BaseModel):
    response: str
    audio_output: Optional[str] = None

# Endpoint to process query
@app.post("/process_query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    try:
        query = request.query
        if request.audio_file:
            audio_content = await request.audio_file.read()
            query = voice_agent.speech_to_text(audio_content)
            if not query:
                return QueryResponse(response="Error transcribing audio.", audio_output=None)
            logger.info(f"Transcribed audio to query: {query}")

        response = process_query(
            query=query,
            api_agent=api_agent,
            scraping_agent=scraping_agent,
            retriever_agent=retriever_agent,
            analysis_agent=analysis_agent,
            language_agent=language_agent
        )

        audio_output = f"output_{uuid.uuid4()}.mp3"
        success = voice_agent.text_to_speech(response, audio_output)
        audio_path = audio_output if success and os.path.exists(audio_output) else None

        return QueryResponse(response=response, audio_output=audio_path)

    except FileNotFoundError as e:
        logger.error(f"File error: {str(e)}")
        return QueryResponse(response=f"File error: {str(e)}", audio_output=None)
    except ValueError as e:
        logger.error(f"Transcription error: {str(e)}")
        return QueryResponse(response=f"Transcription error: {str(e)}", audio_output=None)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return QueryResponse(response=f"Error: {str(e)}", audio_output=None)

# Endpoint to download audio
@app.get("/download_audio/{filename}")
async def download_audio(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename, media_type="audio/mpeg")
    return {"error": "Audio file not found"}