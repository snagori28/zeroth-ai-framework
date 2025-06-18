import openai
from config import Config
import logging

logger = logging.getLogger(__name__)

class LLM_Agent:
    """Wrapper around the OpenAI API used to query language models."""

    def __init__(self):
        """Initialize the agent and configure the OpenAI API key."""

        logger.info("Initializing LLM agent")
        openai.api_key = Config.OPENAI_API_KEY

    def query(self, goal, mode="factual"):
        """Send a prompt to the language model.

        Parameters
        ----------
        goal : str
            The user's request or question.
        mode : str, optional
            Either ``"factual"`` for concise facts or ``"creative"`` for a
            longer answer. Defaults to ``"factual"``.

        Returns
        -------
        str
            The model's textual response or an error message.
        """

        logger.info("Querying LLM with mode '%s'", mode)
        if mode == "factual":
            prompt = f"You are a factual assistant. Provide concise structured facts for the task: '{goal}'. List all relevant facts as bullet points."
            temperature = 0.2
            max_tokens = 300
        else:
            prompt = f"Be creative and helpful. Answer the user query: '{goal}'"
            temperature = 0.7
            max_tokens = 500

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error("LLM query failed: %s", e)
            return f"[LLM ERROR: {e}]"
