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

from core.planner_agent import PlannerAgent
from core.reasoner_agent import ReasonerAgent
from core.explainer_agent import ExplainerAgent
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


def test_reasoner_concatenates_facts():
    agent = ReasonerAgent()
    facts = ["fact1", "fact2"]
    assert agent.reason(facts) == "Based on facts: fact1; fact2"


def test_explainer_formats_steps():
    agent = ExplainerAgent()
    steps = ["step one", "step two"]
    assert agent.explain(steps) == "1. step one\n2. step two"


# Test for MemoryAgent using mocked Neo4j driver

def test_memory_agent_store_and_retrieve(monkeypatch):
    dummy_driver = DummyDriver()
    monkeypatch.setattr("core.memory_agent.GraphDatabase.driver", lambda *a, **kw: dummy_driver)

    memory = MemoryAgent()
    memory.store("fact", "value")

    assert dummy_driver.store["fact"] == "value"
    assert memory.retrieve("fact") == "value"
