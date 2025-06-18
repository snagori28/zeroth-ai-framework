import os
import logging
from pathlib import Path

class Config:
    # Neo4j Settings
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test")

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

    # File Uploads
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(Path(__file__).parent.resolve() / "uploads"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Security or future config placeholders
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 5))


logging.basicConfig(
    level=Config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
