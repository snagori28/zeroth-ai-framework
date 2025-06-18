import logging
from .llm_agent import LLM_Agent

logger = logging.getLogger(__name__)


class ExplainerAgent:
    """Format reasoning steps into a human-readable explanation."""

    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent or LLM_Agent()

    def explain(self, steps):
        """Create a numbered explanation from a list of steps.

        Parameters
        ----------
        steps : list[str]
            Ordered reasoning steps to be presented to the user.

        Returns
        -------
        str
            Multi-line explanation string.
        """

        logger.info("Generating explanation with %d steps", len(steps))
        prompt = "Explain this reasoning in clear language:\n" + "\n".join(steps)
        try:
            return self.llm_agent.query(prompt, mode="creative")
        except Exception as e:
            logger.error("LLM explanation failed: %s", e)
            return "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])
