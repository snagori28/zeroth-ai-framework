import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Minimal openai stub so LLM_Agent can be imported without the real dependency
openai_stub = types.ModuleType("openai")
class _DummyChatCompletion:
    @staticmethod
    def create(*args, **kwargs):
        raise NotImplementedError

openai_stub.ChatCompletion = _DummyChatCompletion
openai_stub.api_key = None
sys.modules["openai"] = openai_stub

import importlib
import core.llm_agent as llm_mod
importlib.reload(llm_mod)
from core.llm_agent import LLM_Agent
from config import Config
import pytest


def _dummy_response(text):
    msg = types.SimpleNamespace(content=text)
    choice = types.SimpleNamespace(message=msg)
    return types.SimpleNamespace(choices=[choice])


def test_llm_agent_query_factual(monkeypatch):
    captured = {}
    def fake_create(**kwargs):
        captured.update(kwargs)
        return _dummy_response("ok")
    monkeypatch.setattr(openai_stub.ChatCompletion, "create", fake_create)
    agent = LLM_Agent()
    result = agent.query("goal", mode="factual")
    assert result == "ok"
    assert captured["temperature"] == 0.2
    assert captured["max_tokens"] == 300
    assert "factual assistant" in captured["messages"][0]["content"]
    assert openai_stub.api_key == Config.OPENAI_API_KEY


def test_llm_agent_query_creative(monkeypatch):
    captured = {}
    def fake_create(**kwargs):
        captured.update(kwargs)
        return _dummy_response("creative")
    monkeypatch.setattr(openai_stub.ChatCompletion, "create", fake_create)
    agent = LLM_Agent()
    result = agent.query("goal", mode="creative")
    assert result == "creative"
    assert captured["temperature"] == 0.7
    assert captured["max_tokens"] == 500
    assert "Be creative" in captured["messages"][0]["content"]


def test_llm_agent_query_error(monkeypatch):
    def fake_create(**kwargs):
        raise RuntimeError("boom")
    monkeypatch.setattr(openai_stub.ChatCompletion, "create", fake_create)
    agent = LLM_Agent()
    result = agent.query("goal")
    assert result.startswith("[LLM ERROR:")
