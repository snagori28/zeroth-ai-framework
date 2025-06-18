import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide a minimal neo4j module so MemoryAgent can be imported without the real
# dependency installed.
neo4j_stub = types.ModuleType("neo4j")
class _DummyGraphDatabase:
    @staticmethod
    def driver(*args, **kwargs):
        raise NotImplementedError

neo4j_stub.GraphDatabase = _DummyGraphDatabase
sys.modules.setdefault("neo4j", neo4j_stub)

# minimal openai stub so imports work
openai_stub = types.ModuleType("openai")
class _DummyChat:
    @staticmethod
    def create(*a, **k):
        raise NotImplementedError
openai_stub.ChatCompletion = _DummyChat
openai_stub.api_key = None
sys.modules["openai"] = openai_stub

# minimal spacy stub
spacy_stub = types.ModuleType("spacy")
class _DummyDoc:
    def __init__(self, text=""):
        self.text = text
        self.noun_chunks = []
    def similarity(self, other):
        return 0.0
class _DummyNLP:
    def __call__(self, text):
        return _DummyDoc(text)
spacy_stub.load = lambda name: _DummyNLP()
sys.modules.setdefault("spacy", spacy_stub)

from core.planner_agent import PlannerAgent
from core.reasoner_agent import ReasonerAgent
from core.explainer_agent import ExplainerAgent
from core.llm_agent import LLM_Agent
from core.memory_agent import MemoryAgent

import pytest


class DummyResult:
    def __init__(self, value=None):
        self._value = value

    def single(self):
        if self._value is None:
            return None
        return {"value": self._value}


class DummySession:
    def __init__(self, store):
        self.store = store

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def run(self, cypher, **params):
        if cypher.strip().startswith("MERGE"):
            self.store[params["name"]] = params["value"]
            return DummyResult()
        elif cypher.strip().startswith("MATCH"):
            value = self.store.get(params["name"])
            return DummyResult(value)
        return DummyResult()


class DummyDriver:
    def __init__(self):
        self.store = {}

    def session(self):
        return DummySession(self.store)


# Tests for simple agents

def test_planner_plan_returns_list():
    agent = PlannerAgent()
    result = agent.plan("test goal")
    assert isinstance(result, list)


def test_reasoner_uses_llm(monkeypatch):
    dummy = types.SimpleNamespace()
    monkeypatch.setattr(LLM_Agent, "query", lambda self, prompt, mode="factual": "result")
    agent = ReasonerAgent(llm_agent=LLM_Agent())
    facts = ["fact1", "fact2"]
    assert agent.reason(facts) == "result"


def test_explainer_formats_steps(monkeypatch):
    monkeypatch.setattr(LLM_Agent, "query", lambda self, prompt, mode="creative": "explain")
    agent = ExplainerAgent(llm_agent=LLM_Agent())
    steps = ["step one", "step two"]
    assert agent.explain(steps) == "explain"


# Test for MemoryAgent using mocked Neo4j driver

def test_memory_agent_store_and_retrieve(monkeypatch):
    dummy_driver = DummyDriver()
    monkeypatch.setattr("core.memory_agent.GraphDatabase.driver", lambda *a, **kw: dummy_driver)
    monkeypatch.setattr(LLM_Agent, "query", lambda self, prompt, mode="factual": "")

    memory = MemoryAgent(llm_agent=LLM_Agent())
    memory.store("fact", "value")

    assert dummy_driver.store["fact"] == "value"
    assert memory.retrieve("fact") == "value"
