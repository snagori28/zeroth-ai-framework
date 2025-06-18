import logging

logger = logging.getLogger(__name__)


class PlannerAgent:
    def plan(self, goal):
        logger.info("Planning goal: %s", goal)
        return [f"Resolve subtask: {goal}"]
