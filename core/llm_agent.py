import openai
from config import Config

class LLM_Agent:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def query(self, goal, mode="factual"):
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
            return f"[LLM ERROR: {e}]"