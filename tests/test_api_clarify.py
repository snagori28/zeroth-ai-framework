import os
import sys
import types
import importlib

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

# minimal neo4j stub
neo4j_stub = types.ModuleType("neo4j")
class _DummyGraphDatabase:
    @staticmethod
    def driver(*a, **k):
        raise NotImplementedError
neo4j_stub.GraphDatabase = _DummyGraphDatabase
sys.modules["neo4j"] = neo4j_stub

from fastapi.testclient import TestClient

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
sys.modules["spacy"] = spacy_stub


def _dummy_response(text):
    msg = types.SimpleNamespace(content=text)
    choice = types.SimpleNamespace(message=msg)
    return types.SimpleNamespace(choices=[choice])


def test_clarify_endpoint(monkeypatch):
    # Ensure required env vars so import does not prompt
    monkeypatch.setenv("NEO4J_URI", "bolt://test")
    monkeypatch.setenv("NEO4J_USER", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "pass")
    monkeypatch.setenv("OPENAI_API_KEY", "key")

    import config
    importlib.reload(config)

    # Dummy Neo4j driver to satisfy MemoryAgent
    class DummySession:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def run(self, *a, **k):
            return types.SimpleNamespace(single=lambda: None, data=lambda: [])
    class DummyDriver:
        def session(self):
            return DummySession()
    monkeypatch.setattr(neo4j_stub.GraphDatabase, "driver", lambda *a, **k: DummyDriver())
    monkeypatch.setattr(openai_stub.ChatCompletion, "create", lambda **k: _dummy_response("Q1\nQ2"))

    import api_interface
    importlib.reload(api_interface)
    monkeypatch.setattr(api_interface.clarifier.llm_agent, "query", lambda *a, **k: "Q1\nQ2")

    client = TestClient(api_interface.app)
    resp = client.post("/clarify", json={"goal": "test goal"})
    assert resp.status_code == 200
    assert resp.json() == {"questions": ["Q1", "Q2"]}
