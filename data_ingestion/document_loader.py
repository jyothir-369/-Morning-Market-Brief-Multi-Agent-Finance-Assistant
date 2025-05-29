from langchain.docstore.document import Document
from datetime import datetime
import os

def load_documents(source_dir="data_ingestion/mock_data"):
    """
    Load documents from a directory or mock data for RAG.
    Args:
        source_dir (str): Directory containing text files or mock data.
    Returns:
        list: List of LangChain Document objects.
    """
    documents = []
    
    # Mock data for demo (replace with file loading in production)
    mock_data = [
        {
            "content": "TSMC reported a 4% earnings beat for Q2 2025.",
            "metadata": {"source": "earnings", "ticker": "TSM", "date": str(datetime.now())},
        },
        {
            "content": "Samsung missed earnings estimates by 2% due to supply chain issues.",
            "metadata": {"source": "earnings", "ticker": "005930.KS", "date": str(datetime.now())},
        },
        {
            "content": "Asia tech sentiment is neutral with a cautionary tilt due to rising yields.",
            "metadata": {"source": "market", "ticker": "general", "date": str(datetime.now())},
        },
    ]
    
    # Convert mock data to LangChain Documents
    for item in mock_data:
        doc = Document(page_content=item["content"], metadata=item["metadata"])
        documents.append(doc)
    
    # In production, load from files
    if os.path.exists(source_dir):
        for filename in os.listdir(source_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(source_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    metadata = {"source": filename, "date": str(datetime.now())}
                    documents.append(Document(page_content=content, metadata=metadata))
    
    return documents

def process_documents(documents):
    """
    Process documents for RAG (e.g., clean text, add metadata).
    Args:
        documents (list): List of LangChain Document objects.
    Returns:
        list: Processed Document objects.
    """
    processed_docs = []
    for doc in documents:
        # Clean text (remove extra whitespace)
        cleaned_content = ' '.join(doc.page_content.split())
        processed_docs.append(Document(page_content=cleaned_content, metadata=doc.metadata))
    return processed_docs

if __name__ == "__main__":
    # Example usage
    docs = load_documents()
    processed_docs = process_documents(docs)
    for doc in processed_docs:
        print(f"Content: {doc.page_content}, Metadata: {doc.metadata}")