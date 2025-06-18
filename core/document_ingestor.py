class DocumentIngestor:
    def __init__(self, llm_agent, memory_agent):
        self.llm_agent = llm_agent
        self.memory_agent = memory_agent

    def ingest(self, content):
        facts = self.llm_agent.query(content, mode="factual")
        for line in facts.split("\n"):
            if ":" in line:
                fact, value = line.split(":", 1)
                self.memory_agent.store(fact.strip(), value.strip(), source="document")
