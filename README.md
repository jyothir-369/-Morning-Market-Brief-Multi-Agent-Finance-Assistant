# 🧠 Morning Market Brief: Multi-Agent Finance Assistant

A **modular, voice-enabled finance assistant** that delivers real-time market updates using multiple AI agents.

> “Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday.  
> TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral.”

Built with `FastAPI`, `Streamlit`, and integrated tools like `yfinance`, `BeautifulSoup`, `FAISS`, and `HuggingFace`.

---

## 🚀 Live Demo

🟡 **Coming Soon** – Will be hosted via Streamlit Cloud & Dockerized FastAPI Microservice

---

## 🧩 System Architecture

```text
[User Query (Voice/Text)]
         ↓
  [Streamlit App UI]
         ↓
 [FastAPI Orchestrator]
         ↓
┌────────────────────────────┐
|   API | Scrape | RAG | NLP | TTS   |
└────────────────────────────┘
🧠 Multi-Agent System Overview
Agent	Responsibility
📄 API Agent	Fetches stock data (e.g., TSMC, Samsung) using yfinance
🔍 Scraping Agent	Gathers earnings data using BeautifulSoup
📚 Retriever Agent	Retrieves financial insights via FAISS + LangChain
📊 Analysis Agent	Computes portfolio exposure, earnings surprise, and narrative summaries
🧠 Language Agent	Generates human-like responses using distilgpt2 from HuggingFace
🎤 Voice Agent	Converts speech to text & vice versa using speech_recognition, gTTS
🌐 Orchestrator	Coordinates agents using FastAPI
🖼️ Streamlit App	Web UI for interaction (voice or text), displays responses

📁 Project Structure
bash
Copy
Edit
Project_root/
├── agents/              # Modular agent logic
│   ├── api_agent.py
│   ├── scraping_agent.py
│   ├── retriever_agent.py
│   ├── analysis_agent.py
│   ├── language_agent.py
│   └── voice_agent.py
├── data_ingestion/      # Loaders and scrapers
│   ├── api.py
│   ├── scraper.py
│   └── document_loader.py
├── orchestrator/        # FastAPI backend
│   ├── main.py
│   └── router.py
├── streamlit_app/       # Frontend (Streamlit)
│   └── app.py
├── tests/               # Unit & integration tests
│   ├── test_agents.py
│   └── test_pipeline.py
├── docs/
│   └── ai_tool_usage.md
├── Dockerfile
├── .env
├── requirements.txt
└── README.md
🛠️ Setup Instructions
🔧 Local Development
bash
Copy
Edit
# Clone the repository
git clone https://github.com/jyothir-369/Project_root.git
cd Project_root

# Install dependencies
pip install -r requirements.txt
⚙️ Run the App
bash
Copy
Edit
# Start FastAPI (backend)
uvicorn orchestrator.main:app --host 0.0.0.0 --port 8000

# Start Streamlit (frontend)
streamlit run streamlit_app/app.py
Streamlit App → http://localhost:8501

FastAPI Docs → http://localhost:8000/docs

📦 Docker Deployment
bash
Copy
Edit
# Build Docker image
docker build -t market-brief .

# Run the container
docker run -p 8501:8501 -p 8000:8000 market-brief
⚖️ Tech Stack & Justification
Category	Tool	Reason
RAG	FAISS + LangChain	Fast, local embedding-based retrieval
LLM	HuggingFace (distilgpt2)	Open-source, lightweight & customizable
TTS / STT	gTTS + speech_recognition	Fast, deployable speech interface
Market Data	yfinance	Free & reliable stock/ETF data
Scraping	BeautifulSoup	Lightweight for extracting web data
Orchestration	FastAPI	Async-ready, microservice architecture
UI	Streamlit	Rapid prototyping and frontend integration

📊 Performance Snapshot
Component	Average Latency
API Fetch	~1–2s
Earnings Scrape	~2–3s
RAG Lookup	~0.5–1s
Voice Input/Output	~2–4s
End-to-End Query	~5–7s

🧪 Testing
bash
Copy
Edit
pytest tests/
test_agents.py – Unit tests for each agent

test_pipeline.py – End-to-end system test

📓 AI Tool Usage
🧠 Developed using AI-assisted scaffolding (Grok-3)

🧱 Prompt engineering & multi-agent orchestration logic

📜 Logs stored in docs/ai_tool_usage.md

📎 Notes
Uses mock data for portfolios & earnings (can be replaced with real-time feeds)

FastAPI backend must be hosted separately in production (Streamlit Cloud doesn’t support custom APIs)

Extendable to new asset classes (commodities, crypto), sectors, or global regions

Replace gTTS with Whisper for improved speech accuracy (optional)

🙋‍♂️ Author
Jyothir Raghavalu Bhogi
🔗 GitHub: @jyothir-369

