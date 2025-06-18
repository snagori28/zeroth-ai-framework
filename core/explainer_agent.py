import logging

logger = logging.getLogger(__name__)


class ExplainerAgent:
    def explain(self, steps):
        logger.info("Generating explanation with %d steps", len(steps))
        return "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])
