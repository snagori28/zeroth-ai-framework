import logging
from .llm_agent import LLM_Agent

logger = logging.getLogger(__name__)


class ReasonerAgent:
    """Combine stored facts to produce a single inference using chain-of-thought prompting."""

    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent or LLM_Agent()

    def reason(self, facts):
        """Return a conclusion derived from a list of facts.

        Parameters
        ----------
        facts : list[str]
            Known facts relevant to the reasoning task.

        Returns
        -------
        str
            A summary conclusion produced from the facts.
        """

        logger.info("Reasoning over %d facts", len(facts))
        prompt = "Based on the facts below, what can you infer?\n" + "\n".join(facts) + "\nExplain step by step then provide a final concise conclusion."
        try:
            response = self.llm_agent.query(prompt, mode="factual")
            return response
        except Exception as e:
            logger.error("Reasoning LLM failed: %s", e)
            return "; ".join(facts)
