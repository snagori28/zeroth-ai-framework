import os
import sys
import pytest
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

from core.document_ingestor import DocumentIngestor
from core.feedback_agent import FeedbackAgent


class DummyLLMAgent:
    def __init__(self):
        self.queries = []

    def query(self, content, mode="factual"):
        self.queries.append((content, mode))
        return "fact1: value1\nfact2: value2"


class DummyMemoryAgent:
    def __init__(self):
        self.stored = []

    def store(self, fact, value, source="user"):
        self.stored.append((fact, value, source))


class DummyFeedbackAgent:
    def review(self, fact, value):
        return "accept"

    def edit(self, fact, value):
        return fact, value


def test_ingest_unsupported_file_extension(tmp_path):
    dummy_llm = DummyLLMAgent()
    dummy_memory = DummyMemoryAgent()
    ingestor = DocumentIngestor(dummy_llm, dummy_memory, DummyFeedbackAgent())

    path = tmp_path / "sample.pdf"
    path.write_text("dummy")

    with pytest.raises(ValueError):
        ingestor.ingest(str(path))


def test_ingest_parses_and_stores_facts(tmp_path):
    dummy_llm = DummyLLMAgent()
    dummy_memory = DummyMemoryAgent()
    ingestor = DocumentIngestor(dummy_llm, dummy_memory, DummyFeedbackAgent())

    path = tmp_path / "sample.txt"
    path.write_text("content")

    ingestor.ingest(str(path))

    assert dummy_llm.queries == [("Extract structured facts from this document:\ncontent", "factual")]
    assert ("fact1", "value1", "document") in dummy_memory.stored
    assert ("fact2", "value2", "document") in dummy_memory.stored


def test_ingest_string_logs_and_stores(caplog):
    dummy_llm = DummyLLMAgent()
    dummy_memory = DummyMemoryAgent()
    ingestor = DocumentIngestor(dummy_llm, dummy_memory, DummyFeedbackAgent())

    with caplog.at_level("INFO"):
        ingestor.ingest("text content")

    assert dummy_llm.queries == [("Extract structured facts from this document:\ntext content", "factual")]
    assert ("fact1", "value1", "document") in dummy_memory.stored
    assert any("Ingesting" in record.message for record in caplog.records)
