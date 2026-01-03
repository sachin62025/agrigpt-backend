import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Storage Paths
    CHROMA_PATH = "vector_db"
    DATA_DIR = "data"
    
    # PDF filenames
    DISEASE_PDF = "CitrusPlantPestsAndDiseases.pdf"
    SCHEME_PDF = "GovernmentSchemes.pdf"
    
    # Collection Names
    DISEASE_COLLECTION = "citrus_diseases"
    SCHEME_COLLECTION = "govt_schemes"
    
    # Model Configuration
    EMBEDDING_MODEL = "models/embedding-001"
    # LLM_MODEL = "gemini-1.5-flash"
    LLM_MODEL = "gpt-3.5-turbo"