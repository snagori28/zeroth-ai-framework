import os
import logging
from .feedback_agent import FeedbackAgent

logger = logging.getLogger(__name__)

class DocumentIngestor:
    """Parse documents and store extracted facts using provided agents."""

    def __init__(self, llm_agent, memory_agent, feedback_agent=None):
        """Create a new ingestor.

        Parameters
        ----------
        llm_agent : LLM_Agent
            Agent used to convert text into factual statements.
        memory_agent : MemoryAgent
            Agent responsible for persisting the extracted facts.
        """

        self.llm_agent = llm_agent
        self.memory_agent = memory_agent
        self.feedback_agent = feedback_agent or FeedbackAgent(llm_agent)

    def ingest(self, content_or_path):
        """Ingest text or a file path and store discovered facts.

        Parameters
        ----------
        content_or_path : str
            Either raw text content or a path to a text file.

        Returns
        -------
        None
        """

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

        facts = self.llm_agent.query("Extract structured facts from this document:\n" + content, mode="factual")
        for line in facts.split("\n"):
            if ":" in line:
                fact, value = line.split(":", 1)
                fact = fact.strip()
                value = value.strip()
                decision = self.feedback_agent.review(fact, value)
                logger.debug("Feedback decision for '%s': %s", fact, decision)
                if decision == "reject":
                    continue
                if decision == "edit":
                    fact, value = self.feedback_agent.edit(fact, value)
                self.memory_agent.store(fact, value, source="document")
