import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini")
AZURE_MODEL = os.getenv("AZURE_MODEL", "gpt-4o-mini")
AZURE_OPENAI_EMBED_MODEL_NAME= os.getenv("AZURE_OPENAI_EMBED_MODEL_NAME", "")
AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT", "")