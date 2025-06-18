import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# minimal openai stub
openai_stub = types.ModuleType("openai")
class _DummyChat:
    @staticmethod
    def create(*a, **k):
        raise NotImplementedError
openai_stub.ChatCompletion = _DummyChat
openai_stub.api_key = None
sys.modules["openai"] = openai_stub

from core.feedback_agent import FeedbackAgent

class DummyLLM:
    def __init__(self, responses):
        self.responses = responses
        self.queries = []

    def query(self, prompt, mode="factual"):
        self.queries.append(prompt)
        return self.responses.pop(0)

def test_feedback_decisions():
    llm = DummyLLM(["accept", "edit", "reject", "fact2: value2"])
    agent = FeedbackAgent(llm)
    assert agent.review("fact1", "value1") == "accept"
    assert agent.review("fact1", "value1") == "edit"
    assert agent.review("fact1", "value1") == "reject"
    fact, value = agent.edit("fact2", "value2")
    assert (fact, value) == ("fact2", "value2")

