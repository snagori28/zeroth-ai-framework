import logging
from .llm_agent import LLM_Agent

logger = logging.getLogger(__name__)

class FeedbackAgent:
    """Use an LLM to validate facts before storage."""

    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent or LLM_Agent()

    def review(self, fact, value):
        """Return accept/edit/reject for a proposed fact."""
        prompt = f"Should this fact be stored?\nFact: {fact}\nValue: {value}\nOptions: accept/edit/reject"
        try:
            decision = self.llm_agent.query(prompt, mode="factual").lower()
            if "edit" in decision:
                return "edit"
            if "reject" in decision:
                return "reject"
            return "accept"
        except Exception as e:
            logger.error("Feedback review failed: %s", e)
            return "reject"

    def edit(self, fact, value):
        """Ask LLM for corrected fact/value pair."""
        prompt = f"Provide corrected fact and value for:\nFact: {fact}\nValue: {value}\nFormat: fact:value"
        try:
            text = self.llm_agent.query(prompt, mode="factual")
            if ':' in text:
                f, v = text.split(':',1)
                return f.strip(), v.strip()
        except Exception as e:
            logger.error("Feedback edit failed: %s", e)
        return fact, value
