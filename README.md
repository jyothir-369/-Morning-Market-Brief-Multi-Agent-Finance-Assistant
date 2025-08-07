# 🧠 Morning Market Brief: Multi-Agent Finance Assistant

A modular, voice-enabled finance assistant that delivers real-time market updates through a multi-agent system. Built with FastAPI, Streamlit, and integrated with tools like yfinance, BeautifulSoup, FAISS, and HuggingFace, this assistant provides verbal summaries such as:

> “Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt due to rising yields.”

---

## 🚀 Live Demo

🟡 **Coming Soon** – Will be hosted via Streamlit Cloud + Dockerized FastAPI microservice.

---

## 🧩 System Overview

**Microservices Architecture** powered by FastAPI with dedicated agents for each responsibility:

[User Query (Voice/Text)]
↓
[Streamlit App UI]
↓
[FastAPI Orchestrator]
↓
┌────────────────────────────┐
| API Scrape RAG NLP TTS |
└────────────────────────────┘

markdown
Copy
Edit

| Agent | Role |
|-------|------|
| 🧾 **API Agent** | Fetches stock data (e.g., TSMC, Samsung) via `yfinance` |
| 🔍 **Scraping Agent** | Gathers earnings data using `BeautifulSoup` |
| 📚 **Retriever Agent** | Retrieves insights using `FAISS` + `LangChain` |
| 📊 **Analysis Agent** | Computes portfolio exposure, risk, and summaries |
| 🧠 **Language Agent** | Generates narrative responses (LLM: `distilgpt2`) |
| 🎤 **Voice Agent** | Converts between speech and text (`speech_recognition`, `gTTS`) |
| 🌐 **Orchestrator** | FastAPI microservice that routes tasks between agents |
| 🖼️ **Streamlit App** | Web UI for input/output, supports voice interaction |

---

## 📁 Project Structure

Project_root/
├── agents/ # Modular agent logic
│ ├── api_agent.py
│ ├── scraping_agent.py
│ ├── retriever_agent.py
│ ├── analysis_agent.py
│ ├── language_agent.py
│ └── voice_agent.py
├── data_ingestion/ # Tools for data collection
│ ├── api.py
│ ├── scraper.py
│ └── document_loader.py
├── orchestrator/ # FastAPI microservice
│ ├── main.py
│ └── router.py
├── streamlit_app/ # Frontend (Streamlit)
│ └── app.py
├── docs/
│ └── ai_tool_usage.md # AI usage logs and debug notes
├── tests/ # Unit and pipeline tests
│ ├── test_agents.py
│ └── test_pipeline.py
├── .env # API keys and secrets (ignored in Git)
├── requirements.txt
├── Dockerfile
└── README.md

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 🔧 Local Development

```bash
# Clone the repository
git clone https://github.com/jyothir-369/Project_root.git
cd Project_root

# Install dependencies
pip install -r requirements.txt
⚙️ Run the App
bash
Copy
Edit
# Run the FastAPI orchestrator
uvicorn orchestrator.main:app --host 0.0.0.0 --port 8000

# Run the Streamlit app
streamlit run streamlit_app/app.py
Access the app at: http://localhost:8501

📦 Docker Deployment
bash
Copy
Edit
# Build Docker image
docker build -t market-brief .

# Run the container
docker run -p 8501:8501 -p 8000:8000 market-brief
Access:

Streamlit App: http://localhost:8501

FastAPI API: http://localhost:8000

⚖️ Framework/Tool Justification
Category	Tool	Reason
RAG	FAISS + LangChain	Fast, local retrieval, no external dependencies
LLM	HuggingFace (distilgpt2)	Open-source, light and customizable
TTS/STT	gTTS + speech_recognition	Simple, fast, web-deployable
Market Data	yfinance	Free and reliable for financial data
Scraping	BeautifulSoup	Lightweight, effective
Orchestration	FastAPI	High performance, async-friendly
UI	Streamlit	Easy deployment and prototyping

📊 Performance Snapshot
Component	Latency
API Fetch	~1–2s per ticker
Earnings Scrape	~2–3s
RAG Lookup	~0.5–1s
Voice Input/Output	~2–4s
End-to-End Query	~5–7s total

🧪 Testing
bash
Copy
Edit
pytest tests/
test_agents.py: Unit tests for each agent

test_pipeline.py: Integration tests from query to spoken output

📓 AI Tool Usage
Code scaffolded using Grok-3 for:

Agent orchestration logic

RAG pipeline optimization

Prompt engineering

Logs available in docs/ai_tool_usage.md

📝 Notes
Uses mock portfolio and earnings data for demo purposes

Streamlit Cloud does not support FastAPI, so orchestrator must run separately (e.g., via Docker or cloud service)

Easily extendable to handle other regions, sectors, or asset types

🙋‍♂️ Author
Jyothir Raghavalu Bhogi
🔗 GitHub: @jyothir-369

📄 License
This project is licensed under the MIT License – use it freely for personal or commercial purposes.
