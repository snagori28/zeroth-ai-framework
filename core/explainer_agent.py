import logging

logger = logging.getLogger(__name__)


class ExplainerAgent:
    """Format reasoning steps into a human-readable explanation."""

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
        return "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])
