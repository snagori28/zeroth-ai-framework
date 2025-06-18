import logging

logger = logging.getLogger(__name__)


class ReasonerAgent:
    def reason(self, facts):
        logger.info("Reasoning over %d facts", len(facts))
        return "Based on facts: " + "; ".join(facts)
