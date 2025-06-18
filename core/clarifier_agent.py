import logging
from .llm_agent import LLM_Agent

logger = logging.getLogger(__name__)

class ClarifierAgent:
    """Generate clarifying questions for an ambiguous user goal."""

    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent or LLM_Agent()

    def clarify(self, goal, num_questions=3):
        """Return a list of follow-up questions about the goal."""
        prompt = (
            f"Ask {num_questions} short questions to better understand the request: '{goal}'. "
            "Return each question on a new line."
        )
        try:
            response = self.llm_agent.query(prompt, mode="creative")
            questions = [q.strip('- ').strip() for q in response.split('\n') if q.strip()]
            return questions[:num_questions]
        except Exception as e:
            logger.error("Clarifier LLM failed: %s", e)
            return []

