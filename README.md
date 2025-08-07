# 🧠 Morning Market Brief: Multi-Agent Finance Assistant

A **modular, voice-enabled finance assistant** that delivers real-time market updates using multiple AI agents. It responds to queries like:

> _“Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%...”_

Built using **FastAPI**, **Streamlit**, and integrated with tools like `yfinance`, `BeautifulSoup`, `FAISS`, and `HuggingFace`.

---

## 🚀 Live Demo

🟡 _Coming Soon_ – Will be hosted using **Streamlit Cloud** and **Dockerized FastAPI** microservice.

---

## 🧩 System Architecture

[User Query (Voice/Text)]
↓
[Streamlit App UI]
↓
[FastAPI Orchestrator]
↓
┌────────────────────────────┐
| API | Scrape | RAG | NLP | TTS |
└────────────────────────────┘

markdown
Copy
Edit

| Agent | Responsibility |
|-------|----------------|
| 📄 **API Agent** | Fetches stock data via `yfinance` |
| 🔍 **Scraping Agent** | Extracts earnings data using `BeautifulSoup` |
| 📚 **Retriever Agent** | Retrieves insights via `FAISS` + `LangChain` |
| 📊 **Analysis Agent** | Computes exposure, earnings surprises, summaries |
| 🧠 **Language Agent** | Generates narrative using `HuggingFace` LLM (distilgpt2) |
| 🎤 **Voice Agent** | Handles speech-to-text and text-to-speech |
| 🌐 **Orchestrator** | Manages agent coordination via `FastAPI` |
| 🖼️ **Streamlit App** | Frontend for voice/text input and verbal responses |

---

## 📁 Project Structure

Project_root/
├── agents/ # Modular AI agents
│ ├── api_agent.py
│ ├── scraping_agent.py
│ ├── retriever_agent.py
│ ├── analysis_agent.py
│ ├── language_agent.py
│ └── voice_agent.py
├── data_ingestion/ # Data loaders and scrapers
│ ├── api.py
│ ├── scraper.py
│ └── document_loader.py
├── orchestrator/ # FastAPI microservice
│ ├── main.py
│ └── router.py
├── streamlit_app/ # Streamlit-based UI
│ └── app.py
├── tests/ # Unit and integration tests
│ ├── test_agents.py
│ └── test_pipeline.py
├── docs/
│ └── ai_tool_usage.md
├── Dockerfile
├── .env
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 🔧 Local Development

```bash
git clone https://github.com/jyothir-369/Project_root.git
cd Project_root
pip install -r requirements.txt
⚙️ Run the App
bash
Copy
Edit
# Run FastAPI Orchestrator
uvicorn orchestrator.main:app --host 0.0.0.0 --port 8000

# Run Streamlit App
streamlit run streamlit_app/app.py
Streamlit App: http://localhost:8501

FastAPI Docs: http://localhost:8000/docs

📦 Docker Deployment
bash
Copy
Edit
# Build Docker image
docker build -t market-brief .

# Run container
docker run -p 8501:8501 -p 8000:8000 market-brief
⚖️ Tech Stack & Justification
Category	Tool	Reason
RAG	FAISS + LangChain	Fast local retrieval
LLM	HuggingFace (distilgpt2)	Lightweight, open-source
TTS / STT	gTTS + speech_recognition	Simple & deployable
Market Data	yfinance	Free, easy access
Scraping	BeautifulSoup	Lightweight and reliable
Orchestration	FastAPI	Async, microservice-ready
UI	Streamlit	Great for fast prototyping

📊 Performance Snapshot
Component	Latency
API Fetch	~1–2s
Earnings Scrape	~2–3s
RAG Retrieval	~0.5–1s
Voice I/O	~2–4s
Total Response	~5–7s

🧪 Testing
bash
Copy
Edit
pytest tests/
test_agents.py – Unit tests for each individual agent

test_pipeline.py – End-to-end pipeline test

📓 AI Tool Usage
AI-assisted development using Grok-3 for:

Multi-agent orchestration logic

RAG prompt engineering

Test generation and scaffolding

Logs and prompts available in docs/ai_tool_usage.md

📎 Notes
Uses mock portfolio & earnings data for demo

FastAPI must run separately in production (e.g., Docker or cloud)

Easily extendable to other regions, sectors, or asset types

Voice features can be enhanced with Whisper for better accuracy

🙋‍♂️ Author
Jyothir Raghavalu Bhogi
🔗 GitHub: @jyothir-369

📄 License
This project is licensed under the MIT License – free to use, modify, and distribute.

