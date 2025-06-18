import logging
from .llm_agent import LLM_Agent

logger = logging.getLogger(__name__)

class ClarifierAgent:
    """Generate clarifying questions for a given goal."""

    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent or LLM_Agent()

    def clarify(self, goal, num_questions=3):
        """Return a list of clarifying questions."""
        prompt = (
            f"Provide {num_questions} clarifying questions that would help better understand the following goal:\n{goal}"
        )
        try:
            text = self.llm_agent.query(prompt, mode="factual")
            questions = [q.strip('- ').strip() for q in text.split('\n') if q.strip()]
            return questions
        except Exception as e:
            logger.error("Clarification failed: %s", e)
            return []

