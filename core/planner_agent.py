import logging
import spacy
from .llm_agent import LLM_Agent


logger = logging.getLogger(__name__)


class PlannerAgent:
    """Generate a list of subtasks for a given goal using NLP and optionally an LLM."""

    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent or LLM_Agent()
        self.nlp = spacy.load("en_core_web_sm")

    def plan(self, goal):
        """Return a list of subtasks derived from the goal.

        Parameters
        ----------
        goal : str
            The high level objective provided by the user.

        Returns
        -------
        list[str]
            A list of subtasks to perform.
        """

        logger.info("Planning goal: %s", goal)

        subtasks = []
        prompt = f"Break this goal into subtasks:\nGoal: {goal}"
        try:
            response = self.llm_agent.query(prompt, mode="factual")
            subtasks = [line.strip('- ').strip() for line in response.split('\n') if line.strip()]
        except Exception as e:
            logger.error("LLM planning failed: %s", e)

        if not subtasks:
            try:
                doc = self.nlp(goal)
                subtasks = [chunk.text.strip() for chunk in doc.noun_chunks]
            except Exception as e:
                logger.error("spaCy planning failed: %s", e)
                subtasks = [goal]

        logger.debug("Generated subtasks: %s", subtasks)
        return subtasks
