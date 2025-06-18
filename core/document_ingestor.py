import os
import logging

logger = logging.getLogger(__name__)

class DocumentIngestor:
    def __init__(self, llm_agent, memory_agent):
        self.llm_agent = llm_agent
        self.memory_agent = memory_agent

    def ingest(self, content_or_path):
        logger.info("Ingesting content or path: %s", content_or_path)
        # Check if the input is a path to a file
        if os.path.exists(content_or_path) and os.path.isfile(content_or_path):
            ext = os.path.splitext(content_or_path)[1].lower()
            if ext == ".txt":
                with open(content_or_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        else:
            content = content_or_path

        facts = self.llm_agent.query(content, mode="factual")
        for line in facts.split("\n"):
            if ":" in line:
                fact, value = line.split(":", 1)
                logger.debug("Storing fact '%s'", fact.strip())
                self.memory_agent.store(fact.strip(), value.strip(), source="document")
