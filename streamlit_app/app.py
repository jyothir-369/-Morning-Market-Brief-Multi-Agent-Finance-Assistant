import streamlit as st
import requests
import yfinance as yf
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
import speech_recognition as sr
from gtts import gTTS
import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise KeyError
except KeyError:
    st.error("OpenAI API key not found in .env file. Please set OPENAI_API_KEY in C:\\Users\\Jayavardhan\\Documents\\CLOUD\\OneDrive\\Desktop\\project_root\\.env.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

ORCHESTRATOR_URL = "http://localhost:8000/orchestrate"

# Initialize embeddings and vector store
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    documents = [
        Document(page_content="TSMC reported a 4% earnings beat for Q2 2025.", metadata={"source": "earnings"}),
        Document(page_content="Samsung missed earnings estimates by 2% due to supply chain issues.", metadata={"source": "earnings"}),
        Document(page_content="Asia tech sentiment is neutral with a cautionary tilt due to rising yields.", metadata={"source": "market"}),
    ]
    vector_store = FAISS.from_documents(documents, embeddings)
except Exception as e:
    st.error(f"Failed to initialize embeddings or vector store: {e}")
    st.stop()

# --- UI design tweaks ---
st.set_page_config(
    page_title="Morning Market Brief",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main > div.block-container {
        max-width: 700px;
        padding: 2rem 3rem;
        background: #f9fafb;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    h1 {
        color: #0a74da;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #0a74da;
        color: white;
        font-weight: 600;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #064a9a;
    }
    .stCheckbox>div {
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📈 Morning Market Brief")
st.write(
    "Ask about your **Asia tech stock exposure** and **earnings surprises**. "
    "You can type your query or use voice input."
)

# Layout: Voice input checkbox and text input
col1, col2 = st.columns([1, 2])

with col1:
    use_voice = st.checkbox("Use Voice Input")

with col2:
    if use_voice:
        st.info("Click the button below and speak your query.")
        if st.button("🎤 Record Query"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    query = recognizer.recognize_google(audio)
                    st.success(f"You said: {query}")
                except sr.UnknownValueError:
                    st.error("Could not understand audio.")
                    query = None
                except sr.RequestError as e:
                    st.error(f"Speech recognition service unavailable: {e}")
                    query = None
                except Exception as e:
                    st.error(f"Voice input error: {e}")
                    query = None
        else:
            query = None
    else:
        query = st.text_input(
            "Enter your query",
            placeholder="What's our risk exposure in Asia tech stocks today, and highlight any earnings surprises?",
        )

def get_market_price_safe(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info.get("regularMarketPrice", 0)
    except Exception as e:
        st.warning(f"Could not fetch market price for {ticker}: {e}")
        return 0

def generate_llm_response(query, context):
    prompt = (
        f"Context:\n{context}\n\n"
        f"User query:\n{query}\n\n"
        "Provide a concise, clear market brief answer based on the context."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing market briefs."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"LLM API call failed: {e}")
        return None

if st.button("Get Market Brief"):
    if query:
        with st.spinner("Fetching data and generating your market brief..."):
            portfolio = {"TSMC": 0.12, "Samsung": 0.10}
            yesterday_portfolio = {"TSMC": 0.10, "Samsung": 0.08}

            tickers = ["TSMC", "005930.KS"]
            market_data = {ticker: get_market_price_safe(ticker) for ticker in tickers}

            earnings_data = {
                "TSMC": "beat estimates by 4%",
                "Samsung": "missed estimates by 2%",
            }

            try:
                retriever_results = vector_store.similarity_search(query, k=3)
                context = "\n".join([doc.page_content for doc in retriever_results])
            except Exception as e:
                st.error(f"Vector store search failed: {e}")
                context = ""

            additional_context = (
                f"Portfolio allocation today: {sum(portfolio.values())*100:.0f}% of AUM, "
                f"up from {sum(yesterday_portfolio.values())*100:.0f}% yesterday.\n"
                f"Latest earnings: TSMC {earnings_data['TSMC']}, Samsung {earnings_data['Samsung']}.\n"
                f"Market prices: TSMC {market_data.get('TSMC', 'N/A')}, Samsung {market_data.get('005930.KS', 'N/A')}."
            )

            full_context = context + "\n" + additional_context

            response = generate_llm_response(query, full_context)
            if not response:
                response = "Sorry, I couldn't generate a response at the moment."

            # Display response
            st.markdown("### 📊 Market Brief Response")
            st.info(response)

            # Voice output
            try:
                tts = gTTS(text=response, lang="en")
                audio_file = f"response_{uuid.uuid4()}.mp3"
                tts.save(audio_file)
                st.audio(audio_file)
                os.remove(audio_file)
            except Exception as e:
                st.warning(f"Text-to-speech failed: {e}")

            # Orchestrator call
            try:
                fastapi_response = requests.post(ORCHESTRATOR_URL, json={"query": query, "context": full_context})
                fastapi_response.raise_for_status()
                st.markdown("### 🔗 Orchestrator Response")
                st.write(fastapi_response.json().get("result", "No result returned"))
            except requests.RequestException as e:
                st.warning(f"Orchestrator unavailable: {e}")
    else:
        st.error("Please provide a query.")