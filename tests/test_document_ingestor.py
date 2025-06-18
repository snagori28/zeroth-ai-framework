import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.document_ingestor import DocumentIngestor


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


def test_ingest_unsupported_file_extension(tmp_path):
    dummy_llm = DummyLLMAgent()
    dummy_memory = DummyMemoryAgent()
    ingestor = DocumentIngestor(dummy_llm, dummy_memory)

    path = tmp_path / "sample.pdf"
    path.write_text("dummy")

    with pytest.raises(ValueError):
        ingestor.ingest(str(path))


def test_ingest_parses_and_stores_facts(tmp_path):
    dummy_llm = DummyLLMAgent()
    dummy_memory = DummyMemoryAgent()
    ingestor = DocumentIngestor(dummy_llm, dummy_memory)

    path = tmp_path / "sample.txt"
    path.write_text("content")

    ingestor.ingest(str(path))

    assert dummy_llm.queries == [("content", "factual")]
    assert ("fact1", "value1", "document") in dummy_memory.stored
    assert ("fact2", "value2", "document") in dummy_memory.stored
