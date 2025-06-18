import logging

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Generate a simple list of subtasks for a given goal."""

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
        return [f"Resolve subtask: {goal}"]
