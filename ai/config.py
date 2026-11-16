
from pathlib import Path
import os

from dotenv import load_dotenv

# Project root directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the project root .env file
load_dotenv(PROJECT_DIR / ".env")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.8-flash"

# RAG configuration
COLLECTION_NAME = "upi_pulse_knowledge"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

# Project paths
KNOWLEDGE_BASE_DIR = PROJECT_DIR / "ai" / "knowledge_base"
VECTOR_STORE_DIR = PROJECT_DIR / "ai" / "vector_store"

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "upi_2024_2026.csv"
)

FORECAST_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "upi_forecast_results.csv"
)
