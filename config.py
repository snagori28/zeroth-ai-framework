import os
import logging
from pathlib import Path

class Config:
    """Simple configuration container populated from environment variables."""

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


def ensure_env_vars():
    """Prompt for required environment variables if they are missing."""

    required = {
        "NEO4J_URI": Config.NEO4J_URI,
        "NEO4J_USER": Config.NEO4J_USER,
        "NEO4J_PASSWORD": Config.NEO4J_PASSWORD,
        "OPENAI_API_KEY": Config.OPENAI_API_KEY,
    }

    for var, value in required.items():
        if not value:
            entered = input(f"Enter value for {var}: ").strip()
            os.environ[var] = entered

    # reload configuration values from environment
    Config.NEO4J_URI = os.getenv("NEO4J_URI", Config.NEO4J_URI)
    Config.NEO4J_USER = os.getenv("NEO4J_USER", Config.NEO4J_USER)
    Config.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", Config.NEO4J_PASSWORD)
    Config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", Config.OPENAI_API_KEY)
    Config.UPLOAD_DIR = os.getenv("UPLOAD_DIR", Config.UPLOAD_DIR)
    Config.LOG_LEVEL = os.getenv("LOG_LEVEL", Config.LOG_LEVEL)
    Config.MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", Config.MAX_UPLOAD_SIZE_MB))


logging.basicConfig(
    level=Config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
