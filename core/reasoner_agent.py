import logging

logger = logging.getLogger(__name__)


class ReasonerAgent:
    """Combine stored facts to produce a single inference."""

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
        return "Based on facts: " + "; ".join(facts)
