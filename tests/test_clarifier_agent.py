import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# minimal openai stub
openai_stub = types.ModuleType("openai")
class _DummyChat:
    @staticmethod
    def create(*a, **k):
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="Q1\nQ2\nQ3"))])
openai_stub.ChatCompletion = _DummyChat
openai_stub.api_key = None
sys.modules["openai"] = openai_stub

import importlib
import core.llm_agent as llm_mod
importlib.reload(llm_mod)
from core.llm_agent import LLM_Agent
import core.clarifier_agent as clarifier_mod
importlib.reload(clarifier_mod)
from core.clarifier_agent import ClarifierAgent


def test_clarifier_returns_list(monkeypatch):
    monkeypatch.setattr(LLM_Agent, "query", lambda self, prompt, mode="creative": "Q1\nQ2\nQ3")
    agent = ClarifierAgent(llm_agent=LLM_Agent())
    questions = agent.clarify("goal")
    assert questions == ["Q1", "Q2", "Q3"]

