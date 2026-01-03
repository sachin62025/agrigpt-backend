from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import Config
import os

def process_pdf(file_path, collection_name):
    # Load document
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # Chunking strategy
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)
    
    # Initialize Embeddings
    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model=Config.EMBEDDING_MODEL,
    #     google_api_key=Config.GOOGLE_API_KEY
    # )
    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
    )
    
    # Create and Persist Vector Store
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=Config.CHROMA_PATH,
        collection_name=collection_name
    )
    print(f"Successfully ingested {len(chunks)} chunks into {collection_name}")

def run_ingestion():
   
    disease_path = os.path.join(Config.DATA_DIR, Config.DISEASE_PDF)
    scheme_path = os.path.join(Config.DATA_DIR, Config.SCHEME_PDF)
    
    if not os.path.exists(Config.DATA_DIR):
        os.makedirs(Config.DATA_DIR)
        print(f"Created {Config.DATA_DIR} folder. Place your PDFs there.")
        return

    # Process Disease KB
    if os.path.exists(disease_path):
        process_pdf(disease_path, Config.DISEASE_COLLECTION)
    else:
        print(f"Missing: {disease_path}")

    # Process Schemes KB
    if os.path.exists(scheme_path):
        process_pdf(scheme_path, Config.SCHEME_COLLECTION)
    else:
        print(f"Missing: {scheme_path}")

if __name__ == "__main__":
    run_ingestion()